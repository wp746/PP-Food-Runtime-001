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

A1 must be first and state that the current reference image is the only product truth. The product may not be redesigned, replaced, re-plated, re-cooked, re-packaged, or beautified into another serving.

## B Prompt — exactly 6 blocks

```text
B1 CURRENT STAGE A PRODUCT LOCK
B2 SELECTED DIRECTOR CONCEPT + CURRENT CATEGORY
B3 COPY TRUTH + INFORMATION RHYTHM
B4 PRODUCT HERO + TYPOGRAPHY ROLE
B5 CATEGORY-NATIVE WORLD + COMPOSITION SKELETON
B6 HARD NEGATIVES
```

B1 must reference the current job Stage A PASS image, never the raw snapshot or a previous job.

## B2 — Winner Only

Include only selected candidate outputs:

```text
selected composition skeleton
selected memorable action
why it belongs to this product
current category profile
core ingredient/material semantics
primary visual mood
primary color/material logic
lighting logic
atmosphere bridge
forbidden style language
```

Do not include rejected candidates or all category profiles.

## B3 — Copy Truth

Include exact user-authorized copy only. Information density follows actual copy truth. Do not force extra selling points, badges or utility fields to make the design look richer.

## B4 — Product Hero + Typography Role

Product is hero #1. Headline is hero #2.

Describe typography according to the selected concept, not a universal 3D checklist. Specify:

```text
headline role in composition
headline material/medium only if concept needs it
headline relationship to product
subtitle/slogan relationship
utility placement logic
occlusion limits
```

Typography must feel integrated, but it may be restrained if restraint better serves the category.

## B5 — Category-Native World + Skeleton

Specify the winning spatial structure and depth logic:

```text
composition skeleton
foreground/midground/background relationship when relevant
primary spatial axis
product support architecture
light direction and material transition
negative-space strategy
one memorable action
```

Do not convert this into a decoration checklist.

## B6 — Hard Negatives

Always include:

```text
no raw snapshot as B reference after A PASS
no previous-job facts or visual skin
no product/package/vessel/plating redesign
no unsupported hard facts
no headline dominance over product
no photo-plus-footer fallback
no TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO safe template unless uniquely justified
no material-swap pseudo-innovation
no rejected candidate blending
no generic all-category 3D title treatment
```

## Prompt Budget Rules

Do not send to IMAGE_MODEL:
- this whole repository;
- tests;
- runtime state explanations;
- all category profiles;
- previous-job examples;
- rejected candidates;
- duplicated synonyms of the same constraint.

IMAGE_MODEL receives only:

```text
CURRENT_REFERENCE_IMAGE
+ CURRENT_COMPACT_CONTRACT
+ FIXED_6_BLOCK_PROMPT
```

If prompt compilation introduces contradictory rules or multiple competing concepts, block production and resolve the contract first.
