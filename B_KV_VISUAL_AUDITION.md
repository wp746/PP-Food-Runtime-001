# B KV Visual Audition — Rendered Candidate Selection

Purpose: stop the runtime from selecting a textually clever but visually weak concept. Stage B quality is judged from rendered evidence, not from planning prose alone.

## 1. Quality-First Default

For normal B production:

```text
B_QUALITY_MODE = VISUAL_AUDITION
```

After Stage A PASS and director planning, create **2 visually distinct B candidate renders** from the same Stage A PASS image. They must use different composition skeletons and different art-direction strategies.

Do not ask the user to choose. VISION_MODEL compares the two renders and selects the stronger one.

If the runtime cannot create at least 2 candidate renders and compare them visually, mark:

```text
B_VISUAL_AUDITION_CAPABILITY = UNAVAILABLE
```

and do not claim deterministic upper-bound reproduction.

## 2. Stage A Hero Camera Lock

Both candidate renders must preserve the Stage A hero scale and visual authority.

```text
PRODUCT_APPARENT_SCALE_SHRINK_FROM_STAGE_A <= 15%
PRODUCT_HERO_POSITION = PRIMARY
PRODUCT_SUPPORT_GEOMETRY = PRESERVED_OR_STRONGLY_RELATED
SCENE_DRAMA_MAY_NOT_PUSH_PRODUCT_DEEP_INTO_BACKGROUND
```

A portal, arch, corridor, room, wall, shelf or architecture concept is automatically rejected when the environment becomes the primary subject and the product reads as an object placed inside a set.

## 3. Non-Literal Art Direction

Category semantics are translated, not illustrated literally.

Examples:
- bakery does not automatically become an old oven tunnel, rustic cave, giant wood sign or kraft-paper world;
- hot noodles do not automatically become a steam corridor;
- seafood does not automatically become blue glass luxury;
- dessert does not automatically become acrylic/ribbon decoration.

Use food semantics as **design cues** for palette, surface, light, rhythm, geometry and typography. Avoid theatrical set-building unless the set directly strengthens product hero status.

## 4. Contemporary Campaign Filter

Every candidate must pass a contemporary commercial-art filter:

```text
PRODUCT_LED = TRUE
VISUAL_HIERARCHY = CLEAN
MATERIAL_COUNT = CONTROLLED
COLOR_PALETTE = CONTROLLED
PROP_DEPENDENCE = LOW
DECORATIVE_LITERALISM = LOW
BRAND/CATEGORY_FIT = HIGH
EDITORIAL_REFINEMENT = HIGH
```

Reject candidates that feel:
- theme-park;
- medieval/rustic theatrical;
- menu-board-like;
- souvenir-shop-like;
- overly literal;
- prop-heavy;
- brown-on-brown with weak hierarchy;
- environment-first rather than product-first.

## 5. Candidate A / B Requirements

Each candidate uses the same product truth and copy truth, but must differ in:

```text
COMPOSITION_SKELETON
PRIMARY_NEGATIVE_SPACE_STRATEGY
HEADLINE_ROLE
DEPTH_LOGIC
MATERIAL_FAMILY
LIGHTING_BEHAVIOR
```

At least one candidate should be **restrained/editorial** rather than architectural. This prevents the system from assuming that “world-class” always means more scenery.

## 6. Visual Comparison — No Self-Justification

VISION_MODEL compares the actual candidate images, not the written briefs.

Score 0–100:

```text
PRODUCT_HERO_STRENGTH        25
CAMPAIGN_REFINEMENT          20
MEMORABILITY                 15
CATEGORY_INEVITABILITY       15
TYPOGRAPHY_INTEGRATION       10
COMPOSITIONAL_TENSION        10
ANTI_TEMPLATE_ORIGINALITY     5
```

Any candidate fails immediately if:
- product is visibly smaller/weaker than Stage A by more than allowed;
- environment is the first read;
- concept looks like a literal themed set;
- headline dominates product;
- text accuracy fails;
- product/package fidelity fails.

## 7. Final Refinement Pass

Select the stronger render. Then perform **one targeted refinement pass only if needed**, preserving the chosen composition and product placement.

Allowed refinement targets:
- hierarchy;
- typography fit;
- material restraint;
- lighting balance;
- utility-copy placement;
- product emphasis.

Do not replace the winning composition with a new concept during refinement.

## 8. Pass Condition

```text
TWO_RENDERED_CANDIDATES = TRUE
CANDIDATES_VISUALLY_DISTINCT = TRUE
STAGE_A_HERO_CAMERA_LOCK = PASS
NON_LITERAL_ART_DIRECTION = PASS
CONTEMPORARY_CAMPAIGN_FILTER = PASS
VISION_MODEL_VISUAL_COMPARISON = PASS
WINNING_RENDER_SELECTED = TRUE
```

Without these, do not claim upper-bound B stability.