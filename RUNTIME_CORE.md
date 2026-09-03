# PP Food Runtime Core

This file is the production P0 source of truth. Other files may specialize these rules but may not weaken them.

## P0 Rules

```text
P0-01 CURRENT_JOB_ONLY = TRUE
P0-02 SOURCE_TRUTH = CURRENT_USER_IMAGE
P0-03 A = STAGE_A_ONLY
P0-04 B = CURRENT_A -> A_QC_PASS -> B_VISUAL_DIRECTOR -> 3_TEXT_CANDIDATES -> 2_RENDER_FINALISTS -> VISUAL_COMPARISON -> WINNER -> FINAL_B
P0-05 VISION_MODEL_REQUIRED_FOR_IMAGE_UNDERSTANDING = TRUE
P0-06 IMAGE_MODEL_MUST_SUPPORT_REFERENCE_IMAGE_EDIT = TRUE
P0-07 PRODUCT_FIDELITY_CAN_NEVER_BE_TRADED_FOR_DESIGN = TRUE
P0-08 PRODUCT_PRIORITY = 1
P0-09 HEADLINE_PRIORITY = 2
P0-10 PREVIOUS_JOB_FACTS_AND_SKIN_IMPORT = OFF
P0-11 ALL_CATEGORY_SKINS_ACTIVE_AT_ONCE = FORBIDDEN
P0-12 FULL_REPO_TO_IMAGE_MODEL = FORBIDDEN
P0-13 PROMPT_STRUCTURE = FIXED
P0-14 OUTPUT_ASPECT_RATIO = EXACT_9_16
P0-15 FAIL_CLOSED_ON_MISSING_CAPABILITY_OR_REQUIRED_STATE = TRUE
P0-16 B_VISUAL_DIRECTOR_REQUIRED = TRUE
P0-17 B_RENDERED_VISUAL_AUDITION_REQUIRED_FOR_UPPER_BOUND_STABLE = TRUE
P0-18 B_PRODUCT_APPARENT_SCALE_SHRINK_FROM_STAGE_A <= 15_PERCENT
P0-19 B_ENVIRONMENT_MAY_NOT_BECOME_FIRST_READ = TRUE
P0-20 B_CATEGORY_SEMANTICS_TRANSLATED_NOT_LITERALIZED = TRUE
P0-21 B_DEFAULT_KV_MODE = TRUE_UPPER_BOUND
P0-22 B_ANTI_TEMPLATE_CHECKS_SKELETON_NOT_MATERIAL = TRUE
P0-23 DIFFERENT_CATEGORY_REQUIRES_MAJOR_KV_REDESIGN = TRUE
P0-24 UPPER_BOUND_IS_NOT_DECORATION_COUNT = TRUE
P0-25 QC_USES_ACTUAL_IMAGE_EVIDENCE = TRUE
P0-26 DESIGN_REGRESSION_CANNOT_PASS = TRUE
```

## Fidelity Targets

```text
Food / Product Identity >=95
Ingredient / Product Geometry >=95
Vessel / Container / Packaging >=98
Plating / Arrangement >=95
Physical Relationships >=95
Source Surface State = LOCKED
```

## Stage A to B Hero Lock

Stage A establishes both product truth and hero-camera baseline.

B must preserve product authority:

```text
PRODUCT_APPARENT_SCALE_SHRINK_FROM_STAGE_A <=15%
PRODUCT_FIRST_READ = TRUE
ENVIRONMENT_FIRST_READ = FALSE
HEADLINE_FIRST_READ = FALSE
```

A more dramatic scene is not an upgrade if it pushes the product deeper or smaller.

## Stage B Upper-Bound Definition

```text
TRUE_UPPER_BOUND =
PRODUCT_TRUTH
+ PRODUCT_HERO_STRENGTH
+ ONE MEMORABLE PRODUCT-DERIVED IDEA
+ CATEGORY-NATIVE BUT NON-LITERAL WORLD
+ COMPOSITIONAL TENSION
+ CONTEMPORARY CAMPAIGN REFINEMENT
```

Not equivalent to more props, more 3D type, bigger architecture, more text or literal category scenery.

## Stage B Quality-First Pipeline

```text
3 textual candidates
→ 2 visually distinct finalists
→ 2 actual B renders from same Stage A PASS image
→ VISION_MODEL compares actual rendered images
→ select winner
→ optional one targeted refinement
→ final QC
```

Textual candidate scoring alone cannot establish upper-bound PASS.

If the runtime cannot render and visually compare at least two B candidates:

```text
B_QUALITY_MODE = DEGRADED
UPPER_BOUND_STABLE_CLAIM = FORBIDDEN
```

## Non-Literal Category Translation

Product semantics drive palette, light, material, rhythm, geometry, negative space and typography behavior.

Do not automatically turn categories into literal themed environments such as old oven tunnels, restaurant caves, giant rustic signs, decorative acrylic worlds or other scenic clichés.

## Runtime Roles

VISION_MODEL:
- read current user image;
- build product lock;
- category route;
- build director candidates;
- inspect actual rendered finalists;
- select winner from visual evidence;
- QC final output.

IMAGE_MODEL:
- receives actual Stage A PASS reference;
- renders each finalist separately;
- receives only compact current finalist contract + fixed prompt;
- never decides runtime flow or winner.

## Context Budget

Do not load tests, research repositories, old conversations, all category examples, rejected prompts or previous-job skin into current IMAGE_MODEL context.