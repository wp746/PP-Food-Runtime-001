# PP Food Validation Engine V0 Design Spec

**Status:** Approved design basis for validation implementation; not a production/miniprogram architecture freeze.

**Date:** 2026-09-04

## 1. Goal

Build a local-first, executable Validation Engine that can prove or disprove the core product claim before any miniprogram handoff:

> Given one user image plus mode A or B and authorized facts, the same runtime code should repeatedly produce outputs inside a stable, high-quality visual envelope comparable to the human-approved PP Food results from the 二大爷米线 project.

This phase is successful only when repeated real image-generation runs pass Golden regression. Markdown compliance or self-reported QC is not sufficient evidence.

## 2. Non-goals

Validation V0 does not freeze the final production architecture and does not build:

- WeChat Mini Program UI
- login, membership, payment, orders, billing, CDN, admin console
- public cloud deployment or high concurrency
- final SDK/handoff package for the miniprogram company

Those are deferred until Validation V0 proves output stability.

## 3. Core architecture principle

The host agent is only a client. It must not decide art direction, prompt structure, category logic, retry strategy, or QC.

```text
Host / CLI
  -> Job Contract
  -> Validation Engine
       -> Vision Adapter
       -> Product Truth Lock
       -> Stage A
       -> Category Visual Translation
       -> Golden Retrieval
       -> B Art Director
       -> Deterministic Prompt Compiler
       -> Image Provider Adapter
       -> Independent Evaluator
       -> Targeted Retry
       -> Artifact Store
```

The engine is implemented as local executable code first. Provider interfaces remain configurable so the same core can later be wrapped by HTTP/cloud deployment without changing creative logic.

## 4. Ground truth hierarchy

Evaluation authority is ordered as:

1. source image truth
2. hard machine QC
3. Golden-relative visual evaluation
4. human Golden authority

A machine may return PASS / RETRY / GOLDEN_CANDIDATE. Only the user may promote an image to GOLD, CANONICAL, or S-TIER.

## 5. Initial Golden Set

### S-TIER North Stars

- S01: 椰椰西瓜冰夏日广告海报
  - teaches sensory-to-visual translation, strong product + strong headline, product-derived material, multi-depth campaign composition.
- S02: 阳光蜜橘罐头广告海报
  - teaches package hero, high information density with control, conversion-oriented campaign completeness.

### CANONICAL

- A01: 安康酸辣米线招牌海报
- A02: 苦瓜炒腊肉金色美食海报
- A03: 茉莉抹茶冰淇淋蛋糕奢华海报

### Empty category

- Bakery currently has no approved Canonical. Existing 欧丰园贝果 output must not be used as a Golden anchor. Bakery earns Canonical status only after a new result is explicitly approved by the user.

## 6. Golden Visual DNA

The B-stage upper-bound target is:

```text
PRODUCT_TRUTH
+ EXTREME_PRODUCT_HERO
+ HIGH_HEADLINE_AGGRESSION
+ PRODUCT_DERIVED_TYPOGRAPHY
+ ONE_PRODUCT_DERIVED_BIG_IDEA
+ MULTI_DEPTH_CO_COMPOSITION
+ CONTROLLED_INFORMATION_DENSITY
+ CATEGORY_INEVITABILITY
+ CAMPAIGN_GRADE_FINISH
```

B does not default to minimalism. High information density is allowed when hierarchy and product dominance remain controlled.

### Golden vector

Every B candidate is evaluated on 0-10 scales:

- product_hero_strength
- headline_aggression
- typography_product_symbiosis
- one_big_idea_clarity
- compositional_depth_tension
- category_inevitability
- information_density_control
- commercial_finish

V0 target floors:

- product_hero_strength >= 9.0
- headline_aggression >= 8.8
- typography_product_symbiosis >= 8.5
- one_big_idea_clarity >= 8.3
- compositional_depth_tension >= 8.8
- category_inevitability >= 8.5
- information_density_control >= 7.8
- commercial_finish >= 9.0

Weighted score is advisory only and cannot override a hard failure.

## 7. Product truth and Stage A/B relationship

Stage A provides:

- product truth baseline
- clean commercial product render
- fidelity reference for B

Stage B inherits product identity, geometry, surface state, ingredient topology, package/vessel identity, and major physical relationships.

Stage B does **not** inherit an exact Stage A camera lock. The previous `<=15% apparent product scale change` rule is removed. B may creatively change scale, crop, camera, position, overlap, foreground pressure, background, and environmental lighting while preserving product DNA and product dominance.

## 8. Category Visual Translation

Category is a constraint/context layer, not a fixed template.

The required derivation chain is:

