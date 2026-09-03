# B Executor

Purpose: transform the **current job Stage A PASS image** into a category-native, visually directed professional KV while keeping the product first visual hero.

## Preconditions

```text
CURRENT_JOB_STAGE_A_PASS_IMAGE exists
A_QC = PASS
COPY_GATE = PASS or DEFAULT_COPY_AUTHORIZED = TRUE
CURRENT_CATEGORY_ROUTE = RESOLVED
```

If any is missing, B is blocked.

## Copy Truth

Build:

```text
COPY_ALLOWLIST
COPY_BLOCKLIST
```

User-provided hard facts must be exact. Product name may serve as headline. Missing subtitle or campaign copy may only be auto-generated after explicit default-copy authorization. Never invent business hard facts.

## Category Route

Select exactly:

```text
1 PRIMARY_CATEGORY_PROFILE
+ optional 1 WEAK_AUXILIARY_PROFILE
```

Do not activate all profiles. Brand positioning is secondary to current category/product semantics.

## Mandatory Visual Direction

Before contract compilation:

```text
read B_KV_VISUAL_DIRECTOR.md
read B_KV_CREATIVE_BOARD.md
```

The director must:

```text
read current product semantics
→ create exactly 3 compositionally distinct candidates
→ compare candidates
→ select 1 winner
```

Do not send rejected candidates to IMAGE_MODEL.

## Candidate Gate

Before B Contract:

```text
THREE_CANDIDATES_CREATED = TRUE
CANDIDATE_SKELETONS_DISTINCT = TRUE
WINNER_SELECTED = TRUE
SELECTED_COMPOSITION_SKELETON = RESOLVED
SELECTED_ONE_MEMORABLE_ACTION = RESOLVED
PRODUCT_HERO_PROTECTION_PLAN = PASS
CATEGORY_INEVITABILITY_PLAN = PASS
THUMBNAIL_MEMORY_PLAN = PASS
ANTI_TEMPLATE_PLAN = PASS
```

A material swap does not count as a different candidate.

## Product Hero Priority

```text
1 PRODUCT / FOOD HERO
2 HEADLINE
3 SPATIAL CONCEPT
4 SUBTITLE / SLOGAN
5 AUTHORIZED SELLING POINTS
6 BUSINESS / UTILITY INFO
```

Product remains nearest/clearest/strongest recognition or appetite anchor. Typography may be strong but cannot become hero #1.

## Typography

Typography must support the selected composition. Do not optimize typography by mechanically adding more depth, more extrusion or more effects.

Required outcome:
- exact text;
- category-native behavior;
- integrated into the selected skeleton;
- no pasted footer feeling;
- no title dominance over product.

## True Upper-Bound

Default B target:

```text
TRUE_UPPER_BOUND =
PRODUCT_TRUTH
+ ONE_MEMORABLE_PRODUCT-DERIVED_IDEA
+ CATEGORY-NATIVE_WORLD
+ COMPOSITIONAL_TENSION
+ REFINED_EXECUTION
```

Upper-bound is not a decoration checklist.

## Generation

1. Complete Visual Director brief.
2. Complete 3-candidate Creative Board.
3. Select one winner.
4. Fill `executors/B_CONTRACT_TEMPLATE.md` with winner only.
5. Compile fixed 6-block B prompt from `PROMPT_COMPILER.md`.
6. Use `CURRENT_JOB_STAGE_A_PASS_IMAGE` as the only B product reference.

## Output

Deliver only after `QC_GATE.md` passes result-oriented creative and hard-truth gates. A visually safe/forgettable first attempt may fail even when typography and fidelity are correct. Otherwise follow targeted retry.
