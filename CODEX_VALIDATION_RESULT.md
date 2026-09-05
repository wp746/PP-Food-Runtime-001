# PP Food Validation Engine V0 — First Live S01/S02 Result

## Git and runtime

- Branch: `validation-engine-v0`
- Validation implementation commit: `2e4c2d74f62338137ae1dc7b4ccbfbee7a47a955`
- Python: `3.12.14`
- Runtime version: `validation-v0.1.0`
- Original handoff base: `eb33cc74929c7e36a83195a00b9d2c4c9e9ef6ac`

## Verification

- Offline tests: `39 passed, 3 deselected, 0 failed`
- Private S01/S02 asset binding tests: `2 passed, 0 failed`
- ZIP checksums: all 6 private images `OK`
- Tracked-file and run-artifact credential scan: no credential-shaped value found
- SiliconFlow route: `https://api.siliconflow.cn/v1`
- SiliconFlow model: `Qwen/Qwen3-VL-32B-Instruct`
- SiliconFlow reachability: `PASS`
- Yunwu route: `https://yunwuapi.cc/v1`
- Yunwu model: `gpt-image-2`
- Yunwu reachability: `PASS`
- Yunwu reference protocol: `/images/edits` with `images[].image_url`; current Stage A binding recorded per candidate

No API key, Authorization value, or raw sensitive provider response is stored here or in the run artifacts.

## Live S01

- Case: `S01` / `椰椰西瓜冰`
- Run ID: `20260904T051630Z-31f04250`
- Real Primary generated: `YES`, `2161x3840`
- Real Challenger generated: `YES`, `2161x3840`
- Product truth: `PASS`
- Copy truth (machine evaluator): `PASS`
- Mechanical 9:16/decode: `PASS`
- Primary weighted score: `8.68`
- Challenger weighted score: `8.68`
- Final decision: `RETRY / NO_QUALIFIED_WINNER`
- Critical failure codes: none
- Floor deficits: `compositional_depth_tension=8.0 < 8.8`; `category_inevitability=8.0 < 8.5`
- Retry family: `GOLDEN_DISTANCE_RETRY / TARGETED_REPAIR`
- Review sheet: `/Users/wangpeng/Documents/ChatGPT/pp-food-代码测试/PP-Food-Runtime-001/validation_runs/S01/S01-review.jpg`

## Live S02

- Case: `S02` / `桔子罐头`
- Run ID: `20260904T052646Z-0e8dce6d`
- Real Primary generated: `YES`, `2161x3840`
- Real Challenger generated: `YES`, `2161x3840`
- Product truth: `PASS`
- Copy truth (machine evaluator): `PASS`
- Mechanical 9:16/decode: `PASS`
- Primary weighted score: `8.68`
- Challenger weighted score: `8.68`
- Final decision: `RETRY / NO_QUALIFIED_WINNER`
- Critical failure codes: none
- Floor deficits: `compositional_depth_tension=8.0 < 8.8`; `category_inevitability=8.0 < 8.5`
- Retry family: `GOLDEN_DISTANCE_RETRY / TARGETED_REPAIR`
- Review sheet: `/Users/wangpeng/Documents/ChatGPT/pp-food-代码测试/PP-Food-Runtime-001/validation_runs/S02/S02-review.jpg`

## Human-visible caveat

The independent evaluator returned the same `8.68` vector for all four images, so its ranking sensitivity is not yet trustworthy. Manual visual inspection also found a probable repeated/malformed main-title character in S02 Challenger that the evaluator marked as Copy PASS. Therefore the machine verdict remains `RETRY`; this run does not prove stability or final visual acceptance.

## Next step

Ask the user to review `S01-review.jpg` and `S02-review.jpg`. After the user identifies acceptable directions, perform failure-code-driven refinement for depth/category/copy exactness. Only after a direction is human-approved should S01/S02 enter the 3x stability harness. Mini Program work remains blocked.
