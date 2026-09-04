from __future__ import annotations

from pp_food_runtime.models.product import ProductTruth
from pp_food_runtime.models.visual import (
    ArtDirection,
    CategoryVisualTranslation,
    CompositionDirection,
    GoldenPrinciplePack,
    ProductHeroDirection,
    TypographyDirection,
)

from .copy_firewall import CopyAllowlist


class BArtDirector:
    def create_directions(
        self,
        truth: ProductTruth,
        translation: CategoryVisualTranslation,
        copy: CopyAllowlist,
        goldens: list[GoldenPrinciplePack],
    ) -> tuple[ArtDirection, ArtDirection]:
        headline = copy.product_name
        brand_line = copy.brand or ""
        golden_target = "; ".join(
            principle for pack in goldens[:2] for principle in pack.principles
        ) or "S-tier product/headline pressure, depth, and commercial finish"
        shared_forbidden = list(dict.fromkeys(translation.forbidden_drift + [
            "change product identity, geometry, label, vessel, count, or surface state",
            "reuse any old Golden brand, copy, palette, props, or exact layout",
        ]))

        primary = ArtDirection(
            concept_id="primary",
            one_big_idea=f"{translation.one_big_idea_seed}; make {headline} inseparable from that physical event",
            product_hero=ProductHeroDirection(
                scale="monumental, roughly half the usable poster height",
                position="lower-center pushing into the headline plane",
                crop_behavior="confident edge pressure without cutting identity-critical features",
                dominance_strategy=f"{truth.identity_summary} remains the brightest, sharpest, most dimensional first read",
            ),
            typography=TypographyDirection(
                exact_headline=headline,
                material_behavior=translation.typography_translation,
                spatial_behavior="headline occupies the upper-middle field and physically interlocks with product material",
                product_relationship="letters emerge from, wrap, splash around, or are occluded by the current product's own material logic",
            ),
            composition=CompositionDirection(
                dominant_axis="vertical surge",
                depth_architecture="foreground fragments, hero product, interlocked headline, atmospheric rear plane",
                energy_direction="upward and outward from the product core",
                foreground_pressure="controlled large foreground accents enter two edges",
            ),
            category_native_atmosphere=translation.spatial_translation,
            color_direction=translation.color_translation,
            lighting_direction=translation.lighting_translation,
            information_system=f"{translation.information_system}; exact brand support: {brand_line}; Golden pressure target: {golden_target}",
            forbidden_drift=shared_forbidden,
        )
        challenger = ArtDirection(
            concept_id="challenger",
            one_big_idea=f"Turn {headline} and the product into one diagonal material collision: {translation.primary_material_metaphor}",
            product_hero=ProductHeroDirection(
                scale="extreme close hero with full identity still legible",
                position="right-lower third crossing the center axis",
                crop_behavior="dynamic partial edge crop allowed only outside identity-critical structure",
                dominance_strategy=f"use raking light and sharp tactile detail so {truth.identity_summary} beats every scene element",
            ),
            typography=TypographyDirection(
                exact_headline=headline,
                material_behavior=translation.typography_translation,
                spatial_behavior="headline travels diagonally behind and in front of the hero with deliberate occlusion",
                product_relationship="product interrupts the headline while material echoes reconnect the letterforms across depth",
            ),
            composition=CompositionDirection(
                dominant_axis="diagonal collision",
                depth_architecture="macro foreground crop, off-axis hero, crossing type ribbon, compressed luminous background",
                energy_direction="lower-right to upper-left counterflow",
                foreground_pressure="one bold macro material arc crosses the near plane",
            ),
            category_native_atmosphere=translation.motion_energy_translation,
            color_direction=translation.color_translation,
            lighting_direction=f"more directional challenger variant; {translation.lighting_translation}",
            information_system=f"dense asymmetrical campaign lockup with exact brand {brand_line}; preserve hierarchy; target {golden_target}",
            forbidden_drift=shared_forbidden,
        )
        return primary, challenger
