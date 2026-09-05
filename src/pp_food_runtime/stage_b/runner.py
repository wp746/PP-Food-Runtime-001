from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import Field

from pp_food_runtime.artifacts.store import ArtifactStore, sha256_file
from pp_food_runtime.config import RuntimeMode, RuntimeSettings
from pp_food_runtime.golden.repository import GoldenRepository
from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.evaluation import EvaluationResult, FinalDecision
from pp_food_runtime.models.job import ImageRef, JobContract, JobState
from pp_food_runtime.models.visual import CompiledPrompt, ValidatedBPromptContract
from pp_food_runtime.providers.base import ImageProvider, VisionProvider
from pp_food_runtime.providers.openai_compatible import ImageProviderTimeout
from pp_food_runtime.stage_a.evaluator import StageAEvaluator
from pp_food_runtime.stage_a.runner import StageARunner
from pp_food_runtime.vision.analyzer import ProductAnalyzer

from .art_director import BArtDirector
from .compiler import compile_stage_b
from .copy_firewall import CopyFirewall
from .evaluator import BEvaluator, EvaluationContext, PairwiseComparison
from .production_gate import ProductionGateResult
from .retry import RetryPlan, RetryPlanner
from .translator import CategoryTranslator


class JobResult(FrozenModel):
    job_id: str
    final_state: JobState
    final_decision: FinalDecision
    state_history: list[JobState]
    artifact_dir: Path
    candidates: dict[str, ImageRef]
    evaluations: dict[str, EvaluationResult]
    prompt_hashes: dict[str, str]
    pairwise_comparison: PairwiseComparison | None = None
    production_gate: ProductionGateResult | None = None
    winner_id: str | None = None
    final_image: ImageRef | None = None
    retry_history: list[RetryPlan | ProductionGateResult] = Field(default_factory=list)


