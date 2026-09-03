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
B2 VISUAL DIRECTOR + CURRENT CATEGORY PROFILE
B3 COPY TRUTH + INFORMATION RHYTHM
B4 PRODUCT HERO + SPATIAL TYPOGRAPHY
B5 ONE BIG IDEA + CATEGORY-NATIVE WORLD
B6 HARD NEGATIVES + ANTI-FLATNESS
```

B1 must reference the current job Stage A PASS image, never the raw snapshot or a previous job.

### B2 must contain only current-job director outputs

```text
core ingredient/material semantics
temperature / texture / process cue
primary visual mood
primary color logic
title material language
forbidden style language
ATMOSPHERE_EVIDENCE >= 3
selected primary category profile
optional weak auxiliary profile
```

Do not inject other category skins.

### B3 must preserve copy truth

Include exact user-authorized copy only. Define distinct hierarchy for headline, subtitle/slogan, selling points, and utility fields when available. Sparse facts stay sparse.

### B4 hard spatial rule

Product remains hero #1; headline hero #2.

Headline must express at least 3 of:

```text
perspective
volume/depth
category-native materiality
spatial attachment to scene
```

B4 must specify `SHARED_COMPOSITION_LOGIC`: product and typography share a perspective field, support plane, stage structure, controlled overlap, atmosphere bridge, geometry echo, or another explicit director-approved relationship.

Do not create an unrelated text rectangle beneath the product.

### B5 requires a concrete action

`ONE_BIG_IDEA` must be a spatial campaign action, not a mood adjective. Describe how the title/world behaves in space and why it belongs to this product/category.

### B6 anti-flatness negatives

Always include:

```text
no commercial-photo-plus-footer-layout
no bottom-only headline strip
no all-copy-on-one-flat-plane
no unrelated product-zone/text-zone split
no generic 3D title treatment detached from category
no title dominance over product
no previous-job skin
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

If the agent cannot compile the prompt without introducing contradictory rules, block production and resolve the contract first.
