from __future__ import annotations

from enum import StrEnum

from pydantic import Field, computed_field, model_validator

from .common import FrozenModel


class FailureCode(StrEnum):
    PRODUCT_IDENTITY_DRIFT = "PRODUCT_IDENTITY_DRIFT"
    COPY_TRUTH_FAILURE = "COPY_TRUTH_FAILURE"
    MECHANICAL_FAILURE = "MECHANICAL_FAILURE"
    SAFE_EDITORIAL_COLLAPSE = "SAFE_EDITORIAL_COLLAPSE"
    SCENE_DOMINATES_PRODUCT = "SCENE_DOMINATES_PRODUCT"
    CATEGORY_CLICHE_DEPENDENCE = "CATEGORY_CLICHE_DEPENDENCE"
    GENERIC_PREMIUM_SKIN = "GENERIC_PREMIUM_SKIN"
    TEMPLATE_REUSE = "TEMPLATE_REUSE"
    PHOTO_PLUS_TEXT = "PHOTO_PLUS_TEXT"
    INFORMATION_STARVATION = "INFORMATION_STARVATION"
    INFORMATION_OVERLOAD = "INFORMATION_OVERLOAD"
    HERO_WEAK = "HERO_WEAK"
    HEADLINE_WEAK = "HEADLINE_WEAK"
    TYPOGRAPHY_DISCONNECTED = "TYPOGRAPHY_DISCONNECTED"
    BIG_IDEA_WEAK = "BIG_IDEA_WEAK"
    COMPOSITION_FLAT = "COMPOSITION_FLAT"
    CATEGORY_WEAK = "CATEGORY_WEAK"
    COMMERCIAL_FINISH_WEAK = "COMMERCIAL_FINISH_WEAK"
    GOLDEN_DISTANCE = "GOLDEN_DISTANCE"
    REFERENCE_BINDING_FAILURE = "REFERENCE_BINDING_FAILURE"
    EVALUATOR_FAILURE = "EVALUATOR_FAILURE"


class FinalDecision(StrEnum):
    PASS = "PASS"
    RETRY = "RETRY"
    NO_QUALIFIED_WINNER = "NO_QUALIFIED_WINNER"
    NEEDS_SECOND_EVALUATION = "NEEDS_SECOND_EVALUATION"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


class GoldenVector(FrozenModel):
    product_hero_strength: float = Field(ge=0, le=10)
    headline_aggression: float = Field(ge=0, le=10)
    typography_product_symbiosis: float = Field(ge=0, le=10)
    one_big_idea_clarity: float = Field(ge=0, le=10)
    compositional_depth_tension: float = Field(ge=0, le=10)
    category_inevitability: float = Field(ge=0, le=10)
    information_density_control: float = Field(ge=0, le=10)
    commercial_finish: float = Field(ge=0, le=10)

    @classmethod
    def all_at(cls, value: float) -> "GoldenVector":
        return cls(**{name: value for name in cls.model_fields})

    @computed_field
    @property
    def weighted_score(self) -> float:
        weights = {
            "product_hero_strength": 0.18,
            "headline_aggression": 0.14,
            "typography_product_symbiosis": 0.14,
            "one_big_idea_clarity": 0.12,
            "compositional_depth_tension": 0.14,
            "category_inevitability": 0.10,
            "information_density_control": 0.08,
            "commercial_finish": 0.10,
        }
        return round(sum(getattr(self, key) * weight for key, weight in weights.items()), 3)


class VisibleEvidence(FrozenModel):
    dimension: str
    what_is_visible: str
    where_visible: str
    why_it_helps_or_hurts: str


class EvaluationResult(FrozenModel):
    candidate_id: str
    mechanical_pass: bool
    product_truth_pass: bool
    copy_truth_pass: bool
    golden_vector: GoldenVector
    critical_failures: list[FailureCode] = Field(default_factory=list)
    materially_weaker_core_dimensions: list[str] = Field(default_factory=list)
    evidence: list[VisibleEvidence] = Field(default_factory=list)
    pairwise_winner: str | None = None
    final_decision: FinalDecision
    confidence: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def prevent_false_pass(self) -> "EvaluationResult":
        if self.final_decision is FinalDecision.PASS and (
            not self.mechanical_pass
            or not self.product_truth_pass
            or not self.copy_truth_pass
            or self.critical_failures
        ):
            raise ValueError("hard failures cannot be compensated by scores")
        return self


class PassFreezeMap(FrozenModel):
    passing_dimensions: list[str] = Field(default_factory=list)
    failing_dimensions: list[str] = Field(default_factory=list)
