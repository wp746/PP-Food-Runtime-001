# PP Food Runtime — Production V1 Freeze

Release: `1.0.0`

## Frozen production behavior

- User workflow `A` produces reference-locked commercial hero photography only.
- User workflow `B` requires current-job Stage A PASS before KV generation.
- `PRODUCTION_FAST` generates one initial B Primary and skips Challenger/Pairwise by default.
- At most one targeted creative retry is allowed, and only for delivery-blocking visual failures.
- Provider, evaluator, timeout, transport, and structured-output failures consume zero creative retries.
- Product truth, geometry/count, package/vessel, topology, major physical relationships, and authorized copy remain hard constraints.
- Pack/food routing normalizes provider casing at deterministic boundaries; canned-fruit package jobs route to `CANNED_FRUIT_RETAIL`.
- Production evaluator structured-output protocol failures trigger at most one evaluator-only retry on the same images; a second failure returns human review without image regeneration.

## Release evidence

Pre-freeze RC3 CI: `85 passed / 3 skipped / 0 failed`.

The skipped tests are opt-in private/provider integrations and are not silently converted into PASS.

Live evaluator-only acceptance on the S02 case confirmed:

- raw `Pack` normalizes to `PACK`;
- RC3 category translation resolves to `CANNED_FRUIT_RETAIL`;
- SiliconFlow structured output is parsed into a normal Production Gate result rather than crashing on schema echo;
- evaluator-only verification performs no Yunwu image regeneration.

The reused historical S02 candidate returned `HERO_WEAK`. This is retained as a legitimate Production Hard Gate retry condition. The release does not lower QC thresholds to manufacture a PASS.

## Deployment defaults

```text
PP_RUNTIME_VERSION=1.0.0
PP_RUNTIME_MODE=PRODUCTION_FAST
PP_PRODUCTION_MAX_CREATIVE_RETRIES=1
PP_VALIDATION_MAX_CREATIVE_CYCLES=3
```

API keys and private job/Golden assets must remain outside the repository.
