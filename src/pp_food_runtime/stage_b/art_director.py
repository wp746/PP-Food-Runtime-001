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
        return self.select_finalists(
            self.create_candidates(truth, translation, copy, goldens)
        )

    def create_candidates(
        self,
        truth: ProductTruth,
        translation: CategoryVisualTranslation,
        copy: CopyAllowlist,
        goldens: list[GoldenPrinciplePack],
    ) -> tuple[ArtDirection, ArtDirection, ArtDirection]:
        headline = copy.product_name
        brand_line = copy.brand or ""
        golden_target = "; ".join(
            principle for pack in goldens[:2] for principle in pack.principles
        ) or "S-tier product/headline pressure, depth, and commercial finish"
        shared_forbidden = list(dict.fromkeys(translation.forbidden_drift + [
            "change product identity, geometry, label, vessel, count, or surface state",
            "reuse any old Golden brand, copy, palette, props, or exact layout",
            "flat 2D headline or subtitle pasted over the food photograph",
            "headline and supporting title sharing one flat plane with no perspective, overlap, occlusion, or depth separation",
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
                spatial_behavior=(
                    "headline occupies the upper-middle field as a scene-integrated spatial object: visible perspective, "
                    "material thickness or layered relief, shared scene light, and deliberate front/behind crossings; "
                    "supporting title sits on a distinct secondary depth plane rather than the same flat text layer"
                ),
                product_relationship=(
                    "letters emerge from, wrap, splash around, or are occluded by the current product's own material logic; "
                    "at least one product/type overlap must make the depth order visually undeniable"
                ),
            ),
            composition=CompositionDirection(
                dominant_axis="vertical surge",
                depth_architecture="foreground fragments, hero product, interlocked headline, secondary title plane, atmospheric rear plane",
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
                spatial_behavior=(
                    "headline travels diagonally through near/mid depth with foreshortened perspective, visible edge depth, "
                    "shared highlights/shadows, and deliberate occlusion; supporting title anchors a separate shallower or deeper plane"
                ),
                product_relationship="product interrupts the headline while material echoes reconnect the letterforms across depth",
            ),
            composition=CompositionDirection(
                dominant_axis="diagonal collision",
                depth_architecture="macro foreground crop, off-axis hero, crossing type ribbon, secondary title plane, compressed luminous background",
                energy_direction="lower-right to upper-left counterflow",
                foreground_pressure="one bold macro material arc crosses the near plane",
            ),
            category_native_atmosphere=translation.motion_energy_translation,
            color_direction=translation.color_translation,
            lighting_direction=f"more directional challenger variant; {translation.lighting_translation}",
            information_system=f"dense asymmetrical campaign lockup with exact brand {brand_line}; preserve hierarchy; target {golden_target}",
            forbidden_drift=shared_forbidden,
        )
        editorial = ArtDirection(
            concept_id="editorial",
            one_big_idea=f"Use disciplined negative space to make {headline} and one product-derived material gesture feel inevitable: {translation.primary_material_metaphor}",
            product_hero=ProductHeroDirection(
                scale="monumental and no more than 15 percent smaller in apparent area than Stage A",
                position="lower-left asymmetric hero crossing the center field",
                crop_behavior="retain all identity-critical product count and structure; only support-plane edges may crop",
                dominance_strategy=f"precise light and tactile separation keep {truth.identity_summary} as the nearest, largest, strongest first read",
            ),
            typography=TypographyDirection(
                exact_headline=headline,
                material_behavior=f"restrained dimensional interpretation: {translation.typography_translation}",
                spatial_behavior=(
                    "headline occupies shaped upper-right negative space but still has spatial evidence: perspective or layered plane offset, "
                    "controlled overlap into the hero plane, contact/cast shadow or shared light response; supporting title uses a distinct depth role"
                ),
                product_relationship="a single product-derived edge, highlight, or motion gesture bridges hero and type without turning type into signage",
            ),
            composition=CompositionDirection(
                dominant_axis="asymmetric editorial counterweight",
                depth_architecture="restrained foreground edge, monumental hero plane, spatial headline plane, secondary support plane, shallow atmospheric rear plane",
                energy_direction="contained lower-left to upper-right tension",
                foreground_pressure="one selective near-plane material accent; no prop pile or architecture",
            ),
            category_native_atmosphere=f"contemporary editorial restraint; {translation.spatial_translation}",
            color_direction=translation.color_translation,
            lighting_direction=f"precise restrained variant; {translation.lighting_translation}",
            information_system=f"headline and subtitle form one compact hierarchy with distinct depth roles; verified brand/contact facts use a clean side lockup; {translation.information_system}; target {golden_target}",
            forbidden_drift=shared_forbidden,
        )
        return primary, challenger, editorial

    @staticmethod
    def select_finalists(
        candidates: tuple[ArtDirection, ArtDirection, ArtDirection],
    ) -> tuple[ArtDirection, ArtDirection]:
        return candidates[0], candidates[2]
