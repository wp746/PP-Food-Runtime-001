# B Executor — Quality-First Visual Audition

Purpose: produce a world-class, product-led KV from the **current job Stage A PASS image**. Stage B is not allowed to rely on planning prose or self-scored checklists; it must compare actual candidate renders.

## Preconditions

```text
CURRENT_JOB_STAGE_A_PASS_IMAGE exists
A_QC = PASS
COPY_GATE = PASS or DEFAULT_COPY_AUTHORIZED = TRUE
CURRENT_CATEGORY_ROUTE = RESOLVED
VISION_MODEL can inspect generated images
IMAGE_MODEL can generate at least 2 candidate B images from the same Stage A PASS image
```

If rendered candidate comparison is unavailable, B may still run in degraded mode only if the user explicitly accepts reduced reproducibility. Do not label degraded mode as upper-bound stable.

## 1. Copy Truth

Build `COPY_ALLOWLIST` and `COPY_BLOCKLIST` from current-job truth only. User-provided hard facts must be exact. Default-copy authorization permits safe non-factual campaign copy only.

## 2. Category Route

Select exactly:

```text
1 PRIMARY_CATEGORY_PROFILE
+ optional 1 WEAK_AUXILIARY_PROFILE
```

Do not activate all profiles or inherit previous-job skin.

## 3. Mandatory Director Stack

Read and execute:

```text
B_KV_VISUAL_DIRECTOR.md
B_KV_CREATIVE_BOARD.md
B_KV_VISUAL_AUDITION.md
```

Pipeline:

```text
Stage A PASS
→ 3 textual art-direction candidates
→ select 2 visually distinct finalists
→ render finalist A
→ render finalist B
→ VISION_MODEL compares actual images
→ select winner
→ optional targeted refinement
→ final B QC
```

The user does not need to choose between finalists.

## 4. Stage A Hero Camera Lock

```text
PRODUCT_APPARENT_SCALE_SHRINK_FROM_STAGE_A <= 15%
PRODUCT = FIRST VISUAL READ
ENVIRONMENT = SUPPORTING
HEADLINE = SECOND VISUAL READ
```

Reject any concept where a tunnel, arch, room, signboard, shelf, wall or scene becomes more visually important than the product.

## 5. Non-Literal Category Translation

Translate food semantics into palette, light, material, rhythm, geometry and type behavior. Do not illustrate the category as a theme park set.

Examples:
- bakery: refined warmth, crust light, restrained wood/stone/paper cues; not automatically old ovens, caves or giant rustic signs;
- dessert: elegance and soft materiality; not automatically acrylic props everywhere;
- beverage: freshness/translucency; not automatically jelly text;
- hot bowl: heat/steam rhythm; not automatically a steam corridor.

## 6. Contemporary Campaign Standard

Prefer controlled materials, designed negative space, product tactile clarity, selective scale contrast, sophisticated lighting and one memorable gesture.

Reject theatrical literalism, prop piles, rustic overload, brown-on-brown monotony, menu-board aesthetics and environment-first compositions.

## 7. Typography

Typography supports the selected visual strategy. It may be dimensional or restrained.

Hard outcome:
- exact text;
- product remains hero #1;
- type is integrated but not dominant;
- no footer fallback;
- no menu/signage feeling unless genuinely appropriate;
- no product shrinkage to create title space.

## 8. Two Rendered Finalists

Both finalists use the same Stage A PASS image, product truth and copy truth, but differ in composition skeleton, negative-space strategy, headline role, depth logic, material family and lighting behavior.

At least one finalist should be restrained/editorial unless clearly inappropriate.

## 9. Visual Selection

VISION_MODEL compares actual renders using `B_KV_VISUAL_AUDITION.md`.

Winner must outperform the other candidate in:
- product hero strength;
- campaign refinement;
- memorability;
- category inevitability;
- typography integration;
- compositional tension.

A textually clever concept cannot win if the rendered image is weaker.

## 10. Final Refinement

If the winner has a local weakness, run one targeted refinement while preserving:

```text
WINNING_COMPOSITION
PRODUCT_POSITION/SCALE
PRODUCT_TRUTH
COPY_TRUTH
```

Do not replace the winner with a new concept during refinement.

## 11. Output

Deliver only after `QC_GATE.md` passes hard truth, hero preservation, contemporary-campaign and visual-result gates.

A technically correct but themed, scenic, environment-led or merely polite poster is FAIL.