---
name: PP-Food-Runtime-001
description: Use when a real food, beverage, bakery, or packaged-product image should be processed through the PP Food A/B workflow and stable cross-agent reproduction matters.
version: 1.3.0
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
category_profiles/CATEGORY_PROFILES.yaml
executors/B_CONTRACT_TEMPLATE.md
```

Do not load B creative files into A generation context. Do not load `tests/` during normal production. Do not send this repository, all category profiles, or rejected candidates to IMAGE_MODEL.

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
THEN DIRECT, COMPARE, SELECT, AND BUILD THE KV.
```

A = commercial hero photography only.

B = current image → A → A QC PASS → Visual Director → three internal candidate directions → select one winner → compact B contract → IMAGE_MODEL → result-oriented QC.

## B V1.3.0 Standard

Every B job defaults to `TRUE_UPPER_BOUND`, defined as:

```text
PRODUCT_TRUTH
+ ONE_MEMORABLE_PRODUCT-DERIVED_IDEA
+ CATEGORY-NATIVE_WORLD
+ COMPOSITIONAL_TENSION
+ REFINED_EXECUTION
```

Upper-bound is not more decoration. A restrained concept may outrank a busier one.

B must:
- create exactly three internally distinct composition skeletons;
- reject material-swap pseudo-innovation;
- select one winner before prompt compilation;
- keep product hero #1 and headline #2;
- derive atmosphere/light/material/typography behavior from current product/category;
- reject safe fallback skeletons unless uniquely justified;
- pass thumbnail memory and category inevitability checks;
- fail visible design regression even when formal rules are satisfied.

Known safe fallbacks include `TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO`, `BIG_SIGNBOARD + CENTER_PRODUCT + SMALL_PLAQUE`, and `PHOTO + FOOTER`.

Never trade product fidelity for creative pressure. Never send rejected candidates or the full repository to IMAGE_MODEL.
