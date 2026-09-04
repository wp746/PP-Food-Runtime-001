# PP-Food-Runtime-001

**Release candidate:** `1.0.0-rc.1`

Self-contained runtime for stable reference-locked food commercial photography (A) and campaign KV generation (B) across hosts. The production runtime does not need to read the research mother repositories at execution time.

## Non-negotiable truth hierarchy

```text
CURRENT USER SOURCE
→ CURRENT-JOB PRODUCT TRUTH
→ CURRENT-JOB STAGE A PASS
→ CURRENT-JOB COPY ALLOWLIST
→ CATEGORY TRANSLATION
→ GOLDEN PRINCIPLES (principles only, never skin)
```

Product identity, geometry/count, visible surface state, package/vessel, topology and major physical relationships are binding. Stage B always edits from the current-job Stage A PASS image.

## User workflow

### `A` / `执行A`

Produces commercial hero photography only. No KV copy or poster treatment.

### `B` / `执行B`

Runs current-job Stage A first, requires Stage A PASS, then enters the B copy/category/art-direction pipeline.

`按默认文案来` authorizes only safe non-factual campaign copy. It never authorizes invented phone numbers, addresses, prices, opening hours, awards, certifications, origins, ingredients, medical/health claims or other hard facts.

## Runtime execution modes

A/B is the user workflow. `VALIDATION` / `PRODUCTION_FAST` is the internal Stage-B execution policy.

### PRODUCTION_FAST

Default deployment mode for mini-program delivery:

```text
Source
→ Product Truth
→ Stage A
→ A hard QC
→ B Primary (one initial render)
→ independent Production Hard Gate
→ PASS
```

If and only if a delivery-blocking visual failure is detected, the runtime may perform **one** targeted creative retry. Provider or evaluator failures consume **zero** creative retries.

Production Hard Gate blocks mechanical/reference-binding/product-truth/copy-truth failures, loss of product-first hierarchy, scene dominance, and clearly broken commercial finish. Golden-relative softness alone does not trigger regeneration.

### VALIDATION

Quality investigation / Golden calibration mode:

```text
Source
→ Product Truth
→ Stage A PASS
→ Primary + Challenger
→ independent per-candidate Golden evaluation
→ pairwise visual audition: Stage A control + Primary + Challenger
→ winner selection / review
```

Validation uses full Golden-vector floors and anti-template checks. It is intentionally more expensive than Production Fast.

## Operational failure rule

Provider timeout/transport failure and evaluator failure are operational failures, not creative failures. They must not be converted into a creative retry request. Evaluator confidence below `0.65` requires evaluation retry/second evaluation without regenerating the image.

## Runtime evidence

Each job persists reproducibility evidence including runtime version/mode, provider/model IDs, source and Stage A hashes, prompt hashes, generation request evidence, latency/timing, retry count, failure class and final decision.

## Configuration

Copy `.env.example` into a secure environment and inject credentials there. Never commit API keys or private job assets.

Production deployment should explicitly set:

```text
PP_RUNTIME_VERSION=1.0.0-rc.1
PP_RUNTIME_MODE=PRODUCTION_FAST
PP_PRODUCTION_MAX_CREATIVE_RETRIES=1
```

## Release state

`1.0.0-rc.1` is the production-convergence release candidate. Offline/contract verification is required on every release commit. Real-provider/private S01/S02 checks remain opt-in and require secure credentials/assets; they must not be represented as passed unless actually executed on that commit.