class StageBRunner:
    def __init__(
        self,
        settings: RuntimeSettings,
        vision_provider: VisionProvider,
        image_provider: ImageProvider,
        golden_repository: GoldenRepository,
        store: ArtifactStore,
    ):
        self.settings = settings
        self.image_provider = image_provider
        self.golden_repository = golden_repository
        self.store = store
        self.product_analyzer = ProductAnalyzer(vision_provider)
        self.stage_a_runner = StageARunner(
            image_provider,
            settings.artifact_root,
            evaluator=StageAEvaluator(vision_provider),
        )
        self.copy_firewall = CopyFirewall()
        self.translator = CategoryTranslator()
        self.art_director = BArtDirector()
        self.evaluator = BEvaluator(vision_provider)
        self.retry_planner = RetryPlanner()

    def run(self, job: JobContract) -> JobResult:
        job_started = time.perf_counter()
        timings: dict[str, float] = {}
        states = [JobState.B_REQUESTED, JobState.B_ENTRY_VALIDATION]
        if job.source_image is None:
            raise ValueError("Stage B requires source image")
        source = job.source_image
        if sha256_file(source.path) != source.sha256:
            raise ValueError("source image hash mismatch")

        self.store.create_job(job)
        self.store.write_json(job.job_id, "contracts/runtime", self._runtime_evidence())
        self.store.copy_image(job.job_id, "input/source", source.path)
        if job.stage_a_pass:
            self.store.copy_image(job.job_id, "input/stage-a", job.stage_a_pass.path)

        states.append(JobState.STAGE_A_REQUIRED)
        started = time.perf_counter()
        truth = self.product_analyzer.analyze(source, job.user_facts)
        timings["product_analysis_seconds"] = self._elapsed(started)

        started = time.perf_counter()
        stage_a = self.stage_a_runner.run(job, source, truth)
        timings["stage_a_total_seconds"] = self._elapsed(started)
        states.extend([JobState.STAGE_A_PASS, JobState.PRODUCT_LOCK_BRIDGE_READY])

        copy = self.copy_firewall.build(job.user_facts)
        states.extend([JobState.COPY_FIREWALL_READY, JobState.CURRENT_PRODUCT_ANALYSIS])
        self.store.write_json(job.job_id, "contracts/product_truth", truth)
        self.store.write_json(job.job_id, "contracts/stage_a_bridge", stage_a)
        self.store.write_json(job.job_id, "contracts/copy_allowlist", copy)

        started = time.perf_counter()
        translation = self.translator.translate(truth, job.user_facts)
        timings["category_translation_seconds"] = self._elapsed(started)
        states.append(JobState.CATEGORY_VISUAL_TRANSLATION)
        self.store.write_json(job.job_id, "contracts/visual_translation", translation)

        started = time.perf_counter()
        goldens = self.golden_repository.retriever().retrieve(
            {
                "primary_category": translation.primary_category,
                "pack_or_food": truth.pack_or_food,
                "sensory_tags": truth.sensory_keywords,
                "visual_problems": ["product_hero", "headline_pressure", "depth"],
            },
            limit=3,
        )
        timings["golden_retrieval_seconds"] = self._elapsed(started)
        if job.golden_case:
            goldens = sorted(
                goldens,
                key=lambda pack: (pack.golden_id != job.golden_case, pack.golden_id),
            )
        states.append(JobState.GOLDEN_RETRIEVAL)
        self.store.write_json(
            job.job_id,
            "contracts/golden_retrieval",
            {"goldens": [g.model_dump(mode="json") for g in goldens]},
        )
        for golden in goldens:
            if golden.local_asset_path:
                self.store.copy_image(
                    job.job_id,
                    f"input/golden-{golden.golden_id}",
                    Path(golden.local_asset_path),
                )

        started = time.perf_counter()
        director_candidates = self.art_director.create_candidates(
            truth, translation, copy, goldens
        )
        primary, challenger = self.art_director.select_finalists(director_candidates)
        timings["art_direction_seconds"] = self._elapsed(started)
        states.extend([JobState.ART_DIRECTION, JobState.ART_DIRECTION_VALIDATION])
        for direction in director_candidates:
            self.store.write_json(
                job.job_id,
                f"contracts/direction-board-{direction.concept_id}",
                direction,
            )

        directions = {"primary": primary, "challenger": challenger}
        selected_ids = (
            ["primary"]
            if self.settings.runtime_mode is RuntimeMode.PRODUCTION_FAST
            else ["primary", "challenger"]
        )
        for candidate_id in selected_ids:
            self.store.write_json(
                job.job_id,
                f"contracts/direction-{candidate_id}",
                directions[candidate_id],
            )

        started = time.perf_counter()
        prompt_contracts = {
            candidate_id: ValidatedBPromptContract(
                truth=truth,
                bridge=stage_a.bridge,
                translation=translation,
                direction=directions[candidate_id],
                exact_copy=copy.exact_copy_lines(),
                golden_principles=[
                    principle for golden in goldens for principle in golden.principles
                ],
                hard_negatives=[
                    "do not invent unsupported hard facts",
                    "do not change current product identity",
                    "do not transfer Golden skin",
                ],
                aspect_ratio=job.aspect_ratio,
            )
            for candidate_id in selected_ids
        }
        compiled = {
            candidate_id: compile_stage_b(
                contract, self.image_provider.capability_profile
            )
            for candidate_id, contract in prompt_contracts.items()
        }
        timings["prompt_compile_seconds"] = self._elapsed(started)
        states.append(JobState.PROMPT_CONTRACT_READY)
        for candidate_id, prompt in compiled.items():
            self.store.write_json(job.job_id, f"prompts/{candidate_id}", prompt)

        if self.settings.runtime_mode is RuntimeMode.PRODUCTION_FAST:
            return self._run_production_fast(
                job=job,
                states=states,
                source=source,
                stage_a=stage_a,
                truth=truth,
                copy=copy,
                translation=translation,
                goldens=goldens,
                compiled=compiled,
                timings=timings,
                job_started=job_started,
            )
        return self._run_validation(
            job=job,
            states=states,
            source=source,
            stage_a=stage_a,
            truth=truth,
            copy=copy,
            translation=translation,
            goldens=goldens,
            compiled=compiled,
            timings=timings,
            job_started=job_started,
        )

    def _run_production_fast(
        self,
        *,
        job,
        states,
        source,
        stage_a,
        truth,
        copy,
        translation,
        goldens,
        compiled,
        timings,
        job_started,
    ) -> JobResult:
        candidates: dict[str, ImageRef] = {}
        prompt_hashes = {"primary": compiled["primary"].sha256}

        started = time.perf_counter()
        candidates["primary"] = self._render_candidate(
            job, "primary", compiled["primary"], stage_a.image
        )
        timings["b_generation_primary_seconds"] = self._elapsed(started)
        states.append(JobState.FINALIST_RENDER)

        primary_context = self._context(
            "primary",
            source,
            stage_a.image,
            candidates["primary"],
            truth,
            copy,
            translation,
            goldens,
        )
        started = time.perf_counter()
        gate = self.evaluator.evaluate_production(primary_context)
        timings["production_gate_primary_seconds"] = self._elapsed(started)
        self.store.write_json(job.job_id, "eval/production-primary", gate)
        states.append(JobState.FINALIST_VISUAL_EVAL)
        retry_history: list[RetryPlan | ProductionGateResult] = []
        final_gate = gate
        winner_id: str | None = None
        final_image = None

        if gate.decision is FinalDecision.PASS:
            winner_id = "primary"
        elif gate.retry_eligible and self.settings.production_max_creative_retries >= 1:
            states.append(JobState.TARGETED_REFINEMENT)
            retry_history.append(gate)
            retry_prompt = self._production_retry_prompt(compiled["primary"], gate)
            compiled["retry-1"] = retry_prompt
            prompt_hashes["retry-1"] = retry_prompt.sha256
            self.store.write_json(job.job_id, "prompts/retry-1", retry_prompt)

            started = time.perf_counter()
            candidates["retry-1"] = self._render_candidate(
                job, "retry-1", retry_prompt, stage_a.image
            )
            timings["b_generation_retry_1_seconds"] = self._elapsed(started)
            retry_context = self._context(
                "retry-1",
                source,
                stage_a.image,
                candidates["retry-1"],
                truth,
                copy,
                translation,
                goldens,
            )
            started = time.perf_counter()
            final_gate = self.evaluator.evaluate_production(retry_context)
            timings["production_gate_retry_1_seconds"] = self._elapsed(started)
            self.store.write_json(
                job.job_id, "eval/production-retry-1", final_gate
            )
            if final_gate.decision is FinalDecision.PASS:
                winner_id = "retry-1"

        if winner_id:
            states.extend([JobState.FINAL_QC, JobState.B_PASS])
            final_image = self.store.copy_image(
                job.job_id, "final/winner", candidates[winner_id].path
            )
            final_state = JobState.B_PASS
            final_decision = FinalDecision.PASS
        else:
            states.append(JobState.NEEDS_HUMAN_REVIEW)
            final_state = JobState.NEEDS_HUMAN_REVIEW
            final_decision = (
                final_gate.decision
                if final_gate.decision is FinalDecision.NEEDS_SECOND_EVALUATION
                else FinalDecision.NEEDS_HUMAN_REVIEW
            )

        decision_payload = {
            "runtime_mode": self.settings.runtime_mode.value,
            "decision": final_decision.value,
            "winner_id": winner_id,
            "production_gate": final_gate.model_dump(mode="json"),
            "creative_retry_count": len(retry_history),
        }
        self.store.write_json(job.job_id, "final/decision", decision_payload)
        timings["runtime_total_seconds"] = self._elapsed(job_started)
        self.store.write_json(job.job_id, "final/timing", timings)
        artifact_dir = self._write_manifest(job, states, stage_a.image, timings)
        return JobResult(
            job_id=job.job_id,
            final_state=final_state,
            final_decision=final_decision,
            state_history=states,
            artifact_dir=artifact_dir,
            candidates=candidates,
            evaluations={},
            prompt_hashes=prompt_hashes,
            pairwise_comparison=None,
            production_gate=final_gate,
            winner_id=winner_id,
            final_image=final_image,
            retry_history=retry_history,
        )

    def _run_validation(
        self,
        *,
        job,
        states,
        source,
        stage_a,
        truth,
        copy,
        translation,
        goldens,
        compiled,
        timings,
        job_started,
    ) -> JobResult:
        candidates: dict[str, ImageRef] = {}
        for candidate_id in ("primary", "challenger"):
            started = time.perf_counter()
            candidates[candidate_id] = self._render_candidate(
                job, candidate_id, compiled[candidate_id], stage_a.image
            )
            timings[f"b_generation_{candidate_id}_seconds"] = self._elapsed(started)
        states.append(JobState.FINALIST_RENDER)

        evaluations: dict[str, EvaluationResult] = {}
        evaluation_contexts: dict[str, EvaluationContext] = {}
        for candidate_id, candidate in candidates.items():
            evaluation_contexts[candidate_id] = self._context(
                candidate_id,
                source,
                stage_a.image,
                candidate,
                truth,
                copy,
                translation,
                goldens,
            )
            started = time.perf_counter()
            evaluations[candidate_id] = self.evaluator.evaluate(
                evaluation_contexts[candidate_id]
            )
            timings[f"validation_eval_{candidate_id}_seconds"] = self._elapsed(
                started
            )

        started = time.perf_counter()
        pairwise_comparison = self.evaluator.compare(
            list(evaluation_contexts.values())
        )
        timings["pairwise_seconds"] = self._elapsed(started)
        self.store.write_json(job.job_id, "eval/pairwise", pairwise_comparison)
        states.extend([JobState.FINALIST_VISUAL_EVAL, JobState.WINNER_SELECTION])
        remaining = sorted(
            (
                candidate_id
                for candidate_id in evaluations
                if candidate_id != pairwise_comparison.winner_id
            ),
            key=lambda item: evaluations[item].golden_vector.weighted_score,
            reverse=True,
        )
        ranking = [pairwise_comparison.winner_id, *remaining]
        pairwise_winner = pairwise_comparison.winner_id
        evaluations = {
            key: value.model_copy(update={"pairwise_winner": pairwise_winner})
            for key, value in evaluations.items()
        }
        for candidate_id, evaluation in evaluations.items():
            self.store.write_json(job.job_id, f"eval/{candidate_id}", evaluation)

        pairwise_qualified = (
            pairwise_comparison.visually_distinct
            and pairwise_comparison.confidence >= 0.65
        )
        qualified = [
            candidate_id
            for candidate_id in ranking
            if pairwise_qualified
            and evaluations[candidate_id].final_decision is FinalDecision.PASS
        ]
        retry_history: list[RetryPlan | ProductionGateResult] = []
        winner_id = qualified[0] if qualified else None
        final_image = None
        if winner_id:
            states.extend([JobState.FINAL_QC, JobState.B_PASS])
            final_image = self.store.copy_image(
                job.job_id, "final/winner", candidates[winner_id].path
            )
            final_state = JobState.B_PASS
            final_decision = FinalDecision.PASS
        else:
            retry_history.append(
                self.retry_planner.plan(evaluations[pairwise_winner], cycle=1)
            )
            self.store.write_json(job.job_id, "retry/cycle-1", retry_history[0])
            states.extend(
                [JobState.TARGETED_REFINEMENT, JobState.NEEDS_HUMAN_REVIEW]
            )
            final_state = JobState.NEEDS_HUMAN_REVIEW
            final_decision = FinalDecision.NO_QUALIFIED_WINNER

        self.store.write_json(
            job.job_id,
            "final/decision",
            {
                "runtime_mode": self.settings.runtime_mode.value,
                "decision": final_decision.value,
                "winner_id": winner_id,
                "pairwise_winner": pairwise_winner,
                "pairwise_visually_distinct": pairwise_comparison.visually_distinct,
                "pairwise_confidence": pairwise_comparison.confidence,
                "scores": {
                    key: value.golden_vector.weighted_score
                    for key, value in evaluations.items()
                },
                "failure_codes": {
                    key: [code.value for code in value.critical_failures]
                    for key, value in evaluations.items()
                },
            },
        )
        timings["runtime_total_seconds"] = self._elapsed(job_started)
        self.store.write_json(job.job_id, "final/timing", timings)
        artifact_dir = self._write_manifest(job, states, stage_a.image, timings)
        return JobResult(
            job_id=job.job_id,
            final_state=final_state,
            final_decision=final_decision,
            state_history=states,
            artifact_dir=artifact_dir,
            candidates=candidates,
            evaluations=evaluations,
            prompt_hashes={key: value.sha256 for key, value in compiled.items()},
            pairwise_comparison=pairwise_comparison,
            production_gate=None,
            winner_id=winner_id,
            final_image=final_image,
            retry_history=retry_history,
        )

    def _render_candidate(
        self,
        job: JobContract,
        candidate_id: str,
        prompt: CompiledPrompt,
        stage_a: ImageRef,
    ) -> ImageRef:
        output_path = self.store.target(job.job_id, f"{candidate_id}/image.png")
        started_at = self._utc_timestamp()
        started = time.perf_counter()
        try:
            candidate = self.image_provider.generate(
                [stage_a], prompt.text, job.aspect_ratio, output_path
            )
        except ImageProviderTimeout:
            self.store.write_json(
                job.job_id,
                f"{candidate_id}/generation",
                {
                    "status": "TIMEOUT",
                    "failure_class": "PROVIDER",
                    "failure_code": ImageProviderTimeout.code,
                    "stage_a_reference_sha256": stage_a.sha256,
                    "compiled_prompt_sha256": prompt.sha256,
                    "provider": self.image_provider.capability_profile.provider_id,
                    "model": self.image_provider.capability_profile.model_id,
                    "request_id": None,
                    "started_at": started_at,
                    "ended_at": self._utc_timestamp(),
                    "latency_seconds": self._elapsed(started),
                    "output_sha256": None,
                },
            )
            raise
        if not candidate.reference_binding_verified:
            raise RuntimeError(
                f"{candidate_id} was not bound to current Stage A reference"
            )
        self.store.write_json(
            job.job_id,
            f"{candidate_id}/generation",
            {
                "status": "PASS",
                "failure_class": "NONE",
                "failure_code": None,
                "stage_a_reference_sha256": stage_a.sha256,
                "compiled_prompt_sha256": prompt.sha256,
                "provider": self.image_provider.capability_profile.provider_id,
                "model": self.image_provider.capability_profile.model_id,
                "request_id": candidate.provider_request_id,
                "started_at": started_at,
                "ended_at": self._utc_timestamp(),
                "latency_seconds": self._elapsed(started),
                "output_sha256": candidate.sha256,
            },
        )
        return candidate

    @staticmethod
    def _context(
        candidate_id,
        source,
        stage_a,
        candidate,
        truth,
        copy,
        translation,
        goldens,
    ):
        return EvaluationContext(
            candidate_id=candidate_id,
            source=source,
            stage_a=stage_a,
            candidate=candidate,
            truth=truth,
            copy_allowlist=copy,
            translation=translation,
            goldens=goldens,
        )

    @staticmethod
    def _production_retry_prompt(
        prompt: CompiledPrompt, gate: ProductionGateResult
    ) -> CompiledPrompt:
        text = (
            prompt.text.rstrip()
            + "\n\n## PRODUCTION TARGETED REPAIR\n"
            + gate.repair_instruction.strip()
            + "\nThis is the only creative retry. Do not redesign passing dimensions.\n"
        )
        return CompiledPrompt(
            text=text,
            sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        )

    def _write_manifest(
        self,
        job: JobContract,
        states: list[JobState],
        stage_a: ImageRef,
        timings: dict[str, float],
    ) -> Path:
        artifact_dir = self.store.job_dir(job.job_id).resolve()
        artifacts = sorted(
            {
                str(path.relative_to(artifact_dir)): sha256_file(path)
                for path in artifact_dir.rglob("*")
                if path.is_file() and path.name != "manifest.json"
            }.items()
        )
        self.store.write_json(
            job.job_id,
            "manifest",
            {
                "job_id": job.job_id,
                "runtime_version": self.settings.runtime_version,
                "runtime_mode": self.settings.runtime_mode.value,
                "source_sha256": job.source_image.sha256 if job.source_image else None,
                "stage_a_sha256": stage_a.sha256,
                "timing": timings,
                "state_history": [state.value for state in states],
                "artifacts": [
                    {"path": path, "sha256": digest} for path, digest in artifacts
                ],
            },
        )
        return artifact_dir

    def _runtime_evidence(self) -> dict[str, object]:
        summary = self.settings.safe_provider_summary()
        profiles = {
            "vision": self.product_analyzer.provider.capability_profile.model_dump(
                mode="json"
            ),
            "image": self.image_provider.capability_profile.model_dump(mode="json"),
        }
        encoded = json.dumps(
            profiles, ensure_ascii=False, sort_keys=True
        ).encode("utf-8")
        return {
            **summary,
            "provider_profiles": profiles,
            "provider_profile_sha256": hashlib.sha256(encoded).hexdigest(),
        }

    @staticmethod
    def _elapsed(started: float) -> float:
        return round(max(0.0, time.perf_counter() - started), 3)

    @staticmethod
    def _utc_timestamp() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
            "+00:00", "Z"
        )
