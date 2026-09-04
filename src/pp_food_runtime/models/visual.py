from __future__ import annotations

from pydantic import Field, model_validator

from .common import FrozenModel
from .product import ProductLockBridge, ProductTruth


class ProductHeroDirection(FrozenModel):
    scale: str
    position: str
    crop_behavior: str
    dominance_strategy: str


class TypographyDirection(FrozenModel):
    exact_headline: str
    material_behavior: str
    spatial_behavior: str
    product_relationship: str


class CompositionDirection(FrozenModel):
    dominant_axis: str
    depth_architecture: str
    energy_direction: str
    foreground_pressure: str


class CategoryVisualTranslation(FrozenModel):
    primary_category: str
    sensory_evidence: list[str]
    emotional_semantics: list[str]
    brand_temperament: list[str]
    primary_material_metaphor: str
    secondary_material_metaphor: str | None = None
    typography_translation: str
    color_translation: str
    lighting_translation: str
    spatial_translation: str
    motion_energy_translation: str
    information_system: str
    one_big_idea_seed: str
    forbidden_drift: list[str]


class ArtDirection(FrozenModel):
    concept_id: str
    one_big_idea: str = Field(min_length=12)
    product_hero: ProductHeroDirection
    typography: TypographyDirection
    composition: CompositionDirection
    category_native_atmosphere: str = Field(min_length=8)
    color_direction: str
    lighting_direction: str
    information_system: str
    forbidden_drift: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_traceability(self) -> "ArtDirection":
        joined = " ".join(
            [
                self.one_big_idea,
                self.product_hero.dominance_strategy,
                self.typography.material_behavior,
                self.typography.product_relationship,
            ]
        ).strip()
        if len(joined) < 40:
            raise ValueError("art direction lacks product traceability")
        return self


class GoldenPrinciplePack(FrozenModel):
    golden_id: str
    tier: str
    principles: list[str]
    prohibited_transfer: list[str]
    local_asset_path: str | None = None
    local_asset_sha256: str | None = None


class ValidatedBPromptContract(FrozenModel):
    truth: ProductTruth
    bridge: ProductLockBridge
    translation: CategoryVisualTranslation
    direction: ArtDirection
    exact_copy: list[str]
    golden_principles: list[str]
    hard_negatives: list[str]
    aspect_ratio: str = "9:16"


class CompiledPrompt(FrozenModel):
    text: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

