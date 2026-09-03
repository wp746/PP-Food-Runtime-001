---
name: PP-Food-Runtime-001
description: Use when a real food, beverage, bakery, or packaged-product image should be processed through the fixed PP Food A/B production workflow and cross-agent reproducibility matters.
version: 1.0.0
---

# PP-Food-Runtime-001

This repository is the **production runtime** for stable cross-agent execution. It is self-contained: production agents must not depend on reading the two research repositories.

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
12. category_profiles/CATEGORY_PROFILES.yaml
```

Do not load `tests/` during normal production.

## User UX

After setup passes, reply READY and wait for `启动`.

In production the user only needs natural language plus:

- `执行A` / `A`
- `执行B` / `B`
- `按默认文案来` when they authorize safe non-factual copy generation.

## Core invariant

```text
PRESERVE THE PRODUCT.
UPGRADE THE PHOTOGRAPHY.
THEN BUILD THE KV.
```

A = commercial hero photography only.
B = current image → A → A QC PASS → B KV.

Never send this whole repository to the image model. Compile only the current-job contract and fixed prompt blocks.
