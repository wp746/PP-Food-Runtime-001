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

User-provided hard facts must be exact. Product name may serve as headline. Missing subtitle or campaign copy may only be auto-generated after explicit default-copy authorization.

Never invent business hard facts.

## Category Route

Select exactly:

```text
1 PRIMARY_CATEGORY_PROFILE
+ optional 1 WEAK_AUXILIARY_PROFILE
```

Do not activate all profiles. Brand positioning is secondary to category-native language.

## Mandatory KV Visual Director

Before contract compilation, read and execute:

```text
B_KV_VISUAL_DIRECTOR.md
```

Create the current-job director brief from:

```text
category
core ingredients / materials
temperature
texture / mouthfeel
process / serving cue
regional-cultural cue when supported
brand positioning
product-derived atmosphere evidence
```

The brief must resolve:

```text
VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >= 3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
HEADLINE_SPATIAL_FORM = RESOLVED
SHARED_COMPOSITION_LOGIC = RESOLVED
INFORMATION_RHYTHM_PLAN = RESOLVED
PRODUCT_HERO_PROTECTION_PLAN = PASS
ANTI_FLATNESS_PLAN = PASS
```

If the director brief is missing or vague, B is blocked.

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

## Spatial Typography Hard Rule

Headline must exhibit at least 3 of:

```text
PERSPECTIVE
VOLUME / DEPTH
CATEGORY-NATIVE MATERIALITY
SPATIAL ATTACHMENT TO SCENE
```

Headline, subtitle, slogan, selling points and utility information belong to one coherent current-category spatial system. Avoid a large 3D headline with all other copy pasted flat like presentation text.

The B result must not read as:

```text
Stage A commercial photo
+ bottom headline card
+ flat footer information
```

That pattern is `ANTI_FLATNESS_FAIL`.

## One Big Idea

Use exactly one thumbnail-readable campaign action derived from the current product/category. Examples are action grammar, not templates: bakery sign, counter front, paper emboss, steam corridor, flavor wave, glass installation, packaging plane, brand display structure.

Vague mood words alone are not a valid One Big Idea.

## Shared Composition Logic

Product and typography must share a deliberate composition relationship: perspective field, support plane, stage structure, overlap, atmosphere bridge, geometry echo, or another director-approved current-category relationship.

If product and copy occupy unrelated independent zones, retry B.

## Generation

1. Complete the Visual Director brief.
2. Fill `executors/B_CONTRACT_TEMPLATE.md`.
3. Compile only the fixed 6-block B prompt from `PROMPT_COMPILER.md`.
4. Use `CURRENT_JOB_STAGE_A_PASS_IMAGE` as the reference.

## Output

Deliver only after `QC_GATE.md` passes, including KV tension and anti-flatness gates. Otherwise follow targeted retry.