```text
Product Truth
-> Sensory Semantics
-> Emotional Semantics
-> Brand Temperament
-> Material Metaphor
-> Typography Translation
-> Color Translation
-> Lighting Translation
-> Spatial Translation
-> Motion/Energy Translation
-> Information System
-> One Big Idea
```

Typography material must be traceable to the current product, not merely to the category.

### Anti-template rule

Principle transfer from Goldens is allowed. Skin transfer is forbidden.

Allowed transfer examples:

- product/headline pressure
- multi-depth composition
- material reasoning
- information hierarchy
- campaign finish

Forbidden transfer examples:

- old brand/copy
- exact old layout
- exact props
- exact palette
- category-inappropriate visual skin

Literal category shortcuts are rejected when they are merely noun associations, e.g. bread -> oven tunnel, seafood -> underwater world.

## 9. B-stage state machine

```text
B_REQUESTED
-> B_ENTRY_VALIDATION
-> STAGE_A_PASS_REQUIRED
-> PRODUCT_LOCK_BRIDGE_READY
-> COPY_FIREWALL_READY
-> CURRENT_PRODUCT_ANALYSIS
-> CATEGORY_VISUAL_TRANSLATION
-> GOLDEN_RETRIEVAL
-> ART_DIRECTION
-> ART_DIRECTION_VALIDATION
-> PROMPT_CONTRACT_READY
-> FINALIST_RENDER
-> FINALIST_VISUAL_EVAL
-> WINNER_SELECTION
-> TARGETED_REFINEMENT
-> FINAL_QC
-> B_PASS
```

Failure states include:

- NEEDS_USER_FACT
- RUNTIME_FAILURE
- PROVIDER_FAILURE
- FIDELITY_RETRY
- CREATIVE_RETRY
- COPY_RETRY
- NEEDS_HUMAN_REVIEW

## 10. Copy Firewall

Text is partitioned into:

- VERIFIED_FACT
- AUTHORIZED_CAMPAIGN_COPY
- FORBIDDEN_UNSUPPORTED_HARD_FACT

User-provided hard facts must be exact. The engine may generate safe non-factual campaign language only when default copy is authorized. It may not invent price, address, phone, certification, award, history, origin, ingredient claims, health claims, or process claims.

Design density follows available truth; missing facts must not be fabricated to fill layout.

## 11. Art direction candidate policy

V0 produces exactly:

- one Primary direction: best product-semantic + Golden-principle solution
- one Challenger direction: same truth/quality target but meaningfully different composition solution

Primary and Challenger must differ in at least two of:

- composition axis
- headline spatial behavior
- product placement
- energy direction
- depth architecture
- information integration

A mere material or color swap is not a valid Challenger.

Both are rendered independently from the same current Stage A reference; Challenger is not an edit of Primary.

## 12. Deterministic Prompt Compiler

The Art Director outputs a validated structured contract and never writes the final provider prompt directly.

The compiler receives only the current validated job contract and provider profile. Same contract + same profile must produce the same prompt structure independent of host agent.

Canonical B prompt order:

1. output contract
2. reference authority
3. product identity lock
4. product surface lock
5. package/vessel/topology lock
6. current product semantics
7. one big idea
8. product hero direction
9. typography direction
10. product-typography relationship
11. composition/depth
12. category-native atmosphere
13. color
14. lighting
15. information system
16. Golden quality target
17. hard negatives
18. final core command

The compiler must not include generator self-scores, rejected-candidate reasoning, whole research repositories, irrelevant Goldens, or old brand examples.

## 13. Provider boundary

Vision and image providers are adapters with explicit capability profiles. Configuration is externalized; secrets are never embedded in prompts or repository files.

Capability fields include at minimum:

- image/reference edit support
- multiple references
- masks/region edit
- seed if available
- text-rendering support
- aspect ratio support
- resolution limits

Reference binding must be evidenced. If the current-job reference image cannot be proven attached, fidelity evaluation is invalid and the failure is classified as provider/runtime failure, not creative failure.

## 14. Independent evaluation

Generator reasoning and self-scores are hidden from the evaluator. The evaluator sees only the necessary current source, Stage A pass, final image, truth/copy contract, category translation, and relevant Golden references/principles.

Evaluation order:

```text
Mechanical
-> Product Truth
-> Copy Truth
-> Visual First-Read
-> Golden Vector
-> Pairwise Comparison
-> Golden-Relative Comparison
-> Anti-Pattern Tests
-> Commercial Finish
-> Final Decision
```

Hard truth failures stop evaluation and cannot be compensated by creative scores.

### First-read target

Default hierarchy:

1. product
2. headline
3. big idea / secondary message

### Required anti-pattern checks

- SAFE_EDITORIAL_COLLAPSE
- SCENE_DOMINATES_PRODUCT
- CATEGORY_CLICHE_DEPENDENCE
- GENERIC_PREMIUM_SKIN
- TEMPLATE_REUSE
- PHOTO_PLUS_TEXT
- INFORMATION_STARVATION
- INFORMATION_OVERLOAD

The evaluator must cite visible evidence (what is seen and where), not rule names.

## 15. Golden-relative rule

The evaluator does not ask whether the output looks like S01/S02. It asks whether the current output operates at comparable visual pressure and campaign maturity.

Core relative dimensions:

- product hero
- headline pressure
- product-derived material logic
- composition/tension
- information system
- commercial finish

Two `materially_weaker` results among core dimensions cause upper-bound failure.

A pairwise winner can still fail. `A > B` does not imply `A = PASS`; if neither reaches the Golden quality floor the result is `NO_QUALIFIED_WINNER` and the engine retries.

## 16. Retry system

Retries are failure-code driven and preserve passing dimensions via a pass-freeze map.

Retry families:

- FIDELITY_RETRY
- HERO_RETRY
- HEADLINE_PRESSURE_RETRY
- TYPOGRAPHY_SYMBIOSIS_RETRY
- BIG_IDEA_RETRY
- COMPOSITION_RETRY
- CATEGORY_TRANSLATION_RETRY
- INFORMATION_RETRY
- COMMERCIAL_FINISH_RETRY
- GOLDEN_DISTANCE_RETRY

Levels:

1. targeted repair
2. concept adjustment
3. art-direction rebuild

Maximum B creative cycles in Validation V0: 3. After that, return NEEDS_HUMAN_REVIEW rather than continuing random regeneration.

## 17. Artifact logging

Every job stores enough evidence to reproduce and compare runs:

- job id
- runtime version
- provider profile
- source image reference/hash
- Stage A pass reference/hash
- user facts / copy allowlist
- product analysis
- category translation
- Golden retrieval
- Primary/Challenger directions
- compiled prompts
- generated finalists
- evaluator output
- retries/pass-freeze maps
- final output/final QC
- optional human review/promotion

No secrets are stored.

## 18. Stability definition

Stability does not mean identical pixels. It means a stable quality envelope.

For a fixed source + facts + runtime version + provider profile, run each Canonical case 3 times.

Minimum V0 stability gate per case:

- fidelity: 3/3 pass
- copy truth: 3/3 pass
- category: 3/3 pass
- catastrophic drift: 0
- upper-bound pass: at least 2/3
- worst run remains at or above strong commercial baseline

Recommended worst-run weighted floor: >= 8.0.

A pattern of `1 world-class + 2 mediocre` is a stability failure.

## 19. Regression policy

Every core runtime change runs the full current Canonical suite.

Initial suite:

- S01 西瓜冰 x3
- S02 橘子罐头 x3
- A01 酸辣米线 x3
- A02 苦瓜炒腊肉 x3
- A03 抹茶蛋糕 x3

A regression of either S-Tier blocks the change. Material degradation of two or more Canonical cases also blocks the change.

Single-case patches are not promoted to Runtime Core unless they demonstrate generalizable improvement.

## 20. Validation implementation boundary

Validation V0 should be implemented as a focused Python codebase with:

- local CLI entrypoint first
- typed/validated job contracts
- deterministic compiler
- provider adapters
- local artifact store
- Golden manifest/retrieval layer
- mockable provider interfaces for tests
- opt-in real-provider integration tests

This is a validation implementation choice, not a freeze of the final miniprogram/cloud architecture.

The code should be organized so the validated core can later be wrapped by HTTP without changing creative logic.

## 21. Acceptance gate before miniprogram handoff

No miniprogram integration package is produced until all of the following are true:

1. A fidelity/commercial-photography path is stable.
2. B produces Golden-range outputs across the current Canonical suite.
3. 3x repeated-run stability gates pass.
4. Bakery receives a newly generated human-approved Canonical.
5. Cross-category regression is clean.
6. Host/client independence is demonstrated with the same engine/compiler path.
7. Runtime version is explicitly frozen for handoff.

Only after this gate will a separate productionization design cover cloud API, Docker/deployment, API key isolation, and copy-paste miniprogram client integration code.

## 22. Immediate validation milestone

The first implementation milestone is not the full product. It is the smallest executable vertical slice that can:

1. create a validated B job contract from one known Canonical case,
2. load the correct Golden manifest,
3. derive a structured visual translation,
4. compile a deterministic provider prompt,
5. call the configured image provider,
6. evaluate the returned image against hard truth + Golden-relative rubric,
7. persist the artifacts.

Once this vertical slice runs end-to-end on S01 and S02, real visual validation begins immediately. The user should be shown results only when the engine can produce actual candidate images and evaluation evidence.