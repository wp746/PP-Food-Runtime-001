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

    sections = [
        (
            "OUTPUT CONTRACT",
            f"One finished premium commercial key visual, exact {contract.aspect_ratio} portrait composition, high resolution, "
            "edge-to-edge campaign artwork, no border, no mockup, no split-screen, no design-process sheet.",
        ),
        (
            "REFERENCE AUTHORITY",
            "The attached current-job Stage A PASS is the binding product reference, not loose inspiration. Preserve its product DNA. "
            "You may creatively reframe scale, crop, position, overlap, and camera for Stage B; do not lock its old camera composition.",
        ),
        ("PRODUCT IDENTITY LOCK", _join(contract.bridge.identity_locks + contract.truth.visual_locks)),
        ("PRODUCT SURFACE LOCK", _join(contract.bridge.surface_locks)),
        ("PACKAGE / VESSEL / TOPOLOGY LOCK", _join(contract.bridge.topology_locks)),
        (
            "CURRENT PRODUCT SEMANTICS",
            f"Identity: {contract.truth.identity_summary}. Sensory evidence: {_join(translation.sensory_evidence)}. "
            f"Emotional semantics: {_join(translation.emotional_semantics)}. Brand temperament: {_join(translation.brand_temperament)}.",
        ),
        ("ONE BIG IDEA", direction.one_big_idea),
        (
            "PRODUCT HERO DIRECTION",
            f"Scale: {direction.product_hero.scale}. Position: {direction.product_hero.position}. "
            f"Crop: {direction.product_hero.crop_behavior}. Dominance: {direction.product_hero.dominance_strategy}. "
            "The product must be the unmistakable first read and remain more visually powerful than the environment.",
        ),
        (
            "TYPOGRAPHY DIRECTION",
            f"Headline: {direction.typography.exact_headline}. Material behavior: {direction.typography.material_behavior}. "
            f"Spatial behavior: {direction.typography.spatial_behavior}. {text_command}",
        ),
        ("PRODUCT–TYPOGRAPHY RELATIONSHIP", direction.typography.product_relationship),
        (
            "COMPOSITION / DEPTH",
            f"Axis: {direction.composition.dominant_axis}. Depth: {direction.composition.depth_architecture}. "
            f"Energy: {direction.composition.energy_direction}. Foreground pressure: {direction.composition.foreground_pressure}. "
            "Use clear foreground, hero, headline, and atmospheric planes with controlled tension.",
        ),
        (
            "CATEGORY-NATIVE ATMOSPHERE",
            f"{direction.category_native_atmosphere}. Spatial translation: {translation.spatial_translation}. "
            f"Motion translation: {translation.motion_energy_translation}.",
        ),
        ("COLOR", direction.color_direction),
        ("LIGHTING", direction.lighting_direction),
        (
            "INFORMATION SYSTEM",
            f"{direction.information_system}. Use only authorized copy: {exact_copy}. "
            "Keep density energetic but legible; no invented facts, badges, numbers, awards, certifications, prices, weights, or origins.",
        ),
        (
            "GOLDEN QUALITY TARGET",
            f"Transfer principles only, never skin: {_join(contract.golden_principles)}. Match S-tier visual pressure through "
            "extreme product hero, strong headline aggression, product-derived typography, one clear product-derived idea, "
            "multi-depth co-composition, category inevitability, controlled information density, and campaign-grade finish.",
        ),
        (
            "HARD NEGATIVES",
            _join(
                contract.hard_negatives
                + direction.forbidden_drift
                + translation.forbidden_drift
                + [
                    "no product identity drift",
                    "no scene dominance",
                    "no safe editorial collapse or giant empty space",
                    "no generic premium skin",
                    "no flat photo plus detached text",
                    "no template reuse",
                ]
            ),
        ),
        (
            "FINAL CORE COMMAND",
            "Using the attached Stage A reference, create one decisive campaign-grade B visual now. Protect product truth and exact copy, "
            "then maximize visible product-headline symbiosis, compositional depth, sensory material logic, and commercial finish.",
        ),
    ]
    text = "\n\n".join(f"## {heading}\n{body.strip()}" for heading, body in sections).strip() + "\n"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return CompiledPrompt(text=text, sha256=digest)
