# B KV Visual Director

Purpose: prevent Stage B from degrading into **commercial photo + pasted text**. Before B prompt compilation, the host must direct one category-native campaign world from the current product truth.

This file is production-critical for B.

## 1. Mandatory Position In Pipeline

```text
CURRENT_JOB_STAGE_A_PASS_IMAGE
→ B_KV_VISUAL_DIRECTOR
→ B_CONTRACT
→ B_PROMPT_COMPILER
→ IMAGE_MODEL
→ B_QC
```

Skipping the visual-director brief is a B critical failure.

## 2. Visual Director Inputs

Use only current-job evidence:

```text
Stage A PASS image
user-provided product / dish name
user-provided brand / store information
current COPY_ALLOWLIST
current category profile
reliably visible food / material semantics
```

Never import a previous job's visual skin.

## 3. Director Brief — Required Fields

Before B generation, resolve:

```text
FOOD_CATEGORY
CORE_INGREDIENT_OR_MATERIAL_SEMANTICS
TEMPERATURE_ATTRIBUTE
TEXTURE_MOUTHFEEL_ATTRIBUTE
PROCESS_OR_SERVING_CUE
REGIONAL_CULTURAL_CUE = RESOLVED_OR_NA
BRAND_POSITIONING
PRIMARY_VISUAL_MOOD
PRIMARY_COLOR_LOGIC
TITLE_MATERIAL_LANGUAGE
FORBIDDEN_STYLE_LANGUAGE
ONE_BIG_IDEA
HEADLINE_SPATIAL_FORM
SHARED_COMPOSITION_LOGIC
INFORMATION_RHYTHM_PLAN
PRODUCT_HERO_PROTECTION_PLAN
ATMOSPHERE_EVIDENCE >= 3
```

The director brief is internal; the user does not need to fill a form.

## 4. Ingredient / Atmosphere Derivation

The visual world must be traceable to at least three current-job signals. Valid evidence includes:

- ingredient identity or packaging material;
- source color family;
- hot / cold state;
- crisp / soft / juicy / creamy / chewy / brothy / refreshing / smoky character;
- cooking or serving process if supported;
- cuisine / regional context if supplied or reliable;
- brand positioning.

```text
PRODUCT_SEMANTICS → ATMOSPHERE → MATERIALS → LIGHT → TYPOGRAPHY → SPATIAL_ACTION
```

Do not begin from generic adjectives such as `premium`, `cinematic`, `luxury`, `warm`, or `energetic` without product-derived evidence.

## 5. One Big Idea Is Mandatory

Every B job chooses exactly one dominant spatial campaign action.

Examples of action grammar:

```text
headline_as_bakery_sign
headline_as_counter_front
headline_as_wood_plaque
headline_as_paper_emboss
headline_as_restaurant_sign
headline_as_architectural_lintel
headline_as_flavor_wave
headline_as_steam_corridor
headline_as_glass_installation
headline_as_acrylic_window
headline_as_packaging_plane
headline_as_brand_display_structure
```

These are methods, not fixed templates. The chosen action must be derived from the current product/category.

`ONE_BIG_IDEA = premium bakery atmosphere` is invalid because it describes mood, not an action.

## 6. Anti-Flatness Hard Gate

The following are B FAIL:

- headline exists only as a bottom horizontal strip;
- product is above and all typography is isolated in an unrelated footer;
- all text occupies one flat plane;
- headline is merely embossed text on a rectangular card with no composition integration;
- headline has no meaningful perspective, volume, materiality, or spatial attachment;
- no explicit spatial campaign action exists;
- design reads as `Stage A photo + text overlay` at thumbnail size.

Headline must exhibit at least **3 of 4**:

```text
PERSPECTIVE
VOLUME / DEPTH
CATEGORY-NATIVE MATERIALITY
SPATIAL ATTACHMENT TO SCENE
```

At the same time:

```text
PRODUCT_PRIORITY = 1
HEADLINE_PRIORITY = 2
```

Anti-flatness never authorizes title dominance.

## 7. Shared Composition Logic

