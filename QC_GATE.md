# QC Gate

VISION_MODEL performs post-generation QC. Do not accept an output because it is merely attractive, and do not accept it merely because individual checklist items can be named.

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

## B Hard Gates

```text
Stage B Reference = CURRENT_JOB_STAGE_A_PASS_IMAGE
Food / Product Fidelity >=95
Vessel / Packaging Fidelity >=98
Typography Accuracy =100%
Product Dominance = PASS
Unsupported Hard Facts = 0
Previous-Skin Contamination = FALSE
Aspect Ratio = EXACT 9:16
```

Any hard-gate failure is immediate FAIL.

## B Creative Evaluation — Result Oriented

Do not score B by counting effects such as perspective, extrusion or materiality. Judge the final image.

Score 0–100:

```text
PRODUCT_LED_MEMORABILITY
CATEGORY_INEVITABILITY
COMPOSITIONAL_TENSION
SPATIAL_INTEGRATION
CAMPAIGN_REFINEMENT
TYPOGRAPHY_FIT
INFORMATION_RHYTHM
ANTI_TEMPLATE_ORIGINALITY
```

Required:

```text
PRODUCT_LED_MEMORABILITY >=90
CATEGORY_INEVITABILITY >=90
COMPOSITIONAL_TENSION >=88
SPATIAL_INTEGRATION >=88
CAMPAIGN_REFINEMENT >=90
TYPOGRAPHY_FIT >=88
ANTI_TEMPLATE_ORIGINALITY >=88
UPPER_BOUND_READINESS >=90
```

Information Rhythm is scored only when enough authorized copy exists. Sparse copy is not penalized for remaining sparse.

## Thumbnail Memory Test

View mentally at small size. PASS only if:
- product is still first read;
- one memorable spatial/compositional action remains clear;
- poster is not merely balanced and polite;
- concept is recognizable without reading every line of copy.

If the image is technically correct but forgettable, FAIL.

## Category Inevitability Test

Ask:

> If the product were replaced by a very different food category, would the environment, typography behavior, materials, lighting and composition require major redesign?

If no, FAIL.

## Skeleton Anti-Template Test

Evaluate composition skeleton, not surface material.

Known fallback skeletons:

```text
TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO
BIG_SIGNBOARD + CENTER_PRODUCT + SMALL_PLAQUE
PHOTO + FOOTER
```

Wood → paper → glass → metal is still the same skeleton if the spatial arrangement is unchanged.

A known fallback may pass only when the current product semantics uniquely justify it and the final composition still demonstrates strong originality.

## Self-Justification Guard

QC may not use statements like:

```text
there is perspective, therefore PASS
there is a material title, therefore PASS
there are three depth layers, therefore PASS
```

For each major creative score, QC must cite a concrete visible result:
- what the eye reads first;
- where the memorable action occurs;
- how product and typography co-compose;
- why the world belongs specifically to this product;
- why the skeleton is not a safe fallback.

If the evaluator cannot state convincing visible evidence, lower the score or FAIL.

## Comparative Sanity Check

When the same current job has a previous B attempt available, compare only to detect regression:
- product dominance;
- memorability;
- category fit;
- composition tension;
- refinement.

A newer version must not PASS merely because it satisfies more formal rules. If it is visibly weaker than a previous passing attempt on the same job, mark `DESIGN_REGRESSION = TRUE` and retry.

## Upper-Bound Definition

```text
UPPER_BOUND =
PRODUCT_TRUTH
+ ONE_MEMORABLE_PRODUCT-DERIVED_IDEA
+ CATEGORY-NATIVE_WORLD
+ COMPOSITIONAL_TENSION
+ REFINED_EXECUTION
```

More elements do not automatically increase the score.

Any failure routes to `RETRY_POLICY.md`; do not call it PASS.
