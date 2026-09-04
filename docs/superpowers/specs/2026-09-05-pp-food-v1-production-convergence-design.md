# PP Food V1 Production Convergence Design

## Status
Approved for implementation from validated baseline `c57fc0b0e3438cdc9a40deaa511e3b449e7d5530`.

## Goal
Convert the validated PP Food visual engine into a production candidate that preserves the current visual quality while reducing normal-user latency, avoiding unnecessary retries, separating provider failures from creative failures, and keeping the Node handoff repository behaviorally synchronized.

## Source of Truth
`wp746/PP-Food-Runtime-001` is the only design/runtime source of truth.

The Node handoff repository is a production integration mirror. It may have different file structure, but its production behavior, prompt policy, runtime modes, failure semantics, and version mapping must match this repository.

## Non-goals
- Do not redesign the visual methodology.
- Do not weaken Product Truth.
- Do not remove the full Validation workflow.
- Do not build WeChat login, payments, billing, queues, UI, or deployment in this repo.
- Do not silently replace providers or image models.

## Runtime Modes

### VALIDATION
Purpose: internal research, regression, Golden calibration, cross-category evaluation.

Flow:
`source -> Product Truth -> Stage A -> A QC -> Primary + Challenger -> independent candidate eval -> pairwise audition -> Golden-relative gate -> targeted retry/human review`

Rules:
- Exactly two initial B finalists.
- Pairwise comparison is mandatory.
- Golden-vector floors remain available for strict internal validation.
- Full artifacts and score evidence are preserved.

### PRODUCTION_FAST
Purpose: normal mini-program user traffic.

Flow:
`source -> Product Truth -> Stage A -> A hard gate -> Primary B -> production hard gate -> PASS`

Normal path generates one B candidate only.

A Challenger/creative retry may be generated only when the first result has a concrete delivery-blocking failure:
- product identity drift
- reference binding failure
- mechanical invalid image
- copy truth failure
- product no longer first hero / severe hero failure
- clearly broken commercial render

Soft aesthetic disagreement alone must not automatically spend another image-generation call in PRODUCTION_FAST.

## Quality Floor Philosophy
Production optimizes the quality floor, not best-of-N.

Hard truth gates remain strict. Soft Golden-relative aesthetic scoring is advisory in Production Fast unless it detects a severe delivery defect.

Human-accepted Canonicals calibrate the evaluator. Machine rubrics cannot automatically reject a human-accepted quality envelope solely because an old soft aesthetic score is lower.

## Stage A
Stage A remains mandatory for B.

Hard Stage A gates remain:
- product identity
- geometry/count
- ingredient/component topology
- plating/arrangement
- physical relationships
- vessel/package
- source-reference binding

Commercial photography scoring remains, but provider failure and QC transport failure are not creative failures.

## Stage B Candidate Policy

### VALIDATION
Create PRIMARY + CHALLENGER.

### PRODUCTION_FAST
Create PRIMARY only.

If Production Fast Primary fails a retry-eligible hard delivery gate, generate exactly one targeted retry candidate. Do not enter a best-of-many loop.

Maximum production creative retries: 1.
Maximum validation creative cycles: 3.

## Evaluator Reliability

### Candidate slot isolation
Pairwise visual audition must compare only:
1. current Stage A control
2. Primary
3. Challenger

Source and Golden images are not included in the pairwise image array. Golden-relative scoring remains in the independent per-candidate evaluator.

This reduces image-slot confusion and category hallucination.

### Evaluator failure
Add a distinct `EVALUATOR_FAILURE` / equivalent non-creative failure path for invalid evaluator output, impossible slot references, unknown winner IDs, malformed structured output, or obvious cross-category/cross-job contamination.

Evaluator failure must not consume a creative retry.

## Provider Failure Semantics
Provider failures are operational failures, never creative failures.

Required categories include:
- `QC_PROVIDER_TIMEOUT`
- `IMAGE_PROVIDER_TIMEOUT`
- provider HTTP/transport failure
- invalid provider output/download

Transport retry uses the exact same reference image, prompt, model and current-job binding. It does not count as a creative cycle.

## Pairwise Policy
Pairwise ranking cannot create a PASS by itself.

In VALIDATION:
- each candidate must independently pass required hard gates
- pairwise chooses among otherwise eligible candidates
- no qualified candidate => `NO_QUALIFIED_WINNER`

In PRODUCTION_FAST there is no default pairwise call.

## Golden / Canonical Calibration
Existing S01 and S02 remain S-Tier North Stars.

Add a human-accepted Street Food / Night Market Canonical based on the approved 肉夹馍 result, with transferable principles only. The actual private image asset does not need to be committed; local binding is allowed.

Street-food transferable principles:
- strong product-first hero
- high headline pressure without demoting food
- night-market heat/smoke energy
- warm grain + braised-meat material semantics
- high but controlled information density
- contemporary commercial finish rather than cheap flyer styling

Forbidden transfer:
- exact old brand/copy/layout
- generic black-gold template
- giant wooden sign
- ordinary photo + footer

## Production Timing Policy
Runtime records latency for:
- product analysis
- Stage A generation
- Stage A QC
- B generation
- production hard gate / validation evaluator
- retries

The runtime must expose enough evidence for the Node host to implement asynchronous job UX.

Target product behavior is asynchronous job delivery; HTTP requests should not rely on remaining open for the whole image-generation duration.

## Versioning
Production candidate version: `1.0.0-rc.1`.

Runtime artifacts must record:
- runtime version
- runtime mode
- provider/model IDs
- source hash
- Stage A hash
- B reference hash
- compiled prompt hashes
- candidate generation latency
- failure class (provider/evaluator/creative/hard-truth)

## Acceptance Criteria
1. Existing validated tests remain green.
2. New mode tests prove PRODUCTION_FAST generates one initial B candidate.
3. Validation still generates two finalists and pairwise compares them.
4. Provider timeout does not increment creative retry count.
5. Evaluator invalid output does not trigger image regeneration.
6. Production hard gate cannot PASS product/copy/reference-binding failures.
7. Pairwise image slots contain Stage A + two candidates only.
8. Runtime version is `1.0.0-rc.1` on the convergence branch.
9. Street Food Canonical manifest is loadable without committing the private image asset.
10. Node handoff repository receives the matching production mode/failure/prompt policy and version mapping after Runtime verification.
