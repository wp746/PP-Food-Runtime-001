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

After startup:

```text
执行A
```
= commercial hero photograph only.

```text
执行B
```
= current image → current A → A QC PASS → category-native KV.

```text
按默认文案来
```
= authorize safe non-factual campaign copy only; never authorize invented business facts.

## Runtime design

```text
CURRENT IMAGE
→ VISION MODEL
→ CURRENT JOB CONTRACT
→ FIXED PROMPT COMPILER
→ IMAGE MODEL
→ VISION QC
→ TARGETED RETRY
```

B adds a mandatory current Stage A bridge before Stage B.

## Status

Version: 1.0.0

Release state: BUILD COMPLETE / CROSS-AGENT VALIDATION REQUIRED.

Do not mark production-qualified until the runtime contract tests pass on at least two different host agents using the intended vision/image stack.
