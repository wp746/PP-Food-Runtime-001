# PP Food Production V1 RC1

Release: `1.0.0-rc.1`

This document is the production-convergence contract for the Python Runtime that the Node mini-program handoff must mirror.

## Frozen production invariants

1. Current user source is the highest product-truth authority.
2. Stage B always uses the current-job Stage A PASS as its image-edit reference.
3. Product DNA is locked; B camera/composition is not globally frozen.
4. Copy is allowlisted. Default-copy authorization permits soft non-factual campaign copy only.
5. `PRODUCTION_FAST` generates exactly one initial B candidate.
6. A normal Production Fast PASS performs no pairwise audition.
7. Production creative retries are capped at one.
8. Provider/evaluator/runtime failures consume zero creative retries.
9. `VALIDATION` keeps Primary + Challenger and pairwise visual audition.
10. Validation pairwise slots are exactly Stage A control, Primary, Challenger.
11. Human-Accepted Canonical metadata may calibrate style; private Golden image assets are not committed.
12. Every job records runtime/provider/hash/prompt/timing/failure evidence.

## Production Fast decision boundary

The production gate exists to reject broken deliverables, not to spend API calls chasing a subjective perfect score.

Hard blockers:

```text
mechanical failure
reference binding failure
product truth drift
copy truth failure
product not first hero
scene dominates product
commercially broken render
```

Soft advisory signals do not alone trigger regeneration:

```text
Golden distance
photo-plus-text tendency
category cliché tendency
generic premium skin
other non-breaking aesthetic shortfall
```

## Validation decision boundary

Validation is the quality-development path. It uses actual rendered images, eight Golden dimensions, anti-template checks, and a three-image pairwise audition where Stage A is control only.

## Security / private assets

API keys, `.env`, private S01/S02 images, private Golden assets and job artifacts must remain outside Git. Golden manifests may use `LOCAL_BIND_REQUIRED` and bind private assets at runtime.

## Release verification

A release commit is not considered verified until the full repository test workflow executes on that exact commit. Real-provider/private-Golden integration remains opt-in and must be reported as skipped/pending unless actually executed with secure assets and credentials.

## Node handoff synchronization rule

The Node handoff must record the exact Runtime commit SHA it mirrors. `SYNC STATUS: MATCHED` is allowed only after Node tests/typecheck and a policy comparison confirm mode behavior, hard/soft failure semantics, retry caps and version mapping are aligned.
