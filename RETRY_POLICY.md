# Targeted Retry Policy

Never random-regenerate the whole concept after a specific failure.

## A Failure Mapping

```text
Food/Product drift            → REFERENCE_LOCK_RETRY
Surface-state drift           → SURFACE_STATE_RETRY
Vessel/Package drift          → VESSEL_PACKAGE_RETRY
Unsupported added content     → CONTENT_REMOVAL_RETRY
Weak hero composition         → HERO_REFRAME_RETRY
Generic / wrong background    → CATEGORY_BACKGROUND_RETRY
Wrong temperature/physics     → PHYSICS_RETRY
Wrong aspect ratio            → ASPECT_CORRECTION_RETRY
```

## B Failure Mapping

```text
Stage A product drift          → RETURN_TO_A
Product demoted by headline    → PRODUCT_HERO_RETRY
Wrong category skin            → CATEGORY_ROUTE_RETRY
Previous-job contamination     → REBUILD_CURRENT_JOB_CONTRACT
Missing/vague director brief   → VISUAL_DIRECTOR_REBUILD
Candidate skeletons too similar→ CREATIVE_BOARD_REBUILD
Safe-template winner           → WINNER_RESELECT_RETRY
Photo-plus-footer              → ANTI_FLATNESS_RETRY
Weak shared composition        → SHARED_COMPOSITION_RETRY
Weak thumbnail memory          → THUMBNAIL_MEMORY_RETRY
Low category inevitability     → CATEGORY_INEVITABILITY_RETRY
Weak visual tension            → KV_TENSION_RETRY
Generic typography behavior    → TYPOGRAPHY_ROLE_RETRY
Typography accuracy error      → TYPOGRAPHY_ACCURACY_RETRY
Unsupported copy               → COPY_TRUTH_RETRY
Too dense / too sparse         → INFORMATION_DENSITY_RETRY
Design regression vs same job  → DESIGN_REGRESSION_RETRY
```

## B Retry Instructions

### CREATIVE_BOARD_REBUILD
Keep product truth, category and copy. Regenerate exactly three candidates using clearly different composition skeletons. Material/color swaps are not sufficient diversity.

### WINNER_RESELECT_RETRY
Do not alter product truth. Re-score the existing candidates with a strong penalty on safe fallback skeletons. If all candidates are weak, rebuild the board instead of forcing a winner.

### ANTI_FLATNESS_RETRY
Preserve accurate product and copy. Replace photo+footer logic with the selected concept's actual spatial composition. Do not fix flatness by simply enlarging or extruding the title.

### THUMBNAIL_MEMORY_RETRY
Strengthen one product-led memorable action. Remove competing secondary ideas. Do not add decorative clutter.

### CATEGORY_INEVITABILITY_RETRY
Re-derive environment, typography role, materials, lighting and spatial action from current product/category semantics. The result should require major redesign if the food category changes.

### KV_TENSION_RETRY
Increase one dominant directional/spatial relationship through composition, perspective, overlap, negative space, architecture or light while protecting product dominance. Do not make every element larger.

### SHARED_COMPOSITION_RETRY
Reconnect product and typography through the selected skeleton: shared support structure, perspective field, controlled overlap, atmosphere bridge, geometry echo or deliberate negative-space relationship.

### TYPOGRAPHY_ROLE_RETRY
Keep exact text. Reconsider typography's role in the selected concept rather than adding generic 3D effects. It may become more restrained if that improves product-led composition.

### DESIGN_REGRESSION_RETRY
When a same-job previous attempt is visibly stronger, preserve the stronger aspects and repair only the new failure. A newer rule version is not automatically better.

Maximum 3 targeted attempts per failure family. Preserve already-passing hard-truth dimensions on every retry.

If hard fidelity, typography accuracy, product dominance or copy truth still cannot be satisfied, do not pretend PASS.
