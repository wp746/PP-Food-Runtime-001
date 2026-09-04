from pp_food_runtime.models.product import ProductLockBridge, ProductTruth
from pp_food_runtime.models.job import ImageRef
from pp_food_runtime.models.visual import (
    ArtDirection,
    CategoryVisualTranslation,
    CompositionDirection,
    ProductHeroDirection,
    TypographyDirection,
    ValidatedBPromptContract,
)
from pp_food_runtime.providers.base import ProviderCapabilityProfile
from pp_food_runtime.stage_b.compiler import compile_stage_b


def make_contract():
    ref = ImageRef(path="stage-a.png", sha256="a" * 64)
    truth = ProductTruth(
        source_sha256="b" * 64,
        identity_summary="visible citrus can",
        primary_category="CANNED_FRUIT_RETAIL",
        pack_or_food="PACK",
        visual_locks=["upright round can", "orange label"],
        sensory_keywords=["juicy", "citrus"],
    )
    bridge = ProductLockBridge(
        source_sha256="b" * 64,
        stage_a=ref,
        identity_locks=["upright round can"],
        surface_locks=["orange label"],
        topology_locks=["sealed can topology"],
    )
    translation = CategoryVisualTranslation(
        primary_category="CANNED_FRUIT_RETAIL",
        sensory_evidence=["juicy", "citrus"],
        emotional_semantics=["sunlit abundance"],
        brand_temperament=["mature retail confidence"],
        primary_material_metaphor="luminous citrus membranes",
        typography_translation="bold citrus-material Chinese letters",
        color_translation="orange, gold, green",
        lighting_translation="bright citrus halo",
        spatial_translation="multi-depth fruit orbit",
        motion_energy_translation="radiating arcs",
        information_system="pack then headline then support",
        one_big_idea_seed="can becomes a compact sun",
        forbidden_drift=["invented claims"],
    )
    direction = ArtDirection(
        concept_id="primary",
        one_big_idea="the can becomes a compact sun that powers a citrus headline",
        product_hero=ProductHeroDirection(
            scale="monumental", position="lower center", crop_behavior="controlled", dominance_strategy="sharp brightest first read"
        ),
        typography=TypographyDirection(
            exact_headline="桔子罐头", material_behavior="juicy citrus volume", spatial_behavior="upper middle interlock", product_relationship="letters orbit the current can"
        ),
        composition=CompositionDirection(
            dominant_axis="vertical", depth_architecture="foreground hero type rear", energy_direction="radiating", foreground_pressure="fruit edges"
        ),
        category_native_atmosphere="sunlit citrus retail world",
        color_direction="orange gold green",
        lighting_direction="retail hero light",
        information_system="exact brand support",
        forbidden_drift=["product drift"],
    )
    return ValidatedBPromptContract(
        truth=truth,
        bridge=bridge,
        translation=translation,
        direction=direction,
        exact_copy=["林家铺子", "桔子罐头"],
        golden_principles=["strong product and strong headline"],
        hard_negatives=["no invented hard facts"],
    )


def profile(text_rendering="strong"):
    return ProviderCapabilityProfile(
        provider_id="test", model_id="image", reference_edit=True, multiple_references=True,
        masks=False, seed=False, text_rendering=text_rendering, aspect_ratio=["9:16"], max_resolution="4k"
    )


def test_stage_b_prompt_uses_canonical_section_order():
    prompt = compile_stage_b(make_contract(), profile()).text
    headings = [
        "OUTPUT CONTRACT", "REFERENCE AUTHORITY", "PRODUCT IDENTITY LOCK",
        "PRODUCT SURFACE LOCK", "PACKAGE / VESSEL / TOPOLOGY LOCK",
        "CURRENT PRODUCT SEMANTICS", "ONE BIG IDEA", "PRODUCT HERO DIRECTION",
        "TYPOGRAPHY DIRECTION", "PRODUCT–TYPOGRAPHY RELATIONSHIP",
        "COMPOSITION / DEPTH", "CATEGORY-NATIVE ATMOSPHERE", "COLOR",
        "LIGHTING", "INFORMATION SYSTEM", "GOLDEN QUALITY TARGET",
        "HARD NEGATIVES", "FINAL CORE COMMAND",
    ]
    positions = [prompt.index(heading) for heading in headings]
    assert positions == sorted(positions)


def test_weak_text_profile_reserves_exact_copy_zones():
    prompt = compile_stage_b(make_contract(), profile("weak")).text
    assert "reserved typography-bearing structures" in prompt
    assert "林家铺子" in prompt and "桔子罐头" in prompt