Product and typography must feel directed in one shot.

Use at least one strong relationship:

- shared vanishing / perspective field;
- headline anchored to product support plane;
- headline forms a stage, lintel, sign, counter, window, corridor or material plane around the product;
- product overlaps or lightly occludes the title system;
- atmosphere, steam, condensation, ingredients, packaging or light connects product and type;
- title orientation echoes product geometry or movement.

If product and text could be separated into two independent rectangles with almost no loss, `SHARED_COMPOSITION_LOGIC = FAIL`.

## 8. Product Hero Protection

The director must protect product dominance while increasing design pressure.

```text
PRODUCT = nearest / clearest / strongest appetite or recognition anchor
HEADLINE = second anchor
COPY_SYSTEM = supporting hierarchy
```

Forbidden:

- shrinking product to create title space;
- pushing product into background/corner;
- using product as decorative wallpaper;
- covering identity or appetite-critical areas;
- letting giant typography become first visual read.

When tension conflicts with product truth:

```text
REDUCE_TYPOGRAPHY_AGGRESSION = TRUE
REDUCE_PRODUCT_DOMINANCE = NEVER
```

## 9. Information Rhythm

When sufficient user-authorized copy exists, organize it as differentiated levels rather than one footer stack:

```text
L1 PRODUCT HERO
L2 HEADLINE
L3 SUBTITLE / SLOGAN
L4 SELLING POINTS
L5 BRAND / STORE / ADDRESS / PHONE / QR / UTILITY
```

Not every level requires equal visual weight. Sparse copy should remain sparse; do not fabricate facts to fill levels.

Use different spatial media where category-appropriate: tag, seal, shelf label, glass strip, wall plaque, hanging sign, side panel, perspective-aligned micro-card, packaging label extension, etc.

## 10. Category-Native Director Cues

### Bakery / Breakfast

Signals: baked crust, grain, morning, handcraft, warm aroma.

Prefer: bakery wood, kraft paper, warm stone, oven/window light; title as bakery sign, wood plaque, paper emboss, counter front, packaging tag.

Avoid: generic coffee props, Chinese restaurant gold brush signboard, technology neon.

### Noodles / Rice Noodles / Hot Bowls

Signals: hot broth, staple-food energy, upward steam, bowl geometry.

Prefer: rising movement, steam depth, signage/lintel/corridor logic, strong Chinese display structure when culturally appropriate.

Avoid: dessert editorial glass/ribbon skin.

### Fresh-Spicy / Sour / Pepper Fish

Signals: fresh heat, pepper/aromatic herbs, sourness, bright broth, green/yellow/red flavor cues when supported.

Prefer: fluid heat, clear steam, ingredient-derived color accents, dynamic sign/steam/flavor-wave spatial structure.

Avoid: bakery wood-world default or unrelated heavy banquet gold.

### Dessert / Cake

Signals: cream, softness, tea/floral notes, cold/airy delicacy.

Prefer: glass, acrylic, ribbon, cream relief, refined editorial typography, airy depth.

Avoid: heavy restaurant signboard behavior.

### Cold Beverage / Fruit Ice

Signals: transparency, condensation, ice, juice, freshness.

Prefer: translucent glass/acrylic/jelly media, window light, refreshing negative space, liquid/fruit geometry.

Avoid: hot-food steam or heavy wood restaurant language.

### Retail Packaged

Signals: pack silhouette, label, brand colors, contents, retail conversion.

Prefer: brand display architecture, plinth/shelf/window structures, packaging-plane extensions; pack remains hero.

Avoid: restaurant serving conversion or package redesign.

Other categories follow the selected current profile using the same derivation logic.

## 11. Director Pass Condition

Before B prompt compilation:

```text
VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >= 3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
HEADLINE_SPATIAL_FORM = RESOLVED
SHARED_COMPOSITION_LOGIC = RESOLVED
PRODUCT_HERO_PROTECTION_PLAN = PASS
ANTI_FLATNESS_PLAN = PASS
```

Any missing field blocks B generation.
