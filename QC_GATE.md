# QC Gate — 1.0.0-rc.2

QC is based on actual generated pixels. Prompt wording and generator self-description are not evidence.

## Stage A hard QC

```text
Aspect Ratio = EXACT 9:16
Food / Product Identity >=95
Ingredient / Product Geometry >=95
Vessel / Container / Packaging >=98
Plating / Arrangement >=95
Physical Relationships >=95
Source Surface State = PASS
Photography >=85
Semantic Relevance >=85
Hero Spatial >=85
Appetite >=85
Critical Failure = NONE
```

Stage A is the binding visual bridge into B.

## PRODUCTION_FAST Hard Gate

Production Fast deliberately ignores Golden soft-score shortfalls as automatic retry triggers. It blocks only delivery-critical failures:

- mechanical/broken render;
- Stage A reference binding failure;
- product identity/truth drift;
- unauthorized or corrupted copy;
- product is no longer the first visual hero;
- scene/environment dominates the product;
- clearly unshippable commercial finish.

Evaluator confidence `< 0.65` yields `NEEDS_SECOND_EVALUATION` / `EVALUATOR_FAILURE`. Re-run evaluation only; do not regenerate the image.

A Production Fast PASS therefore means **shippable truth-preserving output**, not “perfect Golden score”.

## VALIDATION Golden Gate

Validation keeps the full eight-dimensional Golden vector. Current floors:

```text
product_hero_strength           >= 9.2
headline_aggression             >= 8.8
typography_product_symbiosis    >= 8.8
one_big_idea_clarity            >= 9.0
compositional_depth_tension     >= 8.8
category_inevitability          >= 9.0
information_density_control     >= 8.8
commercial_finish               >= 9.2
```

Product truth, copy truth, mechanical validity and reference binding remain hard gates above style scores.

## Pairwise isolation

Validation pairwise receives exactly three images:

```text
image_1 = current Stage A PASS control
image_2 = Primary
image_3 = Challenger
```

Only image 2 or image 3 may win. Source and Golden images are not candidate slots.

## Category / Golden routing integrity

Before Golden-relative QC, runtime category routing must use normalized pack/food signals. Provider casing differences such as `Pack` vs `PACK` must not change which category pack or Golden family is selected. Missing requested Golden evidence is a diagnostic condition, not a reason to crash the acceptance run.

## Anti-drift tests

Validation should explicitly inspect for:

- `SAFE_EDITORIAL_COLLAPSE`
- `SCENE_DOMINATES_PRODUCT`
- `PHOTO_PLUS_TEXT`
- `CATEGORY_CLICHE_DEPENDENCE`
- `GENERIC_PREMIUM_SKIN`
- `TEMPLATE_REUSE`
- `INFORMATION_STARVATION` / `INFORMATION_OVERLOAD`
- product/copy/reference truth failures.

A new rule version is not evidence of a better image. Visible pixels decide.
