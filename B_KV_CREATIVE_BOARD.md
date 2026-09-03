# B KV Creative Board — Candidate-Based Direction

Purpose: prevent Stage B from collapsing into a safe template. The Visual Director must explore three genuinely different composition skeletons, select one, and only then compile the IMAGE_MODEL prompt.

## 1. Mandatory Internal Board

Before B prompt compilation:

```text
CURRENT_STAGE_A_PASS_IMAGE
→ CURRENT PRODUCT SEMANTICS
→ 3 CANDIDATE DIRECTIONS
→ CANDIDATE COMPARISON
→ 1 WINNER
→ COMPACT B CONTRACT
→ IMAGE_MODEL
```

The three candidates are internal planning only. Never send all three to IMAGE_MODEL.

## 2. Candidate Diversity Requirement

Each candidate must differ in **composition skeleton**, not merely surface material or title treatment.

Valid skeleton families include:

```text
FOREGROUND_COUNTER
DEEP_PORTAL
DIAGONAL_STAGE
WRAPAROUND_ARCHITECTURE
ASYMMETRIC_INSTALLATION
PRODUCT_EMBEDDED_SIGNAGE
CENTRAL_SHRINE_OR_STAGE
DEEP_CORRIDOR
PACKAGING_WORLD
SHELF_OR_WINDOW_ARCHITECTURE
FLAVOR_FLOW_FIELD
NEGATIVE_SPACE_EDITORIAL_STAGE
```

Examples of INVALID diversity:

```text
top wood sign
vs top kraft-paper sign
vs top glass sign
```

These are one skeleton with three materials.

## 3. Candidate Card

For each of exactly three candidates, resolve:

```text
CANDIDATE_ID
COMPOSITION_SKELETON
ONE_MEMORABLE_ACTION
WHY_IT_BELONGS_TO_THIS_PRODUCT
PRODUCT_HERO_STRATEGY
HEADLINE_ROLE
ATMOSPHERE_BRIDGE
DEPTH_LOGIC
LIGHTING_LOGIC
COPY_PLACEMENT_LOGIC
ANTI_TEMPLATE_RISK
```

No candidate may require product redesign.

## 4. Candidate Selection Score

Score each candidate 0–10 on:

```text
PRODUCT_DOMINANCE
CATEGORY_INEVITABILITY
THUMBNAIL_MEMORY
COMPOSITIONAL_TENSION
SPATIAL_INTEGRATION
BRAND_FIT
REFINEMENT
ANTI_TEMPLATE_ORIGINALITY
```

Weighted selection:

```text
PRODUCT_DOMINANCE          20%
CATEGORY_INEVITABILITY     15%
THUMBNAIL_MEMORY           15%
COMPOSITIONAL_TENSION      15%
SPATIAL_INTEGRATION        15%
BRAND_FIT                  5%
REFINEMENT                 10%
ANTI_TEMPLATE_ORIGINALITY  5%
```

Any candidate that fails product fidelity, product dominance, copy truth or category plausibility is eliminated regardless of score.

## 5. Safe-Template Penalty

Apply a strong penalty if the skeleton is equivalent to any known safe fallback such as:

```text
TOP_TITLE_BLOCK + CENTER_PRODUCT + BOTTOM_INFO
BIG_SIGNBOARD + CENTER_PRODUCT + SMALL_PLAQUE
PHOTO + FOOTER
```

Changing wood to paper, glass, metal, acrylic or stone does not remove the penalty if the skeleton remains the same.

## 6. Upper-Bound Definition

TRUE_UPPER_BOUND does **not** mean more elements.

```text
TRUE_UPPER_BOUND =
PRODUCT_TRUTH
+ ONE_MEMORABLE_PRODUCT-DERIVED IDEA
+ CATEGORY-NATIVE WORLD
+ COMPOSITIONAL_TENSION
+ REFINED EXECUTION
```

It may be visually restrained if restraint is the stronger choice for that category.

Do not force:
- more props;
- more copy;
- larger type;
- thicker 3D type;
- more decorative layers;
- more badges.

## 7. Winner Output

Only the winner is allowed into the B Contract:

```text
SELECTED_COMPOSITION_SKELETON
SELECTED_ONE_MEMORABLE_ACTION
SELECTED_PRODUCT_HERO_STRATEGY
SELECTED_HEADLINE_ROLE
SELECTED_ATMOSPHERE_BRIDGE
SELECTED_DEPTH_LOGIC
SELECTED_LIGHTING_LOGIC
SELECTED_COPY_PLACEMENT_LOGIC
```

Do not mention rejected candidates in the IMAGE_MODEL prompt.

## 8. Director Sanity Check

Before prompt compilation ask internally:

1. If all text were removed, would the scene still feel specifically built for this product/category?
2. If the product were replaced by a very different category, would the whole world need redesign?
3. At thumbnail size, is there one memorable product-led action?
4. Is the product still the first visual hero?
5. Is the selected skeleton genuinely different from the known safe fallback?

Any `NO` blocks B prompt compilation.
