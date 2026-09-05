# PP Food V1 Production Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the validated PP Food engine into `1.0.0-rc.1` with separate VALIDATION and PRODUCTION_FAST modes, reliable evaluator/provider failure semantics, and synchronized Node handoff behavior.

**Architecture:** Keep the validated Stage A/B components intact. Add a deterministic runtime-mode policy above `StageBRunner`; Validation preserves the full two-finalist Golden flow, while Production Fast generates one Primary candidate and runs a smaller hard-delivery gate, escalating to one targeted retry only for delivery-blocking failures. Pairwise evaluation is simplified to Stage A + Primary + Challenger image slots only.

**Tech Stack:** Python 3.11+, Pydantic v2, pytest, httpx, Pillow, existing PP Food providers/artifact store.

**Spec:** `docs/superpowers/specs/2026-09-05-pp-food-v1-production-convergence-design.md`

## Global Constraints
- Source product truth remains the highest authority.
- Stage B always uses the current-job Stage A PASS image.
- PRODUCTION_FAST generates one initial B candidate.
- VALIDATION preserves two finalists + pairwise + Golden-relative evaluation.
- Provider/evaluator failures never consume creative retry cycles.
- Production maximum creative retry count is 1.
- Runtime version is `1.0.0-rc.1`.
- No API keys, private job assets, or user private Golden images are committed.

---

### Task 1: Runtime Mode Contract

**Files:**
- Modify: `src/pp_food_runtime/config.py`
- Modify: `src/pp_food_runtime/models/evaluation.py`
- Test: `tests/unit/test_config.py`
- Test: `tests/unit/test_production_modes.py`

**Interfaces:**
- Produces: `RuntimeMode` enum with `VALIDATION` and `PRODUCTION_FAST`.
- Produces settings fields `runtime_mode`, `production_max_creative_retries=1`, `validation_max_creative_cycles=3`.

- [ ] Add failing tests for default mode, env parsing, and retry limits.
- [ ] Run targeted tests and confirm failure.
- [ ] Add the enum/settings with `PP_RUNTIME_MODE` env support.
- [ ] Run targeted tests and confirm pass.
- [ ] Commit `feat: add production and validation runtime modes`.

### Task 2: Failure Taxonomy

**Files:**
- Modify: `src/pp_food_runtime/models/evaluation.py`
- Modify: `src/pp_food_runtime/providers/openai_compatible.py`
- Test: `tests/unit/test_provider_contracts.py`
- Test: `tests/unit/test_evaluator.py`

**Interfaces:**
- Produces non-creative operational failure semantics: provider timeout/transport and `EVALUATOR_FAILURE`.

- [ ] Add failing tests proving provider/evaluator failures cannot become creative failure codes.
- [ ] Run tests and confirm failure.
- [ ] Add `EVALUATOR_FAILURE` and operational classification helper/metadata without weakening hard truth gates.
- [ ] Run tests and confirm pass.
- [ ] Commit `feat: separate operational and creative failures`.

### Task 3: Pairwise Slot Isolation

**Files:**
- Modify: `src/pp_food_runtime/stage_b/evaluator.py`
- Test: `tests/unit/test_evaluator.py`

**Interfaces:**
- `BEvaluator.compare(contexts)` sends exactly three images: Stage A control, Primary, Challenger.
- Pairwise payload explicitly maps image_1=STAGE_A, image_2=Primary, image_3=Challenger.

- [ ] Add a failing fake-provider test that captures pairwise image order/count.
- [ ] Run the test and confirm the current 4+ image behavior fails it.
- [ ] Modify pairwise instruction/payload/image list.
- [ ] Keep unknown winner IDs fail-closed as evaluator failure.
- [ ] Run evaluator tests.
- [ ] Commit `fix: isolate pairwise candidate image slots`.

### Task 4: Production Hard Gate

**Files:**
- Create: `src/pp_food_runtime/stage_b/production_gate.py`
- Modify: `src/pp_food_runtime/models/evaluation.py`
- Test: `tests/unit/test_production_gate.py`

**Interfaces:**
- Produces `ProductionGateResult`.
- Produces `evaluate_production_candidate(...)` that blocks only delivery-critical failures: mechanical, reference binding, product truth, copy truth, severe hero/broken-render conditions.
- Golden soft-score shortfalls alone do not trigger retry in Production Fast.

- [ ] Write tests for hard failures, soft aesthetic shortfalls, and passing output.
- [ ] Run and confirm failure.
- [ ] Implement the minimal deterministic gate.
- [ ] Run and confirm pass.
- [ ] Commit `feat: add production delivery hard gate`.

### Task 5: Split Stage B Execution by Mode

**Files:**
- Modify: `src/pp_food_runtime/stage_b/runner.py`
- Modify: `src/pp_food_runtime/engine.py`
- Test: `tests/unit/test_production_modes.py`
- Test: `tests/integration/test_production_fast.py`

**Interfaces:**
- `VALIDATION`: existing Primary + Challenger + per-candidate eval + pairwise.
- `PRODUCTION_FAST`: Primary only, production gate, one targeted retry at most.

- [ ] Write fake-provider integration tests proving one vs two initial image calls by mode.
- [ ] Run and confirm failure.
- [ ] Refactor `StageBRunner.run()` into shared preparation + `_run_validation()` + `_run_production_fast()` while preserving artifact contracts.
- [ ] Ensure Production Fast never calls pairwise on a normal pass.
- [ ] Ensure hard provider/evaluator failures stop without creative regeneration.
- [ ] Run targeted unit/integration tests.
- [ ] Commit `feat: add production fast execution path`.

### Task 6: Human-Accepted Canonical Calibration

**Files:**
- Modify: `src/pp_food_runtime/golden/manifest.py`
- Create: `goldens/manifests/C01_STREET_FOOD.yaml`
- Modify: `src/pp_food_runtime/golden/retrieval.py` if required for calibration metadata.
- Test: `tests/unit/test_golden_repository.py`

**Interfaces:**
- Manifest supports `human_accepted` and `calibration_role` with backward-compatible defaults.
- Street-food Canonical uses `sha256: LOCAL_BIND_REQUIRED`; no private image is committed.

- [ ] Write failing manifest/repository tests.
- [ ] Implement backward-compatible metadata.
- [ ] Add C01 principles and forbidden transfer list.
- [ ] Run Golden tests.
- [ ] Commit `feat: add human accepted street food canonical`.

### Task 7: Runtime Evidence and Timing

**Files:**
- Modify: `src/pp_food_runtime/stage_b/runner.py`
- Modify: `src/pp_food_runtime/stage_a/runner.py` only if timing evidence is absent.
- Modify: `src/pp_food_runtime/config.py`
- Test: `tests/unit/test_artifact_store.py`
- Test: `tests/integration/test_production_fast.py`

**Interfaces:**
- Manifest/final decision evidence records runtime mode, runtime version, provider/model IDs, stage hashes, prompt hashes, generation latency, retry count, and failure class.

- [ ] Add failing artifact assertions.
- [ ] Implement deterministic evidence fields.
- [ ] Run targeted tests.
- [ ] Commit `feat: record production timing and failure evidence`.

### Task 8: Version and Documentation Freeze

**Files:**
- Modify: `VERSION`
- Modify: `.env.example`
- Modify: `README.md`
- Modify: `EXECUTION_MODES.md`
- Modify: `QC_GATE.md`
- Modify: `RETRY_POLICY.md`
- Create: `docs/PRODUCTION_V1_RC1.md`
- Test: existing contract tests plus full pytest.

**Interfaces:**
- Version = `1.0.0-rc.1`.
- Docs clearly distinguish Validation from Production Fast.

- [ ] Update version/env/docs.
- [ ] Run `pytest -q` and record exact pass/skip/fail.
- [ ] Run any package/type/schema export checks defined in the repo.
- [ ] Commit `release: freeze PP Food runtime 1.0.0-rc.1`.

### Task 9: Node Handoff Synchronization

**Repository:** `wp746/wp746-PP-Food-MiniProgram-Node-Handoff`

**Files:**
- Modify: `VERSION`
- Modify: `README.md`
- Modify: `HANDOFF.md`
- Modify: `docs/PROMPT_RUNTIME_FULL.md`
- Modify: `docs/NODE_INTEGRATION_GUIDE.md`
- Modify: `docs/QC_RETRY.md`
- Modify: `docs/VALIDATION_STATUS.md`
- Modify: `src/types.ts`
- Modify: `src/pipeline.ts`
- Modify: `src/ppFoodPrompts.ts` only where production policy changes are represented.
- Modify/Add tests for one-candidate fast path and validation two-candidate path.

**Interfaces:**
- Node runtime exposes matching `VALIDATION | PRODUCTION_FAST` behavior.
- Node docs map its handoff version to Runtime `1.0.0-rc.1` commit SHA.

- [ ] Add/update tests first.
- [ ] Implement the synchronized Node policy.
- [ ] Run `npm test` / `npm run typecheck` when an execution environment is available; otherwise do not claim runtime pass and mark verification pending.
- [ ] Commit with explicit Runtime source SHA in the message/body.

### Task 10: Final Cross-Repo Verification

- [ ] Compare production policy constants and documented failure semantics across both repos.
- [ ] Verify neither repo contains API keys/private assets.
- [ ] Record Runtime branch/commit and Node Handoff branch/commit.
- [ ] Report `SYNC STATUS: MATCHED` only when the behavior/version mapping is actually aligned.
