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
FAIL: headline or environment becomes first read.

## T09 Copy truth
PASS: hard facts only from user/current reliable source.
FAIL: phone/address/price/claims/history/process are invented.

## T10 Exact 9:16
PASS: final A/B delivery is exact 9:16.
FAIL: attractive non-9:16 output is accepted.

## T11 Packaging fidelity
PASS: package silhouette, label structure, brand identity and contents remain source-faithful.
FAIL: packaged product is redesigned or converted to restaurant serving.

## T12 B Visual Director mandatory
PASS: B creates current-job art direction before rendering.
FAIL: B jumps from Stage A PASS directly to layout.

## T13 Three textual candidates
PASS: exactly three compositionally distinct hypotheses are created.
FAIL: one idea or three cosmetic variants.

## T14 Two rendered finalists mandatory for stable upper-bound
PASS: two visually distinct B candidate images are actually generated from the same Stage A PASS image.
FAIL: textual planning scores alone determine the winner.

## T15 Visual comparison uses actual images
PASS: VISION_MODEL compares rendered finalists and selects the stronger image.
FAIL: the host selects from prose before seeing render evidence.

## T16 Stage A hero camera lock
PASS: B product apparent scale shrinks no more than 15% from Stage A and remains first read.
FAIL: scenic concept pushes product deep/small.

## T17 Environment dominance rejection
PASS: arch/portal/room/shelf/signage remains support.
FAIL: environment becomes the remembered subject.

## T18 Non-literal category translation
PASS: bakery/hot/cold/dessert semantics become palette/light/material/rhythm/type cues.
FAIL: category is literalized into old oven tunnel, cave, giant sign, steam corridor or decorative cliché by default.

## T19 Contemporary campaign filter
PASS: result feels like contemporary premium food advertising with controlled materials, hierarchy and negative space.
FAIL: theme-park, souvenir, rustic theatrical or menu-board aesthetic.

## T20 At least one restrained/editorial finalist
PASS: candidate pair is not automatically two scenic/architectural concepts.
FAIL: both finalists assume world-class means more scenery.

## T21 Candidate skeleton diversity
PASS: finalists differ in skeleton, negative space, headline role, depth/material approach and lighting.
FAIL: wood/paper/glass variants of same layout.

## T22 Upper-bound is not decoration count
PASS: restrained solution may beat busier 3D design.
FAIL: more props/type/scenery automatically scores higher.

## T23 Category inevitability
PASS: replacing product with a different category requires major redesign.
FAIL: simple product swap still works.

## T24 Product and typography co-compose
PASS: type belongs to same directed image without forcing product shrinkage.
FAIL: unrelated text zone or title-first composition.

## T25 Anti-template checks skeleton
PASS: material swaps do not count as innovation.
FAIL: top wood sign → top paper sign passes.

## T26 Thumbnail memory
PASS: at small size product remains first read and one product-led gesture is memorable.
FAIL: poster is technically correct but forgettable.

## T27 Self-justifying QC forbidden
PASS: QC cites visible image evidence and can fail an all-green-looking result.
FAIL: “there is perspective/material/depth, therefore PASS.”

## T28 Lighting follows food semantics
PASS: light derives from product properties.
FAIL: all categories use same warm dramatic light.

## T29 Design regression cannot pass
PASS: visibly weaker new output is rejected even if it follows newer rules.
FAIL: latest version automatically wins.

## T30 Visual-audition capability gate
PASS: if runtime cannot render/compare two B candidates, it marks B quality mode DEGRADED and forbids stable-upper-bound claim.
FAIL: single-render host claims deterministic world-class B.

Release candidate should pass all tests in at least two different host agents before being marked production-qualified.