# PP Food Production V1 RC3

Version: `1.0.0-rc.3`

## Why RC3 exists

A real S02 `PRODUCTION_FAST` run reached the production evaluator after successful image generation, but SiliconFlow returned the `RawEvaluation` JSON Schema (`$defs`, `properties`, `required`, `title`, `type`, etc.) instead of an evaluation data instance. Pydantic correctly rejected that payload, but RC2 surfaced it as an unclassified validation exception.

RC3 hardens the evaluator protocol without changing the approved visual methodology, category translation, Golden floors, Product Truth, Prompt Compiler, Stage A logic, or image-generation policy.

## RC3 behavior

Structured Vision output is now classified before model validation:

```text
INVALID_JSON
SCHEMA_ECHO
MODEL_VALIDATION
```

These map to `STRUCTURED_OUTPUT_PROTOCOL_FAILURE` at the provider boundary.

For `PRODUCTION_FAST` only:

```text
Production evaluator call
→ valid RawEvaluation → normal Production Hard Gate
→ structured-output protocol failure
   → evaluator-only retry × 1
      same Source
      same Stage A
      same B Candidate
      no image generation
      no creative retry consumption
      instance-only JSON instruction
   → valid RawEvaluation → normal Production Hard Gate
   → protocol failure again → NEEDS_HUMAN_REVIEW
      failure_code = EVALUATOR_PROTOCOL_FAILURE
      retry_eligible = false
```

A protocol failure must never be converted into a B creative failure or image regeneration request.

## TDD evidence

The RC3 implementation was built from failing regression tests:

1. schema echo must raise a structured protocol error rather than raw Pydantic exceptions;
2. Production evaluator retries protocol once using the exact same images;
3. a second protocol failure returns human review and never requests image regeneration.

The final RC3 release commit must pass the complete offline/contract suite before it can be used for another live evaluator acceptance.

## Live acceptance boundary

The prior S02 run already proved the chain reached real `PRODUCTION_FAST` generation. RC3 does **not** require another full S02 regeneration merely to verify this fix. The preferred final acceptance is evaluator-only against an existing generated S02 candidate, or one normal Production Fast run only if the existing candidate artifact is unavailable.
