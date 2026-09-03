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

A1 must be first and must state that the current reference image is the only product truth and the product may not be redesigned, replaced, re-plated, re-cooked, re-packaged, or beautified into another serving.

A5 is derived from the current product/category only. Do not inject all category examples.

## B Prompt — exactly 6 blocks

```text
B1 CURRENT STAGE A PRODUCT LOCK
B2 UPPER-BOUND VISUAL DIRECTOR + CURRENT CATEGORY PROFILE
B3 COPY TRUTH + INFORMATION RHYTHM
B4 PRODUCT HERO + SPATIAL TYPOGRAPHY + SHARED COMPOSITION
B5 ONE BIG IDEA + THREE-DEPTH CATEGORY WORLD + LIGHT/MATERIAL DRAMA
B6 HARD NEGATIVES + ANTI-FLATNESS + ANTI-TEMPLATE
```

B1 must reference the current job Stage A PASS image, never the raw snapshot or a previous job.

### B2 — current-job director outputs only

Include:

```text
core ingredient/material semantics
temperature / texture / process cue
regional/brand cue when supported
primary visual mood
primary color logic
title material language
forbidden style language
ATMOSPHERE_EVIDENCE >= 3
selected primary category profile
optional weak auxiliary profile
ANTI_TEMPLATE_DIFFERENTIATION
```

Do not inject other category skins.

### B3 — copy truth + differentiated rhythm

Include only exact user-authorized hard facts and explicitly authorized safe campaign copy.

Define hierarchy when content exists:

```text
L1 PRODUCT HERO
L2 HEADLINE
L3 SUBTITLE / SLOGAN
L4 SELLING POINTS
L5 BRAND / UTILITY
```

Do not fabricate hard facts to satisfy density.

### B4 — upper-bound spatial typography

```text
PRODUCT_PRIORITY = 1
HEADLINE_PRIORITY = 2
```

Headline must express at least 3 of:

```text
PERSPECTIVE
VOLUME / DEPTH
CATEGORY-NATIVE MATERIALITY
SPATIAL ATTACHMENT TO SCENE
```

B4 must include explicit `SHARED_COMPOSITION_LOGIC` linking product and typography through perspective, support plane, stage structure, controlled overlap, atmosphere, geometry, light or material continuity.

Do not create an unrelated text rectangle above or below the product.

### B5 — concrete action + campaign depth

`ONE_BIG_IDEA` must be a concrete spatial campaign action, not a mood adjective.

B5 must specify:

```text
FOREGROUND_PLAN
MIDGROUND_PLAN
BACKGROUND_PLAN
LIGHTING_DRAMA_PLAN
MATERIAL_DEPTH_PLAN
```

At least two independent depth cues beyond the product are required.

The category world must be visibly derived from current food/product semantics. Premium-looking but category-generic staging is insufficient.

### B6 — hard negatives

Always include:

```text
no commercial-photo-plus-footer-layout
no bottom-only headline strip
no all-copy-on-one-flat-plane
no unrelated product-zone/text-zone split
no giant-title-first-read
no product-as-background-or-wallpaper
no generic signboard-above-product template unless uniquely justified
no repeated previous-job composition skin
no generic 3D title detached from category
no random prop-pack used as premium substitute
no unsupported hard facts
no product/package/vessel/plating redesign
```

## Prompt Budget Rules

Do not send to IMAGE_MODEL:
- this whole repository;
- tests;
- runtime state explanations;
- all 12 category profiles;
- previous-job examples;
- duplicated synonyms of the same constraint.

IMAGE_MODEL receives only:

```text
CURRENT_REFERENCE_IMAGE
+ CURRENT_COMPACT_CONTRACT
+ FIXED_6_BLOCK_PROMPT
```

If the agent cannot compile the prompt without contradiction or without a concrete upper-bound director brief, block production and repair the contract first.