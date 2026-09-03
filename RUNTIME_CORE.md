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

## Stage B Visual-Director Invariants

Before B prompt compilation:

```text
VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >= 3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
HEADLINE_SPATIAL_FORM = RESOLVED
SHARED_COMPOSITION_LOGIC = RESOLVED
PRODUCT_HERO_PROTECTION_PLAN = PASS
ANTI_FLATNESS_PLAN = PASS
```

B is not `Stage A photo + text overlay`.

The current product/category must drive atmosphere, materials, light, typography material and spatial action. A vague mood such as premium/cinematic/warm is not sufficient evidence.

Headline must show at least 3 of:

```text
PERSPECTIVE
VOLUME / DEPTH
CATEGORY-NATIVE MATERIALITY
SPATIAL ATTACHMENT TO SCENE
```

This requirement never overrides product dominance.

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
