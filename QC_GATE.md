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

## B QC

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
Upper-Bound Readiness >=90

VISUAL_DIRECTOR_BRIEF = PASS
ATMOSPHERE_EVIDENCE >=3
ONE_BIG_IDEA = CONCRETE_SPATIAL_ACTION
Title Spatiality >=90
Visual Tension >=90
Shared Composition Logic >=90
Information Rhythm >=85 when sufficient copy exists
Anti-Flatness = PASS
```

Product remains first visual hero. Headline is second.

## B Anti-Flatness Critical Failures

Any of these immediately blocks PASS:

- Stage A photo plus a bottom text panel is the dominant layout logic;
- headline is a flat or shallow horizontal strip detached from the product world;
- product and typography occupy unrelated independent zones;
- all copy sits on one footer plane;
- title lacks at least 3 of perspective / volume / category-native materiality / spatial attachment;
- no concrete One Big Idea can be identified at thumbnail scale;
- typography is accurate but the KV still reads as polite, generic, or template-flat;
- title becomes the first hero and product is demoted.

## B Tension Evaluation

### Title Spatiality
Evaluate whether headline behaves as a real scene element: sign, lintel, counter front, paper emboss, glass/acrylic installation, corridor, packaging plane, flavor-wave structure, or another category-native spatial action.

### Visual Tension
Evaluate whether the KV has one memorable directional/spatial action rather than balanced-but-flat stacking.

### Shared Composition Logic
Evaluate whether product, title, atmosphere, support planes and perspective belong to one directed composition.

### Information Rhythm
When enough authorized copy exists, check distinct levels for headline, subtitle/slogan, selling points, and utility. Sparse information is not penalized for remaining sparse.

Any hard-gate failure must route to `RETRY_POLICY.md`; do not call it PASS.
