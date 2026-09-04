from __future__ import annotations

import json
from pathlib import Path

from PIL import Image
from pydantic import Field

from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.evaluation import (
    EvaluationResult,
    FailureCode,
    FinalDecision,
    GoldenVector,
    VisibleEvidence,
)
from pp_food_runtime.models.job import ImageRef
from pp_food_runtime.models.product import ProductTruth
from pp_food_runtime.models.visual import CategoryVisualTranslation, GoldenPrinciplePack
from pp_food_runtime.providers.base import VisionProvider

from .copy_firewall import CopyAllowlist


FLOORS = {
    "product_hero_strength": 9.2,
    "headline_aggression": 8.8,
    "typography_product_symbiosis": 8.8,
    "one_big_idea_clarity": 9.0,
    "compositional_depth_tension": 8.8,
    "category_inevitability": 9.0,
    "information_density_control": 8.8,
    "commercial_finish": 9.2,
}


class EvaluationContext(FrozenModel):
    candidate_id: str
    source: ImageRef
    stage_a: ImageRef
    candidate: ImageRef
    truth: ProductTruth
    copy_allowlist: CopyAllowlist
    translation: CategoryVisualTranslation
    goldens: list[GoldenPrinciplePack]


class RawEvaluation(FrozenModel):
    mechanical_pass: bool
    product_truth_pass: bool
    copy_truth_pass: bool
    first_read_order: list[str]
    golden_vector: GoldenVector
    critical_failures: list[str] = Field(default_factory=list)
    materially_weaker_core_dimensions: list[str] = Field(default_factory=list)
    evidence: list[VisibleEvidence] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class RawPairwiseComparison(FrozenModel):
    winner_id: str
    visually_distinct: bool
    winner_reason: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class PairwiseComparison(FrozenModel):
    candidate_ids: list[str]
    actual_images_compared: bool
    winner_id: str
    visually_distinct: bool
    winner_reason: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


EVALUATOR_INSTRUCTION = """
Act as an independent forensic commercial-art evaluator. You receive, in order: current source, current-job
Stage A PASS, current B candidate, then zero or more relevant human Goldens. The generator's rationale and
self-scores are intentionally unavailable. Evaluate visible pixels, not checklist wording.

Sequence: mechanical 9:16/decode -> product truth -> exact copy truth -> first read -> eight Golden-vector scores
-> Golden-relative comparison -> anti-patterns -> commercial finish. Product identity, geometry, surface, package,
vessel, topology, count, and major physical relationships must stay faithful. Exact authorized text may appear;
any unsupported hard fact is a failure. First read should be product, headline, then big idea/support.

For each of the eight score dimensions provide visible evidence naming what is visible, where it is visible, and
why it helps or hurts. A beautiful scene cannot compensate for a weak or changed product. Compare visual pressure
and campaign maturity with Goldens, never demand their exact skin. Mark materially_weaker_core_dimensions when
the candidate is clearly below Golden pressure. Allowed critical failure codes: PRODUCT_IDENTITY_DRIFT,
COPY_TRUTH_FAILURE, MECHANICAL_FAILURE, SAFE_EDITORIAL_COLLAPSE, SCENE_DOMINATES_PRODUCT,
CATEGORY_CLICHE_DEPENDENCE, GENERIC_PREMIUM_SKIN, TEMPLATE_REUSE, PHOTO_PLUS_TEXT,
INFORMATION_STARVATION, INFORMATION_OVERLOAD, HERO_WEAK, HEADLINE_WEAK, TYPOGRAPHY_DISCONNECTED,
BIG_IDEA_WEAK, COMPOSITION_FLAT, CATEGORY_WEAK, COMMERCIAL_FINISH_WEAK, GOLDEN_DISTANCE,
REFERENCE_BINDING_FAILURE. Return strict JSON only. Never infer PASS from the prompt's claims.
""".strip()


PAIRWISE_INSTRUCTION = """
Act as an independent rendered visual-audition judge. You receive, in order: current source, current Stage A PASS,
candidate 1, candidate 2, then zero or more relevant human Goldens. Compare the two actual B renders directly.
Images 1 and 2 are control references only and must never be treated as candidates. Images 3 and 4 are the only
candidate renders. Use the exact business candidate ID supplied for image 3 or image 4 as winner_id.
Choose the stronger campaign result by product hero strength first, then campaign refinement, product-led
memorability, category inevitability, typography integration, compositional tension, and anti-template originality.
Reject novelty when scene or headline demotes the product. Determine whether the two candidates are genuinely
different in composition skeleton, negative-space strategy, headline role, depth, material family, and lighting.
Text planning and prompt claims are not evidence. Return concise strict JSON with visible pairwise evidence only.
""".strip()


