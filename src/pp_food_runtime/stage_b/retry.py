from __future__ import annotations

from enum import StrEnum

from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.evaluation import (
    EvaluationResult,
    FailureCode,
    FinalDecision,
    PassFreezeMap,
)

from .evaluator import FLOORS


class RetryFamily(StrEnum):
    FIDELITY_RETRY = "FIDELITY_RETRY"
    HERO_RETRY = "HERO_RETRY"
    HEADLINE_PRESSURE_RETRY = "HEADLINE_PRESSURE_RETRY"
    TYPOGRAPHY_SYMBIOSIS_RETRY = "TYPOGRAPHY_SYMBIOSIS_RETRY"
    BIG_IDEA_RETRY = "BIG_IDEA_RETRY"
    COMPOSITION_RETRY = "COMPOSITION_RETRY"
    CATEGORY_TRANSLATION_RETRY = "CATEGORY_TRANSLATION_RETRY"
    INFORMATION_RETRY = "INFORMATION_RETRY"
    COMMERCIAL_FINISH_RETRY = "COMMERCIAL_FINISH_RETRY"
    GOLDEN_DISTANCE_RETRY = "GOLDEN_DISTANCE_RETRY"


class RetryLevel(StrEnum):
    TARGETED_REPAIR = "TARGETED_REPAIR"
    CONCEPT_ADJUSTMENT = "CONCEPT_ADJUSTMENT"
    ART_DIRECTION_REBUILD = "ART_DIRECTION_REBUILD"


class RetryPlan(FrozenModel):
    family: RetryFamily
    level: RetryLevel
    failure_codes: list[FailureCode]
    pass_freeze: PassFreezeMap
    repair_instruction: str
    final_decision: FinalDecision = FinalDecision.RETRY


MAPPING = {
    FailureCode.PRODUCT_IDENTITY_DRIFT: RetryFamily.FIDELITY_RETRY,
    FailureCode.REFERENCE_BINDING_FAILURE: RetryFamily.FIDELITY_RETRY,
    FailureCode.SCENE_DOMINATES_PRODUCT: RetryFamily.HERO_RETRY,
    FailureCode.HERO_WEAK: RetryFamily.HERO_RETRY,
    FailureCode.HEADLINE_WEAK: RetryFamily.HEADLINE_PRESSURE_RETRY,
    FailureCode.TYPOGRAPHY_DISCONNECTED: RetryFamily.TYPOGRAPHY_SYMBIOSIS_RETRY,
    FailureCode.BIG_IDEA_WEAK: RetryFamily.BIG_IDEA_RETRY,
    FailureCode.COMPOSITION_FLAT: RetryFamily.COMPOSITION_RETRY,
    FailureCode.SAFE_EDITORIAL_COLLAPSE: RetryFamily.COMPOSITION_RETRY,
    FailureCode.CATEGORY_CLICHE_DEPENDENCE: RetryFamily.CATEGORY_TRANSLATION_RETRY,
    FailureCode.CATEGORY_WEAK: RetryFamily.CATEGORY_TRANSLATION_RETRY,
    FailureCode.GENERIC_PREMIUM_SKIN: RetryFamily.CATEGORY_TRANSLATION_RETRY,
    FailureCode.INFORMATION_STARVATION: RetryFamily.INFORMATION_RETRY,
    FailureCode.INFORMATION_OVERLOAD: RetryFamily.INFORMATION_RETRY,
    FailureCode.COPY_TRUTH_FAILURE: RetryFamily.INFORMATION_RETRY,
    FailureCode.COMMERCIAL_FINISH_WEAK: RetryFamily.COMMERCIAL_FINISH_RETRY,
    FailureCode.PHOTO_PLUS_TEXT: RetryFamily.TYPOGRAPHY_SYMBIOSIS_RETRY,
    FailureCode.TEMPLATE_REUSE: RetryFamily.GOLDEN_DISTANCE_RETRY,
    FailureCode.GOLDEN_DISTANCE: RetryFamily.GOLDEN_DISTANCE_RETRY,
    FailureCode.MECHANICAL_FAILURE: RetryFamily.FIDELITY_RETRY,
}


class RetryPlanner:
    def plan(self, result: EvaluationResult, cycle: int) -> RetryPlan:
        codes = result.critical_failures or [FailureCode.GOLDEN_DISTANCE]
        family = MAPPING.get(codes[0], RetryFamily.GOLDEN_DISTANCE_RETRY)
        level = {
            1: RetryLevel.TARGETED_REPAIR,
            2: RetryLevel.CONCEPT_ADJUSTMENT,
            3: RetryLevel.ART_DIRECTION_REBUILD,
        }.get(cycle, RetryLevel.ART_DIRECTION_REBUILD)
        passing, failing = [], []
        for field, floor in FLOORS.items():
            (passing if getattr(result.golden_vector, field) >= floor else failing).append(field)
        final = FinalDecision.NEEDS_HUMAN_REVIEW if cycle > 3 else FinalDecision.RETRY
        return RetryPlan(
            family=family,
            level=level,
            failure_codes=codes,
            pass_freeze=PassFreezeMap(passing_dimensions=passing, failing_dimensions=failing),
            repair_instruction=(
                f"Apply {family.value} at {level.value}. Preserve these already passing dimensions: "
                f"{', '.join(passing) or 'none'}. Repair only: {', '.join(failing) or ', '.join(code.value for code in codes)}."
            ),
            final_decision=final,
        )
