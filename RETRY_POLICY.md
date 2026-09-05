# Retry Policy — 1.0.0-rc.2

Never random-regenerate after a named failure. Preserve current-job truth and already-passing dimensions.

## Operational failures are not creative retries

The following consume **zero** creative retry budget:

- provider timeout / transport failure;
- evaluator failure or invalid winner ID;
- evaluator confidence below `0.65`;
- runtime/reference I/O failure.

Operational recovery means retry transport/evaluation or fail closed. Do not redesign the image to fix an evaluator/provider problem.

## Stage A

Typical mappings:

```text
Product drift             → REFERENCE_LOCK_RETRY
Surface-state drift       → SURFACE_STATE_RETRY
Vessel/package drift      → VESSEL_PACKAGE_RETRY
Unsupported content       → CONTENT_REMOVAL_RETRY
Weak hero composition     → HERO_REFRAME_RETRY
Wrong category background → CATEGORY_BACKGROUND_RETRY
Wrong physics             → PHYSICS_RETRY
Wrong aspect ratio        → ASPECT_CORRECTION_RETRY
```

## PRODUCTION_FAST

Maximum creative retries: **1**.

A creative retry is eligible only for a delivery-blocking hard gate such as:

```text
PRODUCT_IDENTITY_DRIFT
COPY_TRUTH_FAILURE
MECHANICAL_FAILURE
REFERENCE_BINDING_FAILURE
HERO_WEAK
SCENE_DOMINATES_PRODUCT
COMMERCIAL_FINISH_WEAK
```

The retry instruction must name only the failing dimensions and preserve current Stage A reference, product truth, authorized copy and passing visual dimensions.

The following by themselves do **not** trigger Production Fast regeneration:

```text
GOLDEN_DISTANCE
PHOTO_PLUS_TEXT
CATEGORY_CLICHE_DEPENDENCE
GENERIC_PREMIUM_SKIN
other soft aesthetic shortfalls
```

After the single creative retry, either PASS the hard gate or stop for review. No hidden second/third regeneration loop.

## VALIDATION

Validation retains the richer named repair taxonomy and `PP_VALIDATION_MAX_CREATIVE_CYCLES` cap (maximum 3). It may stop earlier and request review when no qualified winner exists.

Representative repair families include product fidelity, hero hierarchy, headline pressure, typography symbiosis, Big Idea, composition, category translation, information density, commercial finish and Golden distance.

## Pass-freeze rule

Every creative retry must preserve dimensions that already pass. “Make it better” is not a valid retry instruction; the repair target must be explicit and auditable.