def decide_evaluation(
    *,
    candidate_id: str,
    mechanical_pass: bool,
    product_truth_pass: bool,
    copy_truth_pass: bool,
    golden_vector: GoldenVector,
    critical_failures: list[FailureCode],
    materially_weaker_core_dimensions: list[str],
    evidence: list[VisibleEvidence],
    confidence: float,
    pairwise_winner: str | None = None,
) -> EvaluationResult:
    if len(evidence) < len(FLOORS):
        capped = {
            field: min(float(getattr(golden_vector, field)), 7.5)
            for field in GoldenVector.model_fields
        }
        golden_vector = GoldenVector(**capped)
    if confidence < 0.65:
        decision = FinalDecision.NEEDS_SECOND_EVALUATION
    elif not (mechanical_pass and product_truth_pass and copy_truth_pass) or critical_failures:
        decision = FinalDecision.RETRY
    elif len(materially_weaker_core_dimensions) >= 2:
        decision = FinalDecision.RETRY
    elif any(getattr(golden_vector, name) < floor for name, floor in FLOORS.items()):
        decision = FinalDecision.RETRY
    else:
        decision = FinalDecision.PASS
    return EvaluationResult(
        candidate_id=candidate_id,
        mechanical_pass=mechanical_pass,
        product_truth_pass=product_truth_pass,
        copy_truth_pass=copy_truth_pass,
        golden_vector=golden_vector,
        critical_failures=critical_failures,
        materially_weaker_core_dimensions=materially_weaker_core_dimensions,
        evidence=evidence,
        pairwise_winner=pairwise_winner,
        final_decision=decision,
        confidence=confidence,
    )


class BEvaluator:
    def __init__(self, provider: VisionProvider):
        self.provider = provider

    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        local_mechanical = self._mechanical_pass(context.candidate)
        payload = {
            "candidate_id": context.candidate_id,
            "product_truth": context.truth.model_dump(mode="json"),
            "authorized_exact_copy": context.copy_allowlist.exact_copy_lines(),
            "category_translation": context.translation.model_dump(mode="json"),
            "golden_principle_packs": [
                {
                    "golden_id": golden.golden_id,
                    "principles": golden.principles,
                    "prohibited_transfer": golden.prohibited_transfer,
                }
                for golden in context.goldens
            ],
        }
        instruction = f"{EVALUATOR_INSTRUCTION}\nEvaluation context:\n{json.dumps(payload, ensure_ascii=False, sort_keys=True)}"
        images: list[Path | ImageRef] = [context.source, context.stage_a, context.candidate]
        images.extend(Path(golden.local_asset_path) for golden in context.goldens if golden.local_asset_path)
        raw = self.provider.analyze(images, instruction, RawEvaluation)
        failures = []
        for value in raw.critical_failures:
            try:
                failures.append(FailureCode(value))
            except ValueError:
                if FailureCode.GOLDEN_DISTANCE not in failures:
                    failures.append(FailureCode.GOLDEN_DISTANCE)
        if not context.candidate.reference_binding_verified:
            failures.append(FailureCode.REFERENCE_BINDING_FAILURE)
        return decide_evaluation(
            candidate_id=context.candidate_id,
            mechanical_pass=local_mechanical and raw.mechanical_pass,
            product_truth_pass=context.candidate.reference_binding_verified and raw.product_truth_pass,
            copy_truth_pass=raw.copy_truth_pass,
            golden_vector=raw.golden_vector,
            critical_failures=list(dict.fromkeys(failures)),
            materially_weaker_core_dimensions=raw.materially_weaker_core_dimensions,
            evidence=raw.evidence,
            confidence=raw.confidence,
        )

    def compare(self, contexts: list[EvaluationContext]) -> PairwiseComparison:
        if len(contexts) != 2:
            raise ValueError("rendered visual audition requires exactly two candidates")
        candidate_ids = [context.candidate_id for context in contexts]
        if len(set(candidate_ids)) != 2:
            raise ValueError("rendered visual audition candidate ids must be distinct")
        first = contexts[0]
        if any(
            context.source.sha256 != first.source.sha256
            or context.stage_a.sha256 != first.stage_a.sha256
            for context in contexts[1:]
        ):
            raise ValueError("pairwise candidates must share current source and Stage A")
        payload = {
            "candidate_order": candidate_ids,
            "image_slot_map": {
                "image_1": "SOURCE_CONTROL_ONLY",
                "image_2": "STAGE_A_CONTROL_ONLY",
                "image_3": candidate_ids[0],
                "image_4": candidate_ids[1],
            },
            "valid_winner_ids": candidate_ids,
            "product_truth": first.truth.model_dump(mode="json"),
            "authorized_exact_copy": first.copy_allowlist.exact_copy_lines(),
            "category_translation": first.translation.model_dump(mode="json"),
        }
        instruction = (
            f"{PAIRWISE_INSTRUCTION}\nEvaluation context:\n"
            f"{json.dumps(payload, ensure_ascii=False, sort_keys=True)}"
        )
        images: list[Path | ImageRef] = [first.source, first.stage_a]
        images.extend(context.candidate for context in contexts)
        images.extend(
            Path(golden.local_asset_path)
            for golden in first.goldens
            if golden.local_asset_path
        )
        raw = self.provider.analyze(images, instruction, RawPairwiseComparison)
        normalized = raw.winner_id.strip().lower().replace(" ", "_")
        winner_id = {
            "candidate_1": candidate_ids[0],
            "candidate_2": candidate_ids[1],
        }.get(normalized, raw.winner_id)
        if winner_id not in candidate_ids:
            raise ValueError("pairwise evaluator returned an unknown winner id")
        return PairwiseComparison(
            candidate_ids=candidate_ids,
            actual_images_compared=True,
            winner_id=winner_id,
            **raw.model_dump(exclude={"winner_id"}),
        )

    @staticmethod
    def _mechanical_pass(candidate: ImageRef) -> bool:
        try:
            with Image.open(candidate.path) as image:
                width, height = image.size
                image.verify()
            return height > width and abs((width / height) - (9 / 16)) <= 0.02
        except Exception:
            return False
