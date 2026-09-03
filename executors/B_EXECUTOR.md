# B Executor

Purpose: transform the **current job Stage A PASS image** into a category-native professional KV while keeping the product first visual hero.

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

User-provided hard facts must be exact. Product name may serve as headline. Missing subtitle or campaign copy may only be auto-generated after explicit default-copy authorization.

Never invent business hard facts.

## Category Route

Select exactly:

```text
1 PRIMARY_CATEGORY_PROFILE
+ optional 1 WEAK_AUXILIARY_PROFILE
```

Do not activate all profiles. Brand positioning is secondary to category-native language.

## Product Hero Priority

```text
1 PRODUCT / FOOD HERO
2 HEADLINE
3 SPATIAL CONCEPT
4 SUBTITLE
5 SLOGAN / SELLING POINTS
6 BUSINESS / UTILITY INFO
```

The headline may be strong, dimensional, material, and spatial, but must not become the first hero or cover identity/appetite-critical product areas.

## Spatial Typography

Headline, subtitle, slogan, and utility information should belong to one coherent current-category spatial system. Avoid a large 3D headline with all other copy pasted flat like presentation text.

## One Big Idea

Use one thumbnail-readable campaign concept. More decorative ideas are not better.

## Generation

Compile only the fixed 6-block B prompt from `PROMPT_COMPILER.md` and use `CURRENT_JOB_STAGE_A_PASS_IMAGE` as the reference.

## Output

Deliver only after `QC_GATE.md` passes. Otherwise follow targeted retry.
