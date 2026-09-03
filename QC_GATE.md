# QC Gate

VISION_MODEL performs QC from actual generated images. Planning language is not evidence.

## A QC

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

## B Hard Truth Gates

```text
Stage B Reference = CURRENT_JOB_STAGE_A_PASS_IMAGE
Food / Product Fidelity >=95
Vessel / Packaging Fidelity >=98
Typography Accuracy =100%
Unsupported Hard Facts = 0
Previous-Skin Contamination = FALSE
Aspect Ratio = EXACT 9:16
```

## B Hero Preservation Gates

Compare final B against Stage A visually:

```text
PRODUCT_APPARENT_SCALE_SHRINK_FROM_STAGE_A <=15%
PRODUCT_FIRST_READ = TRUE
ENVIRONMENT_FIRST_READ = FALSE
HEADLINE_FIRST_READ = FALSE
PRODUCT_IDENTITY/APPETITE_AREA_OCCLUSION = LOW
```

If architecture, tunnel, arch, room, signboard, shelf or props become the main subject, FAIL.

## B Visual Audition Gate

Upper-bound stable mode requires:

```text
TWO_RENDERED_CANDIDATES = TRUE
CANDIDATES_VISUALLY_DISTINCT = TRUE
VISION_MODEL_COMPARED_ACTUAL_IMAGES = TRUE
WINNER_SELECTED_FROM_VISUAL_EVIDENCE = TRUE
```

Text-board scoring alone may not produce PASS.

## B Contemporary Campaign Evaluation

Score actual final image 0–100:

```text
PRODUCT_HERO_STRENGTH
CAMPAIGN_REFINEMENT
PRODUCT_LED_MEMORABILITY
CATEGORY_INEVITABILITY
TYPOGRAPHY_INTEGRATION
COMPOSITIONAL_TENSION
NEGATIVE_SPACE_QUALITY
MATERIAL_RESTRAINT
ANTI_TEMPLATE_ORIGINALITY
```

Required:

```text
PRODUCT_HERO_STRENGTH >=92
CAMPAIGN_REFINEMENT >=92
PRODUCT_LED_MEMORABILITY >=90
CATEGORY_INEVITABILITY >=90
TYPOGRAPHY_INTEGRATION >=88
COMPOSITIONAL_TENSION >=88
NEGATIVE_SPACE_QUALITY >=88
MATERIAL_RESTRAINT >=88
ANTI_TEMPLATE_ORIGINALITY >=88
UPPER_BOUND_READINESS >=92
```

## Literalism / Theme-Set Rejection

Immediate FAIL when the final KV reads primarily as:
- old oven tunnel / cave / medieval bakery set;
- themed restaurant interior;
- souvenir sign or menu board;
- prop-heavy scenic diorama;
- literal category illustration rather than contemporary campaign art direction;
- brown-on-brown rustic environment that weakens product hierarchy.

Category cues should be translated into light, palette, surface, rhythm, geometry and type behavior rather than literal scenery.

## Thumbnail Memory Test

At small size:
- product must be the first read;
- one product-led gesture must remain memorable;
- design must not depend on reading all copy;
- environment may not become the remembered subject instead of the product.

## Category Inevitability Test

Replacing the current product with a very different category must require major redesign of palette, material, light, type behavior and composition.

## Anti-Template Test

Known fallback skeletons are penalized:

```text
TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO
BIG_SIGNBOARD + CENTER_PRODUCT + SMALL_PLAQUE
PHOTO + FOOTER
```

Material changes do not create originality.

## Self-Justification Guard

Do not PASS because a checklist item can be named. For every major score, cite a visible image-level fact. If convincing visible evidence is unavailable, lower the score or FAIL.

## Comparative Selection Rule

When two rendered finalists exist, choose the one with stronger product hero strength and campaign refinement first. A more dramatic environment does not win merely because it is more novel.

## Design Regression

When a previous attempt for the same job exists, a visibly weaker new result cannot PASS because it follows newer rules. Mark `DESIGN_REGRESSION = TRUE` and retain or refine the stronger direction.