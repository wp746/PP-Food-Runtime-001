# QC Gate

VISION_MODEL performs post-generation QC. Do not accept an output because it is merely attractive.

## A QC

```text
Aspect Ratio = EXACT 9:16
Food / Product Identity >=95
Ingredient / Product Geometry >=95
Vessel / Container / Packaging >=98
Plating / Arrangement >=95
Physical Relationships >=95
Source Surface State = PASS
Photography >=85
Semantic Relevance >=85
Hero Spatial >=85
Appetite >=85
Critical Failure = NONE
```

Critical A failures include product replacement, ingredient drift, packaging drift, vessel drift, re-cooking/surface-state drift, unsupported additions, generic template background, impossible temperature effects, or non-9:16 delivery.

## B QC — Upper-Bound Default

```text
Stage B Reference = CURRENT_JOB_STAGE_A_PASS_IMAGE
Food / Product Fidelity >=95
Vessel / Packaging Fidelity >=98
Typography Accuracy =100%
Product Dominance = PASS
Category Visual Language >=90
Typography-Category Match >=13/15
Spatial Language Match >=13/15
Full Text-System Spatiality >=9/10
KV Design Quality >=90
Previous-Skin Contamination = FALSE
Upper-Bound Readiness >=92

VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >=3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
Title Spatiality >=90
Visual Tension >=90
Shared Composition Logic >=90
Three-Depth Stage >=90
Lighting Drama >=88
Material Depth >=88
Category-Specific Differentiation >=90
Information Rhythm >=85 when sufficient copy exists
Anti-Flatness = PASS
Anti-Template = PASS
```

Product remains first visual hero. Headline is second.

## B Critical Failures

Any of these immediately blocks PASS:

- Stage A photo plus a bottom text panel is the dominant layout logic;
- headline is a flat/shallow strip detached from product world;
- product and typography occupy unrelated independent zones;
- all copy sits on one footer plane;
- title lacks at least 3 of perspective / volume / category-native materiality / spatial attachment;
- no concrete One Big Idea can be identified at thumbnail scale;
- design defaults to `large signboard above + product centered below + small plaque bottom` without product-specific justification;
- a different food category could replace the product with minimal redesign;
- depth is faked mainly by random props instead of spatial planes, perspective, occlusion and light;
- typography is accurate but KV still reads as polite, generic or template-flat;
- title becomes first hero and product is demoted;
- upper-bound pressure changes product, packaging, surface state or plating truth.

## B Evaluation Dimensions

### Title Spatiality
Headline behaves as a real scene element: lintel, counter structure, relief, suspended installation, glass/acrylic plane, flavor wave, packaging extension, light architecture, serving-geometry extension, or another category-native action.

### Visual Tension
One memorable directional/spatial action is visible at thumbnail size. Balanced-but-flat stacking is insufficient.

### Shared Composition Logic
Product, title, atmosphere, support planes and perspective belong to one directed composition.

### Three-Depth Stage
Foreground, midground and background are deliberately designed. At least two depth cues exist beyond the product.

### Lighting Drama
Lighting reinforces current food semantics and material state without changing product truth.

### Material Depth
Primary materials form spatial planes/structures, not merely decorative props.

### Category-Specific Differentiation
The KV should require major redesign if the product were replaced by a different category. Generic premium styling is insufficient.

### Information Rhythm
When enough authorized copy exists, headline, subtitle/slogan, selling points and utility fields form differentiated levels. Sparse copy is not penalized for staying sparse.

Any hard-gate failure routes to `RETRY_POLICY.md`; do not call it PASS.