# Execution Modes — 1.0.0-rc.2

There are two independent axes:

1. **User workflow:** A or B.
2. **B runtime policy:** `PRODUCTION_FAST` or `VALIDATION`.

Do not conflate them.

## User Mode A

Triggers: `A`, `执行A`.

```text
CURRENT USER IMAGE
→ current-job Product Truth
→ Stage A reference edit
→ independent A QC
→ targeted A repair if required
→ deliver Stage A only
```

No KV copy gate and no Stage B.

## User Mode B

Triggers: `B`, `执行B`.

B can never skip current Stage A:

```text
CURRENT USER IMAGE
→ current-job Product Truth
→ current Stage A
→ A QC PASS
→ ProductLockBridge
→ Copy Firewall
→ Category Translation
→ Golden principle retrieval
→ Art Direction
→ runtime policy branch
```

Provider-returned category and pack/food labels are normalized before routing so casing differences such as `Pack` vs `PACK` cannot silently send a packaged-retail product into the generic fallback path.

## PRODUCTION_FAST

Use for mini-program / normal online delivery.

```text
Primary only
→ Production Hard Gate
→ PASS
```

If a delivery-blocking visual failure occurs, allow at most one targeted creative retry. Do not run pairwise on a normal pass. Do not regenerate for Golden soft-score shortfall alone.

Operational provider/evaluator failure stops or re-evaluates; it never consumes the creative retry budget.

## VALIDATION

Use for Golden calibration, regression investigation and quality development.

```text
Primary + Challenger
→ full per-candidate evaluation
→ pairwise audition with exactly 3 images:
   1 Stage A control
   2 Primary
   3 Challenger
→ Golden-relative decision
```

Stage A is control only and can never be selected as the B winner.

## Copy Gate

Formal B requires a headline/product name plus sufficient authorized supporting information. Product/dish name may serve as headline. Ask only for the minimum missing information.

When the user explicitly authorizes default copy (for example `按默认文案来`), the runtime may generate soft, non-factual campaign copy only.

Never invent phone, address, price, opening hours, certification, awards, origin, history, process, unverified ingredients/flavor, weight, health or medical claims.
