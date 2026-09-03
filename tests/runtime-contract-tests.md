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

## T13 B Visual Director is mandatory
PASS: before B prompt compilation, agent creates a current-job visual-director brief derived from category, ingredients/materials, temperature, texture/mouthfeel, regional cues, brand positioning, atmosphere, and one big idea.
FAIL: agent jumps from Stage A PASS directly to typography/layout.

## T14 One Big Idea is concrete
PASS: B defines one explicit spatial campaign action such as headline_as_bakery_sign, headline_as_counter_front, headline_as_flavor_wave, headline_as_glass_installation, or another category-native action.
FAIL: ONE_BIG_IDEA is only vague adjectives such as premium, cinematic, warm, elegant, energetic.

## T15 Anti-flatness
PASS: headline has at least 3 of perspective / volume / materiality / spatial attachment, and the copy system occupies multiple spatial layers while remaining subordinate to product.
FAIL: result is commercial photo + bottom text panel, flat headline strip, or all copy placed on one footer plane.

## T16 Ingredient-atmosphere derivation
PASS: visual world can be traced to observable/current-job food semantics: ingredient/material, temperature, texture/mouthfeel, process or category temperament.
FAIL: background/typography could be swapped onto a different food category with almost no change.

## T17 Product and typography co-compose
PASS: product and title share a deliberate composition axis, perspective field, stage structure, or depth relationship without title becoming hero #1.
FAIL: product occupies one zone and text occupies an unrelated pasted-on zone.

## T18 Information rhythm
PASS: when sufficient copy exists, headline / subtitle-or-slogan / selling points / business utility form clearly different visual levels and spatial media.
FAIL: all text has similar scale, alignment, material, plane, and rhythm.

## T19 Visual-tension QC blocks polite-but-flat KV
PASS: B cannot PASS unless Title Spatiality, Visual Tension, Shared Composition Logic and Anti-Flatness gates pass.
FAIL: accurate typography and correct category alone are treated as sufficient for PASS.

## T20 Category-native typography material
PASS: typography material and spatial medium are derived from the selected current profile and current product semantics.
FAIL: bakery, dessert, noodles, beverages and packaged retail receive the same generic 3D title treatment.

Release candidate should pass all tests in at least two different host agents before being marked production-qualified.
