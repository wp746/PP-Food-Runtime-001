# PP-Food-Runtime-001

Self-contained production runtime for stable A/B food-image generation across different host agents.

## Why this repo exists

The research skills `PP-food-001` and `PP-food-KV-001` contain broad methodology, references, tests and historical evolution. This repository is the **production release layer**: fewer files, one authority chain, fixed A/B executors, fixed prompt compiler, compact contracts, current-job isolation and category isolation.

Normal production must not depend on reading the research repositories.

## Install / startup

Read `SKILL.md`, then follow the exact runtime entry order.

Configure:
- VISION_MODEL
- IMAGE_MODEL with reference-image editing
- API base/connection
- credential in secure storage
- image pass-through, including Stage A → Stage B

When setup passes, the agent returns READY and waits for `启动`.

## Production UX

```text
执行A
```
Commercial hero photograph only.

```text
执行B
```
Current image → current A → A QC PASS → candidate-based KV visual direction → one selected upper-bound KV.

```text
按默认文案来
```
Authorize safe non-factual campaign copy only; never authorize invented business facts.

## V1.3.0 B architecture

Stage B no longer chooses a single first idea and no longer equates upper-bound with more 3D effects or more decoration.

```text
CURRENT STAGE A PASS
→ PRODUCT / CATEGORY SEMANTICS
→ 3 DISTINCT COMPOSITION CANDIDATES
→ SCORE / COMPARE
→ SELECT 1 WINNER
→ COMPACT B CONTRACT
→ IMAGE MODEL
→ RESULT-ORIENTED QC
```

Only the winning candidate reaches IMAGE_MODEL.

Anti-template checks the **composition skeleton**, not whether the title is wood, kraft paper, glass or metal. Known safe fallback structures such as `TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO` receive a strong penalty.

Upper-bound means:

```text
PRODUCT_TRUTH
+ ONE_MEMORABLE_PRODUCT-DERIVED_IDEA
+ CATEGORY-NATIVE_WORLD
+ COMPOSITIONAL_TENSION
+ REFINED_EXECUTION
```

More props, more copy, larger typography or thicker 3D type do not automatically improve the result.

## Status

Version: 1.3.0

Release state: INTERNAL REFACTOR COMPLETE / FINAL CROSS-AGENT VALIDATION STILL REQUIRED.

The runtime must not be called production-qualified until the intended host/model stack completes a final external validation. That validation should be treated as a release acceptance run, not iterative prompt tuning.
