# Fixed Prompt Compiler

The host agent must not invent a new prompt architecture. It fills current-job variables into the fixed blocks below.

## A Prompt — exactly 6 blocks

```text
A1 REFERENCE LOCK
A2 PRODUCT DNA + SURFACE STATE
A3 VESSEL / PACKAGE / DIRECT SUPPORT
A4 COMMERCIAL HERO PHOTOGRAPHY
A5 CURRENT CATEGORY BACKGROUND ARCHITECTURE
A6 HARD NEGATIVES
```

## B Prompt — exactly 6 blocks per rendered finalist

```text
B1 CURRENT STAGE A PRODUCT + HERO CAMERA LOCK
B2 CURRENT CATEGORY SEMANTIC TRANSLATION
B3 COPY TRUTH + INFORMATION HIERARCHY
B4 PRODUCT HERO + TYPOGRAPHY ROLE
B5 SELECTED COMPOSITION + CONTEMPORARY CAMPAIGN WORLD
B6 HARD NEGATIVES
```

Each finalist gets its own compact prompt. Do not combine finalist concepts.

## B1 — Product + Hero Camera Lock

State:

```text
REFERENCE = CURRENT_JOB_STAGE_A_PASS_IMAGE
PRODUCT_TRUTH = LOCKED
PRODUCT_APPARENT_SCALE_SHRINK_FROM_STAGE_A <= 15%
PRODUCT_FIRST_READ = TRUE
ENVIRONMENT_MAY_NOT_BECOME_PRIMARY_SUBJECT
```

Do not push the product deep into a room, tunnel, portal, shelf or architecture.

## B2 — Semantic Translation, Not Literal Set Design

Include only current-job signals and their design translation:

```text
food/material semantics
palette logic
lighting logic
surface/material cues
rhythm/geometry
negative-space behavior
forbidden literalism
```

Do not say only “bakery world”, “luxury seafood world” or similar vague scene labels. Describe how semantics become visual design cues.

## B3 — Copy Truth

Use exact authorized copy. Do not invent hard facts or add filler selling points solely for visual density.

## B4 — Product Hero + Typography Role

```text
PRODUCT = HERO #1
HEADLINE = HERO #2
```

Typography behavior follows the finalist concept. It may be dimensional or restrained. It may not force product shrinkage or become menu/signage-first.

## B5 — Contemporary Campaign World

Specify:
- finalist composition skeleton;
- primary negative-space strategy;
- one memorable product-led gesture;
- support-plane/depth relationship;
- controlled material family;
- light direction;
- refined hierarchy.

World-class does not mean more scenery. The scene should read as contemporary food advertising, not a themed set.

## B6 — Hard Negatives

Always include:

```text
no raw snapshot after Stage A PASS
no previous-job facts/skin
no product/package/vessel/plating redesign
no unsupported hard facts
no product shrinkage beyond hero-camera limit
no environment-first composition
no giant portal/tunnel/arch dominating product
no theatrical rustic set unless product-led and justified
no brown-on-brown material overload
no menu-board/souvenir-sign aesthetic
no photo-plus-footer fallback
no TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO safe template
no material-swap pseudo-innovation
no rejected-candidate blending
```

## Prompt Budget

IMAGE_MODEL receives only:

```text
CURRENT_STAGE_A_PASS_IMAGE
+ CURRENT_FINALIST_COMPACT_CONTRACT
+ CURRENT_FINALIST_6_BLOCK_PROMPT
```

Never send the whole repository, tests, rejected candidates, all category profiles or duplicated constraints.