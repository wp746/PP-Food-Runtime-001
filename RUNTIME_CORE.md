# PP Food Runtime Core

This file is the production P0 source of truth. Other files may explain or specialize these rules but may not weaken them.

## P0 Rules

```text
P0-01 CURRENT_JOB_ONLY = TRUE
P0-02 SOURCE_TRUTH = CURRENT_USER_IMAGE
P0-03 A = STAGE_A_ONLY
P0-04 B = CURRENT_A -> A_QC_PASS -> B_KV_VISUAL_DIRECTOR -> CURRENT_B
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
P0-18 B_ONE_BIG_IDEA_MUST_BE_CONCRETE_SPATIAL_ACTION = TRUE
P0-19 B_ANTI_FLATNESS_REQUIRED = TRUE
P0-20 B_ATMOSPHERE_MUST_DERIVE_FROM_CURRENT_PRODUCT_SEMANTICS = TRUE
P0-21 B_PRODUCT_AND_TYPOGRAPHY_MUST_SHARE_COMPOSITION_LOGIC = TRUE
P0-22 B_DEFAULT_KV_MODE = TRUE_UPPER_BOUND
P0-23 B_ANTI_TEMPLATE_REQUIRED = TRUE
P0-24 B_THREE_DEPTH_STAGE_REQUIRED = TRUE
P0-25 B_LIGHTING_MUST_FOLLOW_PRODUCT_SEMANTICS = TRUE
P0-26 DIFFERENT_CATEGORY_REQUIRES_MAJOR_KV_REDESIGN = TRUE
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

## Stage B Upper-Bound Invariants

Every B job defaults to:

```text
KV_MODE = TRUE_UPPER_BOUND
```

Before B prompt compilation:

```text
VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >= 3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
HEADLINE_SPATIAL_FORM = RESOLVED
SHARED_COMPOSITION_LOGIC = PASS
PRODUCT_HERO_PROTECTION_PLAN = PASS
FOREGROUND_PLAN = PASS
MIDGROUND_PLAN = PASS
BACKGROUND_PLAN = PASS
LIGHTING_DRAMA_PLAN = PASS
MATERIAL_DEPTH_PLAN = PASS
ANTI_FLATNESS_PLAN = PASS
ANTI_TEMPLATE_DIFFERENTIATION = PASS
```

B is not `Stage A photo + text overlay` and not a repeated safe template.

The current product/category must drive atmosphere, materials, light, typography material and spatial action. Generic premium/cinematic styling is insufficient.

Headline must show at least 3 of:

```text
PERSPECTIVE
VOLUME / DEPTH
CATEGORY-NATIVE MATERIALITY
SPATIAL ATTACHMENT TO SCENE
```

Product remains hero #1. Headline remains hero #2.

If another food category could replace the current product with minimal redesign:

```text
CATEGORY_SPECIFIC_DIFFERENTIATION = FAIL
```

## Runtime Roles

VISION_MODEL:
- read current user image;
- build current-job facts and product lock;
- category route;
- build/verify B visual-director brief;
- QC A and B outputs.

IMAGE_MODEL:
- receives actual reference image;
- performs reference-image editing / image-to-image;
- never decides runtime flow.

If the host model cannot see images, it must not guess.

## Context Budget

Normal production loads only the runtime core plus files explicitly required by the current execution mode. Do not load tests, old conversations, research repositories, all category examples, or previous-job prompts into the current image-generation context.