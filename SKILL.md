---
name: PP-Food-Runtime-001
description: Use when a real food, beverage, bakery, or packaged-product image should be processed through the fixed PP Food A/B production workflow and cross-agent reproducibility matters.
version: 1.2.0
---

# PP-Food-Runtime-001

This repository is the **self-contained production runtime** for stable cross-agent execution.

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
category_profiles/CATEGORY_PROFILES.yaml
executors/B_CONTRACT_TEMPLATE.md
```

Do not load B visual-director/category material into A generation context. Do not load `tests/` during normal production. Do not send all category profiles or this repository to IMAGE_MODEL.

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
THEN DIRECT AND BUILD THE UPPER-BOUND KV.
```

A = commercial hero photography only.

B = current image → A → A QC PASS → B KV Visual Director → compact B contract → upper-bound category-native KV → full QC.

## B V1.2.0 Standard

Every B job defaults to:

```text
KV_MODE = TRUE_UPPER_BOUND
```

The current food/product must drive atmosphere, materials, lighting, typography material, spatial action and information rhythm.

B must include:

```text
one concrete spatial One Big Idea
product hero #1 / headline #2
shared product-type composition logic
foreground / midground / background campaign stage
category-native lighting drama
material depth
anti-flatness
anti-template differentiation
```

A repeated `big signboard above + product centered below + plaque bottom` structure is not an acceptable default. If another food category could replace the product with minimal redesign, B fails category-specific differentiation.

Never trade product fidelity for upper-bound design pressure. Never send this whole repository to the image model; compile only the current-job contract and fixed six-block prompt.