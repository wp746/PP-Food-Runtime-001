# PP Food Runtime Core

This file is the production P0 source of truth. Other files may explain or specialize these rules but may not weaken them.

## P0 Rules

```text
P0-01 CURRENT_JOB_ONLY = TRUE
P0-02 SOURCE_TRUTH = CURRENT_USER_IMAGE
P0-03 A = STAGE_A_ONLY
P0-04 B = CURRENT_A -> A_QC_PASS -> B_VISUAL_DIRECTOR -> 3_CANDIDATES -> 1_WINNER -> CURRENT_B
P0-05 VISION_MODEL_REQUIRED_FOR_IMAGE_UNDERSTANDING = TRUE
P0-06 IMAGE_MODEL_MUST_SUPPORT_REFERENCE_IMAGE_EDIT = TRUE
P0-07 PRODUCT_FIDELITY_CAN_NEVER_BE_TRADED_FOR_DESIGN = TRUE
P0-08 PRODUCT_PRIORITY = 1
P0-09 HEADLINE_PRIORITY = 2
P0-10 PREVIOUS_JOB_FACTS_AND_SKIN_IMPORT = OFF
P0-11 ALL_CATEGORY_SKINS_ACTIVE_AT_ONCE = FORBIDDEN
P0-12 FULL_REPO_TO_IMAGE_MODEL = FORBIDDEN
P0-13 PROMPT_STRUCTURE = FIXED
P0-14 RETRY = TARGETED_NOT_RANDOM
P0-15 OUTPUT_ASPECT_RATIO = EXACT_9_16
P0-16 FAIL_CLOSED_ON_MISSING_CAPABILITY_OR_REQUIRED_STATE = TRUE
P0-17 B_VISUAL_DIRECTOR_REQUIRED = TRUE
P0-18 B_THREE_CANDIDATE_BOARD_REQUIRED = TRUE
P0-19 B_ONLY_WINNER_REACHES_IMAGE_MODEL = TRUE
P0-20 B_ATMOSPHERE_MUST_DERIVE_FROM_CURRENT_PRODUCT_SEMANTICS = TRUE
P0-21 B_PRODUCT_AND_TYPOGRAPHY_MUST_CO_COMPOSE = TRUE
P0-22 B_DEFAULT_KV_MODE = TRUE_UPPER_BOUND
P0-23 B_ANTI_TEMPLATE_CHECKS_SKELETON_NOT_MATERIAL = TRUE
P0-24 DIFFERENT_CATEGORY_REQUIRES_MAJOR_KV_REDESIGN = TRUE
P0-25 UPPER_BOUND_IS_NOT_DECORATION_COUNT = TRUE
P0-26 QC_IS_RESULT_ORIENTED_NOT_CHECKBOX_ACCUMULATION = TRUE
P0-27 DESIGN_REGRESSION_CANNOT_PASS = TRUE
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

Source surface state includes visible base color, browning, char, doneness, gloss/matte, moisture, sauce/oil coverage, crust/skin, scoring/cracks, frosting/cream, condensation/frost/translucency.

```text
REVEAL_EXISTING_PROPERTY = YES
AMPLIFY_BEYOND_SOURCE = NO
```

## Stage B Creative Invariants

Every B job defaults to:

```text
KV_MODE = TRUE_UPPER_BOUND
```

Upper-bound means:

```text
PRODUCT_TRUTH
+ ONE_MEMORABLE_PRODUCT-DERIVED_IDEA
+ CATEGORY-NATIVE_WORLD
+ COMPOSITIONAL_TENSION
+ REFINED_EXECUTION
```

It does **not** mean more type, more 3D, more props, more badges or more copy.

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

Known safe fallback skeletons are penalized:

```text
TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO
BIG_SIGNBOARD + CENTER_PRODUCT + SMALL_PLAQUE
PHOTO + FOOTER
```

Changing surface material does not make a new composition.

Product remains hero #1. Headline remains hero #2.

If another food category could replace the current product with minimal redesign:

```text
CATEGORY_INEVITABILITY = FAIL
```

## Runtime Roles

VISION_MODEL:
- read current user image;
- build current-job facts and product lock;
- category route;
- build B director brief;
- create/compare/select creative candidates;
- QC A and B outputs.

IMAGE_MODEL:
- receives actual reference image;
- receives only the selected compact B contract/prompt;
- performs reference-image editing / image-to-image;
- never decides runtime flow or candidate selection.

If the host model cannot see images, it must not guess.

## Context Budget

Normal production loads only runtime core plus files explicitly required by current execution mode. Do not load tests, old conversations, research repositories, all category examples, rejected creative candidates or previous-job prompts into the current image-generation context.
