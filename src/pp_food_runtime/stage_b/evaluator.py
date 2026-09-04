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
    "product_hero_strength": 9.0,
    "headline_aggression": 8.8,
    "typography_product_symbiosis": 8.5,
    "one_big_idea_clarity": 8.3,
    "compositional_depth_tension": 8.8,
    "category_inevitability": 8.5,
    "information_density_control": 7.8,
    "commercial_finish": 9.0,
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

    @staticmethod
    def _mechanical_pass(candidate: ImageRef) -> bool:
        try:
            with Image.open(candidate.path) as image:
                width, height = image.size
                image.verify()
            return height > width and abs((width / height) - (9 / 16)) <= 0.02
        except Exception:
            return False

