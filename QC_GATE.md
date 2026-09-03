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
```

Product remains first visual hero. Headline is second.

Any hard-gate failure must route to `RETRY_POLICY.md`; do not call it PASS.
