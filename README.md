# PP-Food-Runtime-001

Self-contained production runtime for stable A/B food-image generation across different host agents.

## Why this repo exists

This repository is the production release layer for the PP Food workflow. Normal production must not depend on reading the two research repositories.

## Install / startup

Read `SKILL.md`, then follow the exact runtime entry order.

Configure:
- VISION_MODEL
- IMAGE_MODEL with reference-image editing
- API base/connection
- credential in secure storage
- Stage A → Stage B image pass-through
- ability to render at least 2 B candidates from the same Stage A image
- ability for VISION_MODEL to compare multiple generated B images

When setup passes, the agent returns READY and waits for `启动`.

## Production UX

```text
执行A
```
Commercial hero photograph only.

```text
执行B
```
Quality-first B:

```text
current image
→ Stage A
→ A QC PASS
→ 3 textual art-direction candidates
→ 2 visually distinct finalists
→ render both finalists
→ VISION_MODEL compares actual images
→ select winner
→ optional targeted refinement
→ final B QC
```

The user does not need to choose between finalists.

```text
按默认文案来
```
Authorizes safe non-factual campaign copy only; never invented business facts.

## V1.4.0 B architecture

V1.4.0 addresses three failures seen in cross-agent testing:

1. **Text-only concept selection was not enough.** A concept could sound sophisticated but render poorly.
2. **Scenic concepts could demote the product.** Stage A now establishes a hero-camera baseline; B may not shrink apparent product scale by more than 15%.
3. **Category semantics were being literalized.** Bakery became oven tunnels/sign worlds, etc. V1.4 translates semantics into palette, light, material, rhythm, geometry, negative space and typography behavior instead of default themed scenery.

Upper-bound means:

```text
PRODUCT_TRUTH
+ PRODUCT_HERO_STRENGTH
+ ONE MEMORABLE PRODUCT-DERIVED IDEA
+ CATEGORY-NATIVE BUT NON-LITERAL WORLD
+ COMPOSITIONAL TENSION
+ CONTEMPORARY CAMPAIGN REFINEMENT
```

It does not mean more scenery, more props, larger typography, thicker 3D type or more text.

## Status

Version: 1.4.0

Release state: QUALITY-FIRST ARCHITECTURE COMPLETE / FINAL EXTERNAL ACCEPTANCE STILL REQUIRED.

If the host cannot render and visually compare at least two B candidates, B must be marked `DEGRADED` and may not claim stable upper-bound reproduction.