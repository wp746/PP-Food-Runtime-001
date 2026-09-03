# Runtime Contract Tests

Development/release tests only. Do not load during normal production.

## T01 Explicit A stays A
PASS: `执行A` generates commercial Stage A only.
FAIL: Agent enters KV because brand/price/address is present.

## T02 Explicit B cannot skip A
PASS: current raw image → current A → A QC PASS → B.
FAIL: B starts directly from raw snapshot.

## T03 No guessing images
PASS: non-visual host routes image to VISION_MODEL.
FAIL: host infers product from filename or user sentence.

## T04 Current-job isolation
PASS: previous brand/copy/skin absent unless explicitly continued.
FAIL: previous task entities or visual skin leak into current contract.

## T05 Category isolation
PASS: exactly one primary profile + optional one weak auxiliary profile.
FAIL: all category skins/examples are loaded or mixed.

## T06 Prompt compiler is fixed
PASS: IMAGE_MODEL receives current reference + compact contract + fixed six blocks.
FAIL: whole repository, tests, old examples, or ad hoc prompt architecture is sent.

## T07 Product fidelity dominates aesthetics
PASS: design aggression is reduced when it threatens product identity.
FAIL: product is re-plated, re-cooked, re-packaged, or redesigned for beauty.

## T08 Product hero dominates B
PASS: product is first visual hero, headline second.
FAIL: headline becomes dominant focal point or obscures critical product area.

## T09 Copy truth
PASS: hard facts only from user/current reliable source; missing copy is asked minimally or generated only after authorization.
FAIL: phone/address/price/claims/history/process are invented.

## T10 Targeted retry
PASS: only failed dimension is repaired.
FAIL: random full concept regeneration after a local failure.

## T11 Exact 9:16
PASS: final A/B delivery is exact 9:16.
FAIL: attractive non-9:16 output is accepted.

## T12 Packaging fidelity
PASS: package silhouette, lid/seal, label structure, brand identity, major visible text blocks and contents remain source-faithful.
FAIL: packaged product is redesigned or turned into restaurant food styling.

Release candidate should pass all tests in at least two different host agents before being marked production-qualified.
