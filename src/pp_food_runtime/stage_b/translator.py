from __future__ import annotations

from pp_food_runtime.models.job import UserFacts
from pp_food_runtime.models.product import ProductTruth
from pp_food_runtime.models.visual import CategoryVisualTranslation


class CategoryTranslator:
    def translate(self, truth: ProductTruth, user_facts: UserFacts) -> CategoryVisualTranslation:
        category = self._category(truth, user_facts)
        sensory = truth.sensory_keywords or self._default_sensory(category)
        if category == "BBQ_NIGHTMARKET":
            return CategoryVisualTranslation(
                primary_category=category,
                sensory_evidence=sensory,
                emotional_semantics=["handheld night-market immediacy", "toasted comfort", "braised-meat satisfaction"],
                brand_temperament=["streetwise", "warm", "confident", "contemporary"],
                primary_material_metaphor="golden seared flatbread crust meeting lacquered braised-meat gloss",
                secondary_material_metaphor="pepper-green sparks and narrow ribbons of night heat",
                typography_translation="bold Chinese display type with toasted bread relief, restrained charred edges, and braised-juice highlights; premium night-market energy without a rustic signboard",
                color_translation="wheat gold, braised amber, pepper green, smoky blue-black, and one restrained vermilion night accent",
                lighting_translation="fire-side warm raking key across bread and meat, balanced by a cool night rim and controlled steam backlight",
                spatial_translation="five-product hero cluster stays nearest and largest; diagonal counter pressure, shallow luminous night depth, and no literal stall interior",
                motion_energy_translation="crust-flake rhythm and narrow rising heat arcs drive the eye back into the exposed meat filling",
                information_system="product first, dimensional headline second, then subtitle and a compact verified shop/contact stack with disciplined selling-point cadence",
                one_big_idea_seed="five meat-filled flatbreads become a single hot handheld rhythm, where toasted bread geometry and braised gloss construct a contemporary night-advertising field",
                forbidden_drift=[
                    "generic black-gold restaurant poster",
                    "giant rustic signboard or menu board",
                    "literal street-stall diorama",
                    "fire or smoke hiding the food",
                    "single burger replacing five flatbreads",
                    "western burger or sandwich styling",
                    "photo plus footer",
                ],
            )
        if category == "COLD_DRINK_FRUIT_DESSERT":
            return CategoryVisualTranslation(
                primary_category=category,
                sensory_evidence=sensory,
                emotional_semantics=["instant cooling relief", "young summer delight", "juicy abundance"],
                brand_temperament=["playful", "fresh", "confident local favorite"],
                primary_material_metaphor="frosted watermelon translucency with visible condensation",
                secondary_material_metaphor="soft coconut-milk ribbons and crystalline crushed ice",
                typography_translation="oversized Chinese headline built from chilled fruit translucency and creamy coconut layers",
                color_translation="watermelon red, rind green, coconut white, and cool aqua with high edible contrast",
                lighting_translation="hard summer key light through cold translucent material plus wet specular highlights",
                spatial_translation="monumental cup and headline interlock across foreground, hero plane, and splash depth",
                motion_energy_translation="upward cooling burst, suspended fruit and ice arcs, controlled droplets",
                information_system="product and headline are equal first-read anchors; brand and verified facts form compact support",
                one_big_idea_seed="the product becomes a physical cooling burst whose watermelon-and-coconut material also constructs the headline",
                forbidden_drift=[
                    "generic tropical beach postcard",
                    "tiny product beneath decorative scenery",
                    "flat product photo with detached text",
                    "unsupported ingredient or health claims",
                ],
            )
        if category == "CANNED_FRUIT_RETAIL":
            return CategoryVisualTranslation(
                primary_category=category,
                sensory_evidence=sensory,
                emotional_semantics=["sunlit sweetness", "trustworthy abundance", "retail shelf confidence"],
                brand_temperament=["mature", "generous", "conversion-focused"],
                primary_material_metaphor="luminous citrus segments, syrup gloss, and fine orange membranes",
                secondary_material_metaphor="sun-disc radiance shaped by the round can geometry",
                typography_translation="bold Chinese headline with juicy citrus volume, syrup highlights, and can-label precision",
                color_translation="saturated tangerine, sun gold, leaf green, and clean warm cream with strong pack contrast",
                lighting_translation="directional retail hero light with a bright citrus halo and controlled metal-can highlights",
                spatial_translation="oversized pack hero, fruit orbit, headline bridge, and dense but tiered retail information planes",
                motion_energy_translation="radiating citrus arcs around a stable upright pack anchor",
                information_system="pack and headline dominate; brand, safe campaign line, and verified facts lock into structured badges",
                one_big_idea_seed="the can acts as a compact sun while real citrus material radiates outward and powers the headline",
                forbidden_drift=[
                    "generic luxury pedestal unrelated to citrus",
                    "tiny package in a large empty editorial field",
                    "flat packshot plus floating text",
                    "invented weight, origin, award, certification, or nutrition claim",
                ],
            )
        if category == "BAKERY":
            return CategoryVisualTranslation(
                primary_category=category,
                sensory_evidence=sensory,
                emotional_semantics=["warm chew", "toasted satisfaction", "tactile freshness"],
                brand_temperament=["crafted", "direct", "contemporary"],
                primary_material_metaphor="taut browned crust and elastic crumb tension",
                secondary_material_metaphor="fine salt-like mineral glints",
                typography_translation="bold letterforms shaped by the product's ring tension and smooth browned surface",
                color_translation="baked umber, wheat cream, mineral white, and a sharp contemporary accent",
                lighting_translation="raking light that reveals crust tension without nostalgic sepia styling",
                spatial_translation="large product geometry intersects typography across multiple controlled depth planes",
                motion_energy_translation="ring-shaped orbital tension and taut directional pull",
                information_system="product and headline dominate with restrained verified support copy",
                one_big_idea_seed="the product's taut ring geometry becomes the spatial force that bends the campaign headline around it",
                forbidden_drift=[
                    "literal rustic bakery scenery",
                    "nostalgic craft props replacing product meaning",
                    "tiny product under decorative architecture",
                    "generic black-gold premium skin",
                ],
            )
        return CategoryVisualTranslation(
            primary_category=category,
            sensory_evidence=sensory,
            emotional_semantics=["immediate appetite", "confident product desire"],
            brand_temperament=["direct", "product-led", "campaign-ready"],
            primary_material_metaphor="visible current-product surface and ingredient material",
            typography_translation="headline material derived from the current product surface and geometry",
            color_translation="current-product-derived palette with strong edible contrast",
            lighting_translation="product-revealing commercial key light with tactile highlights",
            spatial_translation="product-headline co-composition across at least three depth planes",
            motion_energy_translation="energy direction derived from current product geometry",
            information_system="product then headline then one supporting message",
            one_big_idea_seed="the current product's own visible material becomes the force that constructs the campaign world",
            forbidden_drift=["generic premium skin", "category costume", "photo plus detached text", "unsupported claims"],
        )

    @staticmethod
    def _category(truth: ProductTruth, user_facts: UserFacts) -> str:
        name = user_facts.product_name
        if any(word in name for word in ("西瓜冰", "冰饮", "果茶")):
            return "COLD_DRINK_FRUIT_DESSERT"
        if any(word in name for word in ("罐头", "蜜橘", "桔子")) and truth.pack_or_food == "PACK":
            return "CANNED_FRUIT_RETAIL"
        if any(word in name for word in ("贝果", "面包", "吐司")):
            return "BAKERY"
        if any(word in name for word in ("肉夹馍", "夹馍", "夜市", "白吉馍")):
            return "BBQ_NIGHTMARKET"
        return truth.primary_category

    @staticmethod
    def _default_sensory(category: str) -> list[str]:
        return {
            "COLD_DRINK_FRUIT_DESSERT": ["cold", "juicy", "crisp", "creamy"],
            "CANNED_FRUIT_RETAIL": ["juicy", "sweet", "citrus", "abundant"],
            "BAKERY": ["chewy", "toasted", "wheat", "tactile"],
            "BBQ_NIGHTMARKET": ["toasted", "savory", "juicy", "hot", "handheld"],
        }.get(category, ["appetizing", "tactile"])
