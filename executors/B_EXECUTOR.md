# B Executor — Upper-Bound Campaign Mode

Purpose: transform the **current job Stage A PASS image** into a category-native, ingredient-atmosphere-driven, upper-bound professional KV while keeping the product first visual hero.

## Preconditions

```text
CURRENT_JOB_STAGE_A_PASS_IMAGE exists
A_QC = PASS
COPY_GATE = PASS or DEFAULT_COPY_AUTHORIZED = TRUE
CURRENT_CATEGORY_ROUTE = RESOLVED
```

If any is missing, B is blocked.

## 1. Copy Truth

Build:

```text
COPY_ALLOWLIST
COPY_BLOCKLIST
```

User-provided hard facts must be exact. Product name may serve as headline. Missing subtitle/campaign copy may only be generated after explicit default-copy authorization.

Never invent business hard facts.

## 2. Category Route

Select exactly:

```text
1 PRIMARY_CATEGORY_PROFILE
+ optional 1 WEAK_AUXILIARY_PROFILE
```

Do not activate all profiles. Brand positioning is secondary to category-native language.

## 3. Mandatory KV Visual Director

Before contract compilation, read and execute:

```text
B_KV_VISUAL_DIRECTOR.md
```

The current-job brief must resolve:

```text
VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >= 3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
HEADLINE_SPATIAL_FORM = RESOLVED
SHARED_COMPOSITION_LOGIC = PASS
INFORMATION_RHYTHM_PLAN = RESOLVED
PRODUCT_HERO_PROTECTION_PLAN = PASS
FOREGROUND_PLAN = PASS
MIDGROUND_PLAN = PASS
BACKGROUND_PLAN = PASS
LIGHTING_DRAMA_PLAN = PASS
MATERIAL_DEPTH_PLAN = PASS
ANTI_FLATNESS_PLAN = PASS
ANTI_TEMPLATE_DIFFERENTIATION = PASS
```

If any is missing or vague, B is blocked.

## 4. Default Output Standard

```text
KV_MODE = TRUE_UPPER_BOUND
```

Every category outputs its own upper-bound language by default. The system does not reserve upper-bound treatment for explicit user requests.

Upper-bound means more resolved, more category-specific and more spatial — not simply larger typography, more props or more effects.

## 5. Product Hero Priority

```text
1 PRODUCT / FOOD HERO
2 HEADLINE
3 SPATIAL CONCEPT
4 SUBTITLE
5 SLOGAN / SELLING POINTS
6 BUSINESS / UTILITY INFO
```

The product must remain the first visual read. The headline may be strong, dimensional and spatial, but may not become visual priority #1 or cover identity/appetite-critical product areas.

## 6. Spatial Typography Hard Rule

Headline must exhibit at least 3 of:

```text
PERSPECTIVE
VOLUME / DEPTH
CATEGORY-NATIVE MATERIALITY
SPATIAL ATTACHMENT TO SCENE
```

Headline, subtitle, slogan, selling points and utility information belong to one coherent current-category spatial system.

The output must not read as:

```text
Stage A photo + bottom headline card + flat footer
```

That is `ANTI_FLATNESS_FAIL`.

## 7. Anti-Template Hard Rule

Do not default to:

```text
large signboard above
product centered below
small brand plaque at bottom
```

unless current product semantics uniquely justify that structure.

The director must create a product-derived differentiator. If a different category could replace the current product with minimal redesign:

```text
ANTI_TEMPLATE_DIFFERENTIATION = FAIL
```

## 8. One Big Idea

Use exactly one thumbnail-readable campaign action derived from the current product/category. It must alter the spatial composition, not merely describe mood.

Examples of action grammar: counter-front structure, material lintel, wall relief, suspended installation, flavor wave, steam corridor, glass installation, acrylic window, packaging plane, light architecture, table-edge structure, serving-geometry extension.

## 9. Three-Depth Stage

B must deliberately establish:

```text
FOREGROUND = near-camera framing / material edge / controlled overlap
MIDGROUND = PRODUCT HERO + main light pool + main title relationship
BACKGROUND = category-native architecture + recession + light/material depth
```

At least two independent depth cues beyond the product are required.

Props are optional and subordinate. Depth must come mainly from architecture, material planes, perspective, light and occlusion.

## 10. Lighting Drama

Lighting must translate product semantics:

- baked/crisp → grazing warm texture light;
- brothy/hot → liquid highlights + steam separation;
- cold/transparent → refractive edge light + condensation clarity;
- creamy/dessert → soft sculpting + elegant gradients;
- premium seafood → restrained precise speculars;
- retail package → contour light + pack-face readability.

Lighting may not change product truth or surface state.

## 11. Information Rhythm

When authorized copy is sufficient, organize differentiated levels instead of one footer stack:

```text
L1 PRODUCT HERO
L2 HEADLINE
L3 SUBTITLE / SLOGAN
L4 SELLING POINTS
L5 BRAND / STORE / ADDRESS / PHONE / QR / UTILITY
```

Sparse factual content remains sparse. Never fabricate hard facts for density.

## 12. Generation

1. Complete current Visual Director brief.
2. Fill `executors/B_CONTRACT_TEMPLATE.md`.
3. Compile only the fixed 6-block B prompt from `PROMPT_COMPILER.md`.
4. Use `CURRENT_JOB_STAGE_A_PASS_IMAGE` as the only B product reference.
5. Generate.
6. Run full B QC including upper-bound, anti-flatness and anti-template gates.
7. Targeted retry only.

## 13. Output

Deliver only after `QC_GATE.md` passes all hard gates. A visually attractive but template-like, flat or weakly differentiated KV is not PASS.