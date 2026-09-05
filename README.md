# PP-Food-Runtime-001

**Release candidate:** `1.0.0-rc.3`

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

## Category normalization

Provider observations are treated as evidence, not canonical routing keys. Pack/food classification is normalized at runtime boundaries before category translation and Golden retrieval. For example, `Pack`, `PACK`, and equivalent casing must route consistently; canned-fruit package jobs must resolve to `CANNED_FRUIT_RETAIL` rather than a generic fallback.

## Evaluator protocol safety

Structured evaluator output is treated as a protocol contract, not as creative evidence. A JSON-Schema echo, invalid JSON, or payload that does not validate as the requested response model is classified as `STRUCTURED_OUTPUT_PROTOCOL_FAILURE`.

In `PRODUCTION_FAST`, the runtime may retry the **evaluator only once** with the exact same Source / Stage A / B Candidate images and an instance-only response instruction. This retry never regenerates an image and consumes zero creative retries. If the second evaluator response is still invalid, the job returns `NEEDS_HUMAN_REVIEW` with `EVALUATOR_PROTOCOL_FAILURE`; it must not trigger B regeneration.

## Operational failure rule

Provider timeout/transport failure and evaluator failure are operational failures, not creative failures. They must not be converted into a creative retry request. Evaluator confidence below `0.65` requires evaluation retry/second evaluation without regenerating the image.

## Runtime evidence

Each job persists reproducibility evidence including runtime version/mode, provider/model IDs, source and Stage A hashes, prompt hashes, generation request evidence, latency/timing, retry count, failure class and final decision.

## Configuration

Copy `.env.example` into a secure environment and inject credentials there. Never commit API keys or private job assets.

Production deployment should explicitly set:

```text
PP_RUNTIME_VERSION=1.0.0-rc.3
PP_RUNTIME_MODE=PRODUCTION_FAST
PP_PRODUCTION_MAX_CREATIVE_RETRIES=1
```

## Release state

`1.0.0-rc.3` preserves the approved RC2 visual methodology and category/Golden routing fixes. RC3 is a production-evaluator protocol hardening candidate discovered during the real S02 Production Fast run: SiliconFlow returned the `RawEvaluation` JSON Schema itself instead of a data instance. RC3 classifies this condition explicitly, performs at most one evaluator-only retry on the same images, and fails closed to human review without image regeneration if the protocol fails again. Offline/contract verification is required on every release commit. Real-provider/private checks remain opt-in.
