# B KV Visual Director — Upper-Bound Edition

Purpose: make every Stage B output a **category-native, ingredient-atmosphere-driven, upper-bound campaign KV**, not a commercial photo with decorative text.

This file is production-critical for B.

## 1. Mandatory Pipeline Position

```text
CURRENT_JOB_STAGE_A_PASS_IMAGE
→ B_KV_VISUAL_DIRECTOR
→ B_CONTRACT
→ B_PROMPT_COMPILER
→ IMAGE_MODEL
→ B_QC
```

Skipping the director brief is a B critical failure.

## 2. Director Inputs

Use current-job evidence only:

```text
Stage A PASS image
user-provided product / dish name
user-provided brand / store information
current COPY_ALLOWLIST / COPY_BLOCKLIST
current category profile
reliably visible ingredient / product / package semantics
```

Previous-job visual skin, typography, props, palette, slogans and spatial devices are OFF unless the user explicitly requests continuity.

## 3. Required Director Brief

Resolve before B generation:

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
ATMOSPHERE_EVIDENCE >= 3
ONE_BIG_IDEA
HEADLINE_SPATIAL_FORM
SHARED_COMPOSITION_LOGIC
INFORMATION_RHYTHM_PLAN
PRODUCT_HERO_PROTECTION_PLAN
FOREGROUND_PLAN
MIDGROUND_PLAN
BACKGROUND_PLAN
LIGHTING_DRAMA_PLAN
MATERIAL_DEPTH_PLAN
ANTI_TEMPLATE_DIFFERENTIATION
```

The brief is internal. The user does not fill a form.

## 4. Ingredient / Atmosphere Derivation

The campaign world must be traceable to the current product.

```text
PRODUCT SEMANTICS
→ ATMOSPHERE
→ MATERIALS
→ LIGHT
→ COLOR
→ TYPOGRAPHY PERSONALITY
→ SPATIAL ACTION
→ INFORMATION RHYTHM
```

Valid evidence includes ingredient identity, source colors, hot/cold state, crisp/soft/juicy/creamy/chewy/brothy/refreshing/smoky character, cooking/serving process when supported, regional context, packaging material, and brand positioning.

Do not start from generic adjectives such as `premium`, `cinematic`, `luxury`, `warm`, `modern`, or `energetic` without product-derived evidence.

## 5. Upper-Bound Means Resolved, Not Louder

Every B defaults to:

```text
KV_MODE = TRUE_UPPER_BOUND
```

Upper-bound means:

- product remains first hero;
- category-native environment is unmistakable;
- title material and spatial form are category-native;
- one memorable spatial action exists at thumbnail size;
- foreground / midground / background are intentionally designed;
- light and material depth feel campaign-grade;
- text hierarchy has rhythm, not a footer stack;
- the result could not be reused for a different food category without major redesign.

Upper-bound does **not** mean giant type, more badges, more props, stronger saturation, more smoke, or more decorative objects.

## 6. One Big Idea — Mandatory and Specific

Every B chooses exactly one dominant spatial action. Mood labels are invalid.

Valid action grammar includes:

```text
headline_as_bakery_sign
headline_as_counter_front
headline_as_material_lintel
headline_as_wall_relief
headline_as_suspended_installation
headline_as_flavor_wave
headline_as_steam_corridor
headline_as_glass_installation
headline_as_acrylic_window
headline_as_packaging_plane
headline_as_brand_display_structure
headline_as_light_architecture
headline_as_table_edge_structure
headline_as_serving_geometry_extension
```

The action must be justified by current category and ingredient semantics.

`ONE_BIG_IDEA = premium bakery atmosphere` is invalid.

## 7. Anti-Template Rule

The director must not choose the same safe structure simply because it worked previously.

The following default repetition is forbidden unless uniquely justified by the current product:

```text
large signboard above product
product centered below
small brand plaque at bottom
```

For each job, ask:

> If another product in another category replaced this product, would this composition still work with minimal changes?

If YES:

```text
ANTI_TEMPLATE_DIFFERENTIATION = FAIL
```

Rebuild the spatial action from current ingredient/category evidence.

## 8. Anti-Flatness Hard Gate

The following are B FAIL:

- headline exists only as a bottom horizontal strip;
- product sits above and all typography is isolated in a footer;
- all text occupies one flat plane;
- headline is merely text on a rectangular card with no scene integration;
- headline has no meaningful perspective, volume, materiality, or spatial attachment;
- no explicit spatial campaign action exists;
- design reads as `Stage A photo + text overlay` at thumbnail size;
- title and product can be separated into two independent rectangles with almost no loss.

Headline must exhibit at least **3 of 4**:

```text
PERSPECTIVE
VOLUME / DEPTH
CATEGORY-NATIVE MATERIALITY
SPATIAL ATTACHMENT TO SCENE
```

## 9. Product Hero Protection

```text
PRODUCT_PRIORITY = 1
HEADLINE_PRIORITY = 2
```

Product must be the nearest, clearest, strongest recognition/appetite anchor. Headline is the second anchor.

Forbidden:
- shrinking product to create title space;
- pushing product into background or corner;
- using product as wallpaper;
- covering identity/appetite-critical areas;
- giant typography becoming first read;
- using product merely as a prop for typography.

When tension conflicts with product truth:

```text
REDUCE_DESIGN_AGGRESSION = TRUE
REDUCE_PRODUCT_DOMINANCE = NEVER
```

## 10. Shared Composition Logic

Product and typography must feel directed in one shot. Use one or more of:

- shared perspective / vanishing field;
- title anchored to product support plane;
- title acting as stage, lintel, counter, window, light architecture, corridor or material plane;
- product lightly overlaps or occludes the title system;
- steam, condensation, ingredients, packaging, shadows or light connect product and type;
- title orientation echoes product geometry or food movement.

If product and title could be cut apart and pasted separately with little loss:

```text
SHARED_COMPOSITION_LOGIC = FAIL
```

## 11. Three-Depth Campaign Stage

Every upper-bound B must deliberately create:

```text
FOREGROUND = near-camera framing / material edge / tag / controlled overlap / atmospheric entry
MIDGROUND = PRODUCT HERO + main light pool + key title relationship
BACKGROUND = category-native architecture / recession / material depth / light separation
```

At least two independent depth cues must exist beyond the product: perspective recession, scale falloff, occlusion, defocus, light falloff, material planes, suspended elements, or shadow architecture.

Do not create depth mainly by adding random props.

## 12. Lighting Drama

Lighting must reinforce the food/property semantics, not merely make the scene darker or warmer.

Examples:
- baked/crisp → grazing highlights, oven/morning directional warmth, crust texture readability;
- brothy/hot → steam separation, liquid specularity, heat glow without obscuring ingredients;
- cold/transparent → refractive edge light, condensation sparkle, cool-clear negative space;
- creamy/dessert → soft sculpting, elegant gradients, controlled sheen;
- premium seafood → restrained specular precision and cool refined depth;
- packaged retail → label clarity, contour light, pack-face legibility, shelf/display architecture.

## 13. Information Rhythm

When enough authorized copy exists, organize differentiated levels:

```text
L1 PRODUCT HERO
L2 HEADLINE
L3 SUBTITLE / SLOGAN
L4 SELLING POINTS
L5 BRAND / STORE / ADDRESS / PHONE / QR / UTILITY
```

Do not fabricate facts to fill levels. Sparse copy may stay sparse.

Default-copy authorization may generate only safe non-factual campaign/sensory copy.

Use category-appropriate carriers: shelf labels, hanging tags, side panels, glass strips, seals, paper bands, wall relief, packaging extensions, perspective micro-cards, projected light fields, etc.

## 14. Category-Native Upper-Bound Cues

### CN_HOME_STYLE
Signals: wok heat, sauce, homestyle abundance, Chinese dining energy.
World: warm wood/stone/dark metal, steam depth, bold Chinese display/signage integrated into architectural surfaces.
Avoid: dessert glass-ribbon minimalism, generic luxury banquet gold without dish evidence.

### SPICY_HOT
Signals: chili/pepper/aromatic heat, red-green contrast, fast flavor impact.
World: dark stone/metal/lacquer, dynamic diagonal or heat-wave spatial action, vapor/ingredient motion used selectively.
Avoid: safe centered signboard, western editorial restraint.

### CLAYPOT_SOUP
Signals: broth, clay/copper vessel, hearth warmth, steam, slow simmer.
World: hearth-like depth, warm stone/clay/copper surfaces, title as hearth lintel / vessel-edge architecture / steam corridor.
Avoid: beverage acrylic world or unrelated neon.

### NOODLE_RICE_NOODLE
Signals: bowl geometry, broth, noodle trajectories, staple-food satisfaction, steam.
World: upward movement, bowl-perspective rhythm, signage/lintel/corridor logic tied to steam or noodle flow.
Avoid: cake editorial skin or static flat title card.

### BBQ_NIGHTMARKET
Signals: char, fire, frying, smoke, skewers, night energy.
World: blackened metal/charcoal/signage/lightbox structures, hard diagonals, fire/smoke depth with controlled contrast.
Avoid: soft morning bakery or luxury hotel banquet styling.

### SEAFOOD_PREMIUM
Signals: delicacy, freshness, translucency, refined plating, banquet premium.
World: blue-gray stone, jade, metal, glass, restrained elegant typography, clean negative space and precise specular light.
Avoid: rough nightmarket signage, oversized rustic wood title.

### DESSERT_CAKE
Signals: cream, softness, floral/tea notes, cold/airy delicacy, layered texture.
World: cream relief, glass/acrylic/ribbon architecture, refined editorial type, sculptural negative space.
Avoid: Chinese restaurant plaque behavior, heavy rustic wood.

### COFFEE_TEA_BEVERAGE
Signals: liquid transparency, ice, condensation, fruit/tea color, freshness.
World: glass/acrylic/jelly/light architecture, window-light depth, translucent title forms, refreshing negative space.
Avoid: hot-food smoke, dense wooden restaurant signage.

### WESTERN_DINING
Signals: sear, sauce, refined plating, linen/stone/silver service.
World: editorial stone/linen/silver, high-contrast serif + clean sans, restrained architectural staging.
Avoid: Chinese brush-gold signage or nightmarket graphics.

### JAPANESE_KOREAN
Signals: order, geometry, clean cuts, wood/paper/stone, restrained modernity.
World: modular geometry, narrow/minimal sans, sliding-plane or paper/wood architecture, calm controlled depth.
Avoid: heavy banquet spectacle or ornate western luxury.

### BAKERY_BREAKFAST
Signals: baked crust, grain, handcraft, morning light, paper/wood warmth.
World: bakery wood, kraft paper, warm stone, oven/window light; actions can include counter-front, bread-rack architecture, paper emboss, oven lintel, hanging bakery mark, shelf-edge perspective.
Avoid: repeating the same giant top signboard on every bread product; generic coffee props; Chinese restaurant signboard.

### RETAIL_PACKAGED
Signals: pack silhouette, label, brand color, contents, retail conversion.
World: brand display architecture, plinth/shelf/window/light structure, packaging-plane extensions; pack remains dominant hero.
Avoid: restaurant serving conversion, package redesign, decorative food world that hides the pack.

## 15. Director Pass Condition

Before B prompt compilation:

```text
VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >= 3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
HEADLINE_SPATIAL_FORM = RESOLVED
SHARED_COMPOSITION_LOGIC = PASS
PRODUCT_HERO_PROTECTION_PLAN = PASS
FOREGROUND_PLAN = PASS
MIDGROUND_PLAN = PASS
BACKGROUND_PLAN = PASS
LIGHTING_DRAMA_PLAN = PASS
MATERIAL_DEPTH_PLAN = PASS
ANTI_FLATNESS_PLAN = PASS
ANTI_TEMPLATE_DIFFERENTIATION = PASS
```

Any missing field blocks B generation.