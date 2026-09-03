# B KV Visual Director

Purpose: turn the current Stage A PASS image into a category-native campaign world with a memorable product-led idea. The director protects hard truths, explores creative alternatives, and selects one strong composition before prompt compilation.

This file is production-critical for B.

## 1. Mandatory Pipeline

```text
CURRENT_JOB_STAGE_A_PASS_IMAGE
→ CURRENT PRODUCT SEMANTICS
→ B_KV_VISUAL_DIRECTOR
→ B_KV_CREATIVE_BOARD (3 candidates)
→ SELECT 1 WINNER
→ B_CONTRACT
→ B_PROMPT_COMPILER
→ IMAGE_MODEL
→ B_QC
```

Skipping the director or candidate board is a B critical failure.

## 2. Hard Bottom-Line Constraints

These are non-negotiable:

```text
PRODUCT_FIDELITY = LOCKED
PRODUCT_PRIORITY = 1
HEADLINE_PRIORITY = 2
COPY_TRUTH = EXACT
CURRENT_JOB_ONLY = TRUE
PREVIOUS_SKIN_IMPORT = OFF
EXACT_9_16 = TRUE
```

Creative ambition must never redesign, re-cook, re-plate, re-package, shrink, demote or obscure the product.

## 3. Current Product Reading

Use only current-job evidence:

```text
Stage A PASS image
user-provided product/dish name
user-provided brand/store information
current COPY_ALLOWLIST
selected current category profile
reliably visible ingredients/materials
reliably supported temperature / texture / serving cues
```

Resolve:

```text
FOOD_CATEGORY
CORE_INGREDIENT_OR_MATERIAL_SEMANTICS
TEMPERATURE_ATTRIBUTE
TEXTURE_MOUTHFEEL_ATTRIBUTE
PROCESS_OR_SERVING_CUE
REGIONAL_CULTURAL_CUE = RESOLVED_OR_NA
BRAND_POSITIONING
PRIMARY_VISUAL_MOOD
PRIMARY_COLOR_LOGIC
CATEGORY_MATERIAL_LANGUAGE
FORBIDDEN_STYLE_LANGUAGE
ATMOSPHERE_EVIDENCE >= 3
```

The product/category must drive the world. Generic adjectives such as premium, cinematic, warm or luxury are insufficient by themselves.

## 4. Creative Direction Is Candidate-Based

Read and execute `B_KV_CREATIVE_BOARD.md`.

Generate exactly three internally distinct concepts using different composition skeletons. Compare them. Select one winner. Only the winner enters the B Contract and IMAGE_MODEL prompt.

Do not treat material swaps as new concepts.

## 5. One Memorable Action

The selected concept must have one clear, thumbnail-readable, product-led action.

Examples of action grammar may include:

```text
product emerging through a category-native portal
counter or shelf architecture wrapping around product
headline embedded into the product support structure
flavor/steam/liquid field connecting product and type
asymmetric installation directing eye into product
packaging world extending the pack identity into the environment
negative-space editorial stage with one refined spatial anchor
```

These are design grammars, not reusable templates.

A mood phrase is not an action.

## 6. Composition Skeleton Matters More Than Surface Material

Anti-template evaluation must compare spatial skeleton, not whether the title is made of wood, paper, glass or metal.

Known safe fallback skeletons receive a strong penalty:

```text
TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO
BIG_SIGNBOARD + CENTER_PRODUCT + SMALL_PLAQUE
PHOTO + FOOTER
```

If the same skeleton remains after swapping materials, it is still the same template.

## 7. Product + Typography Co-Composition

Typography must belong to the same directed shot as the product, but typography complexity is not a goal by itself.

Strong relationships include:
- shared perspective field;
- shared support architecture;
- controlled overlap;
- atmosphere/light bridge;
- geometry echo;
- title embedded in a category-native structure;
- asymmetric negative space deliberately shaped around product.

If product and copy can be separated into independent rectangles with almost no loss, composition integration fails.

## 8. Typography Principle

Do **not** mechanically force perspective + volume + materiality + spatial attachment as a checklist.

Choose the typography behavior that best supports the winning concept and category. It may be dimensional, embedded, hanging, translucent, embossed, restrained editorial, architectural, or nearly flat when that is the strongest category-native decision.

Hard rules:
- typography must not become hero #1;
- it must not look pasted on;
- it must not default to a footer;
- it must belong to the selected composition skeleton;
- user-supplied text must remain exact.

## 9. Information Rhythm

Information density follows copy truth and concept.

Do not invent extra selling points to make the poster look richer. If copy is sparse, keep the KV elegant and spatially resolved. If copy is rich, distribute it into a clear hierarchy.

Possible hierarchy:

```text
PRODUCT HERO
HEADLINE
SUBTITLE / SLOGAN
AUTHORIZED SELLING POINTS
BRAND / STORE / ADDRESS / PHONE / QR / UTILITY
```

Not every job must visually activate every level.

## 10. Lighting + Atmosphere

Lighting must reveal current product truth and support the chosen campaign world.

Examples:
- bakery: crust, grain, warm oven/window light, but avoid turning every bakery into the same brown signboard world;
- hot bowls: broth depth, steam trajectory and table heat;
- cold drinks: translucency, condensation, freshness, cool light behavior;
- desserts: cream softness, glass/acrylic finesse, restrained highlights;
- seafood: moisture, clarity, refined cool/wet materiality;
- packaged retail: label readability, pack silhouette, brand-color discipline and retail clarity.

Never re-cook or over-amplify product surface state for drama.

## 11. True Upper-Bound

```text
TRUE_UPPER_BOUND =
PRODUCT_TRUTH
+ ONE_MEMORABLE_PRODUCT-DERIVED_IDEA
+ CATEGORY-NATIVE_WORLD
+ COMPOSITIONAL_TENSION
+ REFINED_EXECUTION
```

Upper-bound is not more decoration.

Do not equate it with:
- giant title;
- extra props;
- more badges;
- more text;
- thicker 3D type;
- more material effects.

For refined categories, a restrained solution can score higher than a busy one.

## 12. Director Pass Condition

Before B prompt compilation:

```text
VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >= 3
THREE_CANDIDATES_CREATED = TRUE
CANDIDATE_SKELETONS_DISTINCT = TRUE
WINNER_SELECTED = TRUE
SELECTED_ONE_MEMORABLE_ACTION = RESOLVED
PRODUCT_HERO_PROTECTION_PLAN = PASS
CATEGORY_INEVITABILITY_PLAN = PASS
THUMBNAIL_MEMORY_PLAN = PASS
ANTI_TEMPLATE_PLAN = PASS
```

Any missing field blocks B generation.
