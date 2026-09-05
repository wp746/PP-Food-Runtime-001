from __future__ import annotations

import json

from PIL import Image
from pydantic import Field

from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.job import ImageRef
from pp_food_runtime.models.product import ProductTruth, StageAQCEvaluation
from pp_food_runtime.providers.base import VisionProvider


FIDELITY_FLOORS = {
    "product_identity_score": 9.5,
    "geometry_count_score": 9.5,
    "ingredient_topology_score": 9.5,
    "plating_arrangement_score": 9.5,
    "physical_relationships_score": 9.5,
    "surface_state_score": 9.5,
    "vessel_package_score": 9.8,
    "commercial_photography_score": 8.5,
    "semantic_relevance_score": 8.5,
    "hero_spatial_score": 8.5,
    "appetite_score": 8.5,
}


class RawStageAEvaluation(FrozenModel):
    product_identity_score: float = Field(ge=0, le=10)
    geometry_count_score: float = Field(ge=0, le=10)
    ingredient_topology_score: float = Field(ge=0, le=10)
    plating_arrangement_score: float = Field(ge=0, le=10)
    physical_relationships_score: float = Field(ge=0, le=10)
    surface_state_score: float = Field(ge=0, le=10)
    vessel_package_score: float = Field(ge=0, le=10)
    commercial_photography_score: float = Field(ge=0, le=10)
    semantic_relevance_score: float = Field(ge=0, le=10)
    hero_spatial_score: float = Field(ge=0, le=10)
    appetite_score: float = Field(ge=0, le=10)
    critical_drifts: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


STAGE_A_EVALUATOR_INSTRUCTION = """
Act as a strict forensic Stage A food/product fidelity inspector. You receive two images in order: the original
source and the generated Stage A candidate. Judge visible pixels, never the generation prompt. Stage A is a
clean 9:16 commercial photograph, not a poster: it must contain no added headline, promotion, logo, badge, QR,
price, phone, address, decorative fake packaging text, or invented ingredient.

Score each independent dimension from 0 to 10: exact product identity; geometry and count; ingredient/package
topology; plating/arrangement; physical relationships; surface/material/cooking state; vessel or package fidelity;
commercial-photography quality; semantic relevance; hero spatial strength; and appetite. For a
dimension not applicable to a loose food, judge preservation of its closest visible supporting structure rather
than penalizing absence. Product identity outranks styling. Changed food type, changed major ingredient, changed
count, changed package/vessel, invented topping, removed identity-critical component, human/hand, or readable
invented text is a critical drift. Crop and camera may improve, but every identity-critical visible relationship
must remain recognizable. Return concise strict JSON with concrete visible evidence only.
""".strip()


def decide_stage_a_qc(
    *,
    candidate_id: str,
    mechanical_pass: bool,
    reference_binding_verified: bool,
    raw: RawStageAEvaluation,
) -> StageAQCEvaluation:
    failed = [
        name for name, floor in FIDELITY_FLOORS.items()
        if float(getattr(raw, name)) < floor
    ]
    passed = (
        mechanical_pass
        and reference_binding_verified
        and raw.confidence >= 0.70
        and not raw.critical_drifts
        and not failed
        and bool(raw.evidence)
    )
    return StageAQCEvaluation(
        candidate_id=candidate_id,
        status="PASS" if passed else "RETRY",
        mechanical_pass=mechanical_pass,
        reference_binding_verified=reference_binding_verified,
        failed_dimensions=failed,
        **raw.model_dump(),
    )


class StageAEvaluator:
    def __init__(self, provider: VisionProvider):
        self.provider = provider

    def evaluate(
        self,
        *,
        candidate_id: str,
        source: ImageRef,
        candidate: ImageRef,
        truth: ProductTruth,
    ) -> StageAQCEvaluation:
        payload = {
            "product_truth": truth.model_dump(mode="json"),
            "fidelity_floors": FIDELITY_FLOORS,
        }
        instruction = (
            f"{STAGE_A_EVALUATOR_INSTRUCTION}\nEvaluation context:\n"
            f"{json.dumps(payload, ensure_ascii=False, sort_keys=True)}"
        )
        raw = self.provider.analyze([source, candidate], instruction, RawStageAEvaluation)
        return decide_stage_a_qc(
            candidate_id=candidate_id,
            mechanical_pass=self._mechanical_pass(candidate),
            reference_binding_verified=candidate.reference_binding_verified,
            raw=raw,
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
