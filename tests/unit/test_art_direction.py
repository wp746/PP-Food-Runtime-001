from pp_food_runtime.models.job import UserFacts
from pp_food_runtime.models.product import ProductTruth
from pp_food_runtime.stage_b.art_director import BArtDirector
from pp_food_runtime.stage_b.copy_firewall import CopyFirewall
from pp_food_runtime.stage_b.translator import CategoryTranslator


def _truth(category="BAKERY"):
    return ProductTruth(
        source_sha256="a" * 64,
        identity_summary="single glossy original alkaline bagel",
        primary_category=category,
        pack_or_food="FOOD",
        sensory_keywords=["chewy", "toasted", "wheat"],
        visual_locks=["single ring", "smooth brown crust"],
    )


def test_bakery_translation_does_not_force_oven_or_wood_sign():
    result = CategoryTranslator().translate(_truth(), UserFacts(product_name="碱水原味贝果"))
    joined = " ".join(result.forbidden_drift + [result.one_big_idea_seed])
    assert "oven tunnel" not in joined.lower()
    assert "wooden sign" not in joined.lower()


def test_primary_and_challenger_differ_in_two_structural_dimensions():
    truth = _truth("COLD_DRINK_FRUIT_DESSERT")
    facts = UserFacts(product_name="椰椰西瓜冰", brand="有幸小食院", default_copy_authorized=True)
    translation = CategoryTranslator().translate(truth, facts)
    copy = CopyFirewall().build(facts)
    primary, challenger = BArtDirector().create_directions(truth, translation, copy, [])
    differences = sum(
        [
            primary.composition.dominant_axis != challenger.composition.dominant_axis,
            primary.typography.spatial_behavior != challenger.typography.spatial_behavior,
            primary.product_hero.position != challenger.product_hero.position,
            primary.composition.depth_architecture != challenger.composition.depth_architecture,
        ]
    )
    assert differences >= 2


def test_directions_trace_current_product_and_not_old_golden_skin():
    truth = _truth("CANNED_FRUIT_RETAIL")
    facts = UserFacts(product_name="桔子罐头", brand="林家铺子")
    translation = CategoryTranslator().translate(truth, facts)
    primary, _ = BArtDirector().create_directions(
        truth, translation, CopyFirewall().build(facts), []
    )
    serialized = primary.model_dump_json()
    assert "桔子罐头" in serialized
    assert "林家铺子" in serialized
    assert "有幸小食院" not in serialized
