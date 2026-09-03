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
Stage A product drift         → RETURN_TO_A
Product demoted by headline   → PRODUCT_HERO_RETRY
Wrong category skin           → CATEGORY_ROUTE_RETRY
Previous-job skin/entity leak → REBUILD_CURRENT_JOB_CONTRACT
Flat headline/subtitle        → SPATIAL_TYPOGRAPHY_RETRY
Typography error              → TYPOGRAPHY_ACCURACY_RETRY
Unsupported copy              → COPY_TRUTH_RETRY
Weak One Big Idea             → UPPER_BOUND_CREATIVE_RETRY
Too dense / too sparse        → INFORMATION_DENSITY_RETRY
```

Maximum 3 targeted attempts per failure family. On every retry, preserve already-passing parts and change only the failed dimension.

If hard fidelity or typography gates still cannot be satisfied, do not pretend PASS.
