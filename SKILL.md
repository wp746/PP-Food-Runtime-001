---
name: PP-Food-Runtime-001
description: Use when a real food, beverage, bakery, or packaged-product image should be processed through the PP Food A/B workflow and stable cross-agent reproduction matters.
version: 1.4.0
---

# PP-Food-Runtime-001

Self-contained production runtime for stable cross-agent A/B execution.

## Entry

Read, in this exact order:

```text
1. VERSION
2. RUNTIME_CORE.md
3. SETUP_GATE.md
4. STARTUP_PROTOCOL.md
5. EXECUTION_MODES.md
6. CURRENT_JOB_ISOLATION.md
7. PROMPT_COMPILER.md
8. QC_GATE.md
9. RETRY_POLICY.md
10. executors/A_EXECUTOR.md
11. executors/B_EXECUTOR.md
```

For B only, after current Stage A PASS and category routing, additionally read:

```text
B_KV_VISUAL_DIRECTOR.md
B_KV_CREATIVE_BOARD.md
B_KV_VISUAL_AUDITION.md
category_profiles/CATEGORY_PROFILES.yaml
executors/B_CONTRACT_TEMPLATE.md
```

Do not load B creative files into A generation context. Do not load `tests/` during normal production. Do not send this repository, all category profiles, rejected candidates or planning prose to IMAGE_MODEL.

## User UX

After setup passes, reply READY and wait for `启动`.

Production commands:

- `执行A` / `A`
- `执行B` / `B`
- `按默认文案来` only when safe non-factual copy generation is authorized.

## Core invariant

```text
PRESERVE THE PRODUCT.
UPGRADE THE PHOTOGRAPHY.
THEN DIRECT, RENDER-COMPARE, SELECT, AND REFINE THE KV.
```

A = commercial hero photography only.

B quality-first mode:

```text
current image
→ Stage A
→ A QC PASS
→ 3 textual art-direction candidates
→ 2 visually distinct finalists
→ render finalist A + finalist B
→ VISION_MODEL compares actual images
→ select winner
→ optional targeted refinement
→ final B QC
```

## B V1.4.0 Standard

Stage A establishes both product truth and hero-camera baseline. B may not shrink the apparent product scale by more than 15% or let environment/title become the first read.

Category semantics must be translated into palette, light, surface, rhythm, geometry, negative space and typography behavior. Do not literalize them into themed scenery by default.

`TRUE_UPPER_BOUND` means:

```text
PRODUCT_TRUTH
+ PRODUCT_HERO_STRENGTH
+ ONE MEMORABLE PRODUCT-DERIVED IDEA
+ CATEGORY-NATIVE BUT NON-LITERAL WORLD
+ COMPOSITIONAL TENSION
+ CONTEMPORARY CAMPAIGN REFINEMENT
```

Upper-bound is not more scenery, more props, bigger architecture, thicker 3D type or more text.

For stable upper-bound B, actual rendered finalist comparison is mandatory. Textual candidate scores alone cannot establish PASS.

Never trade product fidelity or product hero strength for creative pressure.