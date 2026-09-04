from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import Field

from pp_food_runtime.artifacts.store import ArtifactStore, sha256_file
from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.golden.repository import GoldenRepository
from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.evaluation import EvaluationResult, FinalDecision
from pp_food_runtime.models.job import ImageRef, JobContract, JobState
from pp_food_runtime.models.visual import ValidatedBPromptContract
from pp_food_runtime.providers.base import ImageProvider, VisionProvider
from pp_food_runtime.providers.openai_compatible import ImageProviderTimeout
from pp_food_runtime.stage_a.runner import StageARunner
from pp_food_runtime.stage_a.evaluator import StageAEvaluator
from pp_food_runtime.vision.analyzer import ProductAnalyzer

from .art_director import BArtDirector
from .compiler import compile_stage_b
from .copy_firewall import CopyFirewall
from .evaluator import BEvaluator, EvaluationContext, PairwiseComparison
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
    pairwise_comparison: PairwiseComparison
    winner_id: str | None = None
    final_image: ImageRef | None = None
    retry_history: list[RetryPlan] = Field(default_factory=list)


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
        states = [JobState.B_REQUESTED, JobState.B_ENTRY_VALIDATION]
        if job.source_image is None:
            raise ValueError("Stage B requires source image")
        source = job.source_image
        if sha256_file(source.path) != source.sha256:
            raise ValueError("source image hash mismatch")
        self.store.create_job(job)
        self.store.write_json(job.job_id, "contracts/runtime", self._runtime_evidence())
        source_copy = self.store.copy_image(job.job_id, "input/source", source.path)
        if job.stage_a_pass:
            self.store.copy_image(job.job_id, "input/stage-a", job.stage_a_pass.path)

        states.append(JobState.STAGE_A_REQUIRED)
        truth = self.product_analyzer.analyze(source, job.user_facts)
        stage_a = self.stage_a_runner.run(job, source, truth)
        states.extend([JobState.STAGE_A_PASS, JobState.PRODUCT_LOCK_BRIDGE_READY])
        copy = self.copy_firewall.build(job.user_facts)
        states.extend([JobState.COPY_FIREWALL_READY, JobState.CURRENT_PRODUCT_ANALYSIS])
        self.store.write_json(job.job_id, "contracts/product_truth", truth)
        self.store.write_json(job.job_id, "contracts/stage_a_bridge", stage_a)
        self.store.write_json(job.job_id, "contracts/copy_allowlist", copy)

        translation = self.translator.translate(truth, job.user_facts)
        states.append(JobState.CATEGORY_VISUAL_TRANSLATION)
        self.store.write_json(job.job_id, "contracts/visual_translation", translation)
        goldens = self.golden_repository.retriever().retrieve(
            {
                "primary_category": translation.primary_category,
                "pack_or_food": truth.pack_or_food,
                "sensory_tags": truth.sensory_keywords,
                "visual_problems": ["product_hero", "headline_pressure", "depth"],
            },
            limit=3,
        )
        if job.golden_case:
            goldens = sorted(goldens, key=lambda pack: (pack.golden_id != job.golden_case, pack.golden_id))
        states.append(JobState.GOLDEN_RETRIEVAL)
        self.store.write_json(job.job_id, "contracts/golden_retrieval", {"goldens": [g.model_dump(mode="json") for g in goldens]})
        for golden in goldens:
            if golden.local_asset_path:
                self.store.copy_image(job.job_id, f"input/golden-{golden.golden_id}", Path(golden.local_asset_path))

        director_candidates = self.art_director.create_candidates(truth, translation, copy, goldens)
        primary, editorial = self.art_director.select_finalists(director_candidates)
        states.extend([JobState.ART_DIRECTION, JobState.ART_DIRECTION_VALIDATION])
        for direction in director_candidates:
            self.store.write_json(job.job_id, f"contracts/direction-board-{direction.concept_id}", direction)
        directions = {"primary": primary, "challenger": editorial}
        for candidate_id, direction in directions.items():
            self.store.write_json(job.job_id, f"contracts/direction-{candidate_id}", direction)

        prompt_contracts = {
            candidate_id: ValidatedBPromptContract(
                truth=truth,
                bridge=stage_a.bridge,
                translation=translation,
                direction=direction,
                exact_copy=copy.exact_copy_lines(),
                golden_principles=[principle for golden in goldens for principle in golden.principles],
                hard_negatives=[
                    "do not invent unsupported hard facts",
                    "do not change current product identity",
                    "do not transfer Golden skin",
                ],
                aspect_ratio=job.aspect_ratio,
            )
            for candidate_id, direction in directions.items()
        }
        compiled = {
            candidate_id: compile_stage_b(contract, self.image_provider.capability_profile)
            for candidate_id, contract in prompt_contracts.items()
        }
        states.append(JobState.PROMPT_CONTRACT_READY)
        for candidate_id, prompt in compiled.items():
            self.store.write_json(job.job_id, f"prompts/{candidate_id}", prompt)

        candidates = {}
        for candidate_id in ("primary", "challenger"):
            prompt = compiled[candidate_id]
            output_path = self.store.target(job.job_id, f"{candidate_id}/image.png")
            started_at = self._utc_timestamp()
            started = time.perf_counter()
            try:
                candidates[candidate_id] = self.image_provider.generate(
                    [stage_a.image], prompt.text, job.aspect_ratio, output_path
                )
            except ImageProviderTimeout:
                self.store.write_json(
                    job.job_id,
                    f"{candidate_id}/generation",
                    {
                        "status": "TIMEOUT",
                        "failure_code": ImageProviderTimeout.code,
                        "stage_a_reference_sha256": stage_a.image.sha256,
                        "compiled_prompt_sha256": prompt.sha256,
                        "provider": self.image_provider.capability_profile.provider_id,
                        "model": self.image_provider.capability_profile.model_id,
                        "request_id": None,
                        "started_at": started_at,
                        "ended_at": self._utc_timestamp(),
                        "latency_seconds": round(time.perf_counter() - started, 3),
                        "output_sha256": None,
                    },
                )
                raise
            if not candidates[candidate_id].reference_binding_verified:
                raise RuntimeError(f"{candidate_id} was not bound to current Stage A reference")
            self.store.write_json(
                job.job_id,
                f"{candidate_id}/generation",
                {
                    "status": "PASS",
                    "failure_code": None,
                    "stage_a_reference_sha256": stage_a.image.sha256,
                    "compiled_prompt_sha256": prompt.sha256,
                    "provider": self.image_provider.capability_profile.provider_id,
                    "model": self.image_provider.capability_profile.model_id,
                    "request_id": candidates[candidate_id].provider_request_id,
                    "started_at": started_at,
                    "ended_at": self._utc_timestamp(),
                    "latency_seconds": round(time.perf_counter() - started, 3),
                    "output_sha256": candidates[candidate_id].sha256,
                },
            )
        states.append(JobState.FINALIST_RENDER)

        evaluations = {}
        evaluation_contexts = {}
        for candidate_id, candidate in candidates.items():
            evaluation_contexts[candidate_id] = EvaluationContext(
                candidate_id=candidate_id,
                source=source,
                stage_a=stage_a.image,
                candidate=candidate,
                truth=truth,
                copy_allowlist=copy,
                translation=translation,
                goldens=goldens,
            )
            evaluations[candidate_id] = self.evaluator.evaluate(evaluation_contexts[candidate_id])
        pairwise_comparison = self.evaluator.compare(list(evaluation_contexts.values()))
        self.store.write_json(job.job_id, "eval/pairwise", pairwise_comparison)
        states.extend([JobState.FINALIST_VISUAL_EVAL, JobState.WINNER_SELECTION])
        remaining = sorted(
            (candidate_id for candidate_id in evaluations if candidate_id != pairwise_comparison.winner_id),
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

        pairwise_qualified = pairwise_comparison.visually_distinct and pairwise_comparison.confidence >= 0.65
        qualified = [
            candidate_id
            for candidate_id in ranking
            if pairwise_qualified and evaluations[candidate_id].final_decision is FinalDecision.PASS
        ]
        retry_history = []
        winner_id = qualified[0] if qualified else None
        final_image = None
        if winner_id:
            states.extend([JobState.FINAL_QC, JobState.B_PASS])
            final_image = self.store.copy_image(job.job_id, "final/winner", candidates[winner_id].path)
            final_state = JobState.B_PASS
            final_decision = FinalDecision.PASS
        else:
            retry_history.append(self.retry_planner.plan(evaluations[pairwise_winner], cycle=1))
            self.store.write_json(job.job_id, "retry/cycle-1", retry_history[0])
            states.extend([JobState.TARGETED_REFINEMENT, JobState.NEEDS_HUMAN_REVIEW])
            final_state = JobState.NEEDS_HUMAN_REVIEW
            final_decision = FinalDecision.NO_QUALIFIED_WINNER

        decision_payload = {
            "decision": final_decision.value,
            "winner_id": winner_id,
            "pairwise_winner": pairwise_winner,
            "pairwise_visually_distinct": pairwise_comparison.visually_distinct,
            "pairwise_confidence": pairwise_comparison.confidence,
            "scores": {
                key: value.golden_vector.weighted_score for key, value in evaluations.items()
            },
            "failure_codes": {
                key: [code.value for code in value.critical_failures]
                for key, value in evaluations.items()
            },
        }
        self.store.write_json(job.job_id, "final/decision", decision_payload)
        artifact_dir = self.store.job_dir(job.job_id).resolve()
        artifacts = sorted(
            {
                str(path.relative_to(artifact_dir)): sha256_file(path)
                for path in artifact_dir.rglob("*")
                if path.is_file()
            }.items()
        )
        self.store.write_json(
            job.job_id,
            "manifest",
            {
                "job_id": job.job_id,
                "runtime_version": self.settings.runtime_version,
                "state_history": [state.value for state in states],
                "artifacts": [{"path": path, "sha256": digest} for path, digest in artifacts],
            },
        )
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
            winner_id=winner_id,
            final_image=final_image,
            retry_history=retry_history,
        )

    def _runtime_evidence(self) -> dict[str, object]:
        summary = self.settings.safe_provider_summary()
        profiles = {
            "vision": self.product_analyzer.provider.capability_profile.model_dump(mode="json"),
            "image": self.image_provider.capability_profile.model_dump(mode="json"),
        }
        encoded = json.dumps(profiles, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return {**summary, "provider_profiles": profiles, "provider_profile_sha256": hashlib.sha256(encoded).hexdigest()}

    @staticmethod
    def _utc_timestamp() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
