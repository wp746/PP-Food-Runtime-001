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
B2 CURRENT CATEGORY PROFILE
B3 COPY TRUTH
B4 PRODUCT HERO + SPATIAL TYPOGRAPHY
B5 ONE BIG IDEA + CATEGORY-NATIVE WORLD
B6 HARD NEGATIVES
```

B1 must reference the current job Stage A PASS image, never the raw snapshot or a previous job.

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
