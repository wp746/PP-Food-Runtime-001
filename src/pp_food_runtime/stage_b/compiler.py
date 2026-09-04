from __future__ import annotations

import hashlib

from pp_food_runtime.models.visual import CompiledPrompt, ValidatedBPromptContract
from pp_food_runtime.providers.base import ProviderCapabilityProfile


def _join(values: list[str]) -> str:
    return "; ".join(dict.fromkeys(value.strip() for value in values if value.strip()))


def compile_stage_b(
    contract: ValidatedBPromptContract,
    profile: ProviderCapabilityProfile,
) -> CompiledPrompt:
    direction = contract.direction
    translation = contract.translation
    exact_copy = _join(contract.exact_copy)
    if profile.text_rendering.lower() == "strong":
        text_command = (
            f"Render only this exact authorized Chinese copy, character-for-character: {exact_copy}. "
            "Make the product name an aggressive, large campaign headline. Do not add, translate, paraphrase, "
            "duplicate, or corrupt any text."
        )
    else:
        text_command = (
            f"Build reserved typography-bearing structures for deterministic overlay. Preserve exact copy zones for: {exact_copy}. "
            "Do not hallucinate substitute lettering or any additional marks."
        )

    support_copy = _join(
        line for line in contract.exact_copy
        if line != direction.typography.exact_headline
    )
    sections = [
        (
            "B1 CURRENT STAGE A PRODUCT + HERO CAMERA LOCK",
            f"Create one finished edge-to-edge premium commercial KV, exact {contract.aspect_ratio}, high resolution, no border, mockup, split-screen, or process sheet. "
            "The attached current-job Stage A PASS is binding visual truth. PRODUCT_TRUTH=LOCKED. PRODUCT=HERO #1. "
            "Apparent product area may not shrink by more than 15 percent from Stage A; environment and headline may not become first read. "
            f"Identity: {_join(contract.bridge.identity_locks + contract.truth.visual_locks)}. Surface: {_join(contract.bridge.surface_locks)}. "
            f"Vessel/topology: {_join(contract.bridge.topology_locks)}.",
        ),
        (
            "B2 CURRENT CATEGORY SEMANTIC TRANSLATION",
            f"Category: {translation.primary_category}. Sensory evidence: {_join(translation.sensory_evidence)}. "
            f"Translate into palette/light/surface/rhythm/geometry rather than themed scenery: {translation.primary_material_metaphor}; "
            f"{translation.secondary_material_metaphor or ''}; color: {direction.color_direction}; lighting: {direction.lighting_direction}; "
            f"spatial behavior: {translation.spatial_translation}; motion: {translation.motion_energy_translation}. "
            f"Current-job mood only: {_join(translation.emotional_semantics + translation.brand_temperament)}.",
        ),
        (
            "B3 COPY TRUTH + INFORMATION HIERARCHY",
            f"Exact headline: {direction.typography.exact_headline}. Exact supporting lines, in supplied order: {support_copy}. {text_command} "
            "Hierarchy: product first; headline second; subtitle and slogan third; brand/store, selling points, address and phone as disciplined utility information. "
            "Use fewer support lines only if necessary for legibility, but every visible character must exactly match an authorized line. "
            "Do not add filler, pseudo-logos, QR codes, prices, opening hours, awards, certifications, weights, origins, ingredients, claims, or numbers.",
        ),
        (
            "B4 PRODUCT HERO + TYPOGRAPHY ROLE",
            f"One Big Idea: {direction.one_big_idea}. Product scale: {direction.product_hero.scale}; position: {direction.product_hero.position}; "
            f"crop: {direction.product_hero.crop_behavior}; dominance: {direction.product_hero.dominance_strategy}. "
            f"Typography material: {direction.typography.material_behavior}; spatial role: {direction.typography.spatial_behavior}; "
            f"product relationship: {direction.typography.product_relationship}. Typography has visible depth and design intention but never forces product shrinkage or menu-sign dominance.",
        ),
        (
            "B5 SELECTED COMPOSITION + CONTEMPORARY CAMPAIGN WORLD",
            f"Composition skeleton: {direction.composition.dominant_axis}. Depth: {direction.composition.depth_architecture}. "
            f"Energy: {direction.composition.energy_direction}. Foreground pressure: {direction.composition.foreground_pressure}. "
            f"Atmosphere: {direction.category_native_atmosphere}. Information system: {direction.information_system}. "
            f"Transfer abstract Golden principles only, never their skin: {_join(contract.golden_principles)}. "
            "Use designed negative space, controlled materials, selective scale contrast, tactile food clarity, one memorable product-led gesture, and contemporary advertising refinement.",
        ),
        (
            "B6 HARD NEGATIVES",
            _join(
                contract.hard_negatives
                + direction.forbidden_drift
                + translation.forbidden_drift
                + [
                    "no raw snapshot after Stage A PASS",
                    "no previous-job facts or skin",
                    "no product, package, vessel, count, plating, filling, surface, or cooking-state redesign",
                    "no unsupported hard facts",
                    "no product shrinkage beyond the hero-camera limit",
                    "no environment-first or headline-first composition",
                    "no giant portal, tunnel, arch, signboard, room, shelf, stall, or theatrical rustic set dominating product",
                    "no brown-on-brown overload",
                    "no menu-board or souvenir-sign aesthetic",
                    "no photo-plus-footer fallback",
                    "no top-title plus center-product plus bottom-info safe template",
                    "no material-swap pseudo-innovation",
                    "no rejected-candidate blending",
                ]
            )
            + ". Using only the attached current Stage A reference and this single compact finalist contract, render the decisive B candidate now.",
        ),
    ]
    text = "\n\n".join(f"## {heading}\n{body.strip()}" for heading, body in sections).strip() + "\n"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return CompiledPrompt(text=text, sha256=digest)
