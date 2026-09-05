# PP Food Production V1 RC2

Release: `1.0.0-rc.2`

RC2 is a live-acceptance bug-fix release built from RC1. It does not change the approved visual methodology.

## Live evidence that triggered RC2

- S01 Validation generated two real candidates successfully and produced valid evaluations.
- S02 Vision returned `pack_or_food=Pack` and `primary_category=Canned fruit`.
- RC1 compared `pack_or_food` case-sensitively against `PACK`, so S02 missed `CANNED_FRUIT_RETAIL` translation.
- The wrong category prevented S02 from retrieving its own S-tier Golden and allowed unrelated Golden principles into art direction.
- The diagnostic review sheet then raised `StopIteration` when `golden-S02` was absent, aborting the remaining Production Fast smoke.

## RC2 fixes

- Normalize pack/food classification case at category-routing and Golden-retrieval boundaries.
- Route title-case `Pack` canned-fruit observations to `CANNED_FRUIT_RETAIL`.
- Make Golden retrieval treat `Pack`, `PACK`, and equivalent casing as the same pack signal.
- Make review-sheet generation fail-soft with an explicit `GOLDEN NOT RETRIEVED` placeholder instead of aborting the run.
- Preserve all RC1 Product Truth, Stage A, Production Fast, QC and retry policies.

## Acceptance status

Offline regression: required on the final RC2 commit.

Live S02 Validation + S02 Production Fast: must be re-run on RC2 before merge to `main`.
