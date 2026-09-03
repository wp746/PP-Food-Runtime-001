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
PASS: before B prompt compilation, agent creates a current-job visual-director brief derived from category, ingredients/materials, temperature, texture/mouthfeel, regional cues, brand positioning and product truth.
FAIL: agent jumps from Stage A PASS directly to typography/layout.

## T14 Three candidate concepts before selection
PASS: Visual Director internally proposes exactly three compositionally distinct candidate concepts before choosing one.
FAIL: it commits immediately to the first idea or generates three cosmetic variants of the same skeleton.

## T15 Candidate skeleton diversity
PASS: three candidates use materially different composition skeletons, e.g. foreground counter vs portal vs wraparound architecture.
FAIL: top wood sign / top paper sign / top glass sign are treated as three different concepts.

## T16 One selected concept only reaches IMAGE_MODEL
PASS: only the winning candidate is compiled into the B prompt.
FAIL: all three concepts are sent to IMAGE_MODEL, causing blended or averaged design.

## T17 Upper-bound is not a decoration checklist
PASS: a restrained but memorable category-native concept may beat a busier 3D design.
FAIL: system equates upper-bound with more props, more text, larger type or more 3D effects.

## T18 Ingredient-atmosphere derivation
PASS: visual world can be traced to observable/current-job food semantics: ingredient/material, temperature, texture/mouthfeel, process or category temperament.
FAIL: background/typography could be swapped onto a different food category with almost no change.

## T19 Product and typography co-compose
PASS: product and title share a deliberate composition axis, perspective field, stage structure, overlap or depth relationship without title becoming hero #1.
FAIL: product occupies one zone and text occupies an unrelated pasted-on zone.

## T20 Anti-template checks composition skeleton, not surface material
PASS: material changes alone do not count as a new design.
FAIL: top wood sign → top kraft-paper banner passes Anti-Template despite identical top-title / center-product / bottom-info skeleton.

## T21 Thumbnail memory test
PASS: at small size the KV has one clear product-led memorable action.
FAIL: every element is technically correct but the poster reads as polite, balanced and forgettable.

## T22 Category inevitability test
PASS: the chosen world feels specifically derived from this product/category; changing to another category would require major redesign.
FAIL: only copy/material labels would need swapping.

## T23 Creative score is weighted, not mechanical
PASS: QC evaluates product dominance, memorability, category inevitability, composition tension, refinement and typography truth as a whole.
FAIL: design passes by mechanically accumulating checkboxes such as perspective + depth + materiality.

## T24 Self-justifying QC is forbidden
PASS: QC states concrete visual evidence for major scores and can FAIL a visually weak first attempt even when text/fidelity are correct.
FAIL: generator declares all-green PASS because it can name a rule that exists in the image.

## T25 Information density follows copy truth and concept
PASS: sparse copy remains elegant; rich copy is hierarchically distributed.
FAIL: system invents extra selling points or forces 4-level text when unsupported.

## T26 Category-native typography material
PASS: typography material and spatial medium are derived from selected current profile and product semantics.
FAIL: bakery, dessert, noodles, beverages and packaged retail receive the same generic 3D title treatment.

## T27 Candidate score rejects safe-template fallback
PASS: a candidate using an overused skeleton receives a strong penalty even if it satisfies material and depth requirements.
FAIL: safest top-title / center-product / bottom-info layout wins because it is easy to justify.

## T28 Lighting follows food semantics
PASS: light behavior is derived from baked/brothy/cold/creamy/seafood/package properties and preserves source truth.
FAIL: every category receives the same warm dramatic light regardless of food state.

## T29 Category replacement stress test
PASS: replacing current product with a different food category would require major redesign of material, typography, spatial action and atmosphere.
FAIL: current KV remains valid after a simple product swap.

Release candidate should pass all tests in at least two different host agents before being marked production-qualified.
