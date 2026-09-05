# PP Food Validation Engine V0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the smallest executable PP Food Validation Engine that can run S01/S02 end-to-end with real provider calls, deterministic prompt compilation, artifact logging, independent Golden-relative evaluation, and repeatable validation runs.

**Architecture:** Implement a Python 3.11+ local-first core package under `src/pp_food_runtime/`. Host clients submit typed contracts; the engine owns product truth, category translation, Golden retrieval, prompt compilation, provider invocation, evaluation, retry decisions, and artifact persistence. Real providers are OpenAI-compatible adapters configured only through environment variables; tests use deterministic mocks. Golden image assets remain local/private and are referenced through manifests plus SHA-256 hashes; the repository stores manifests/schema/examples, not the user's image binaries.

**Tech Stack:** Python 3.11+, Pydantic v2, httpx, Typer, PyYAML, Pillow, pytest, pytest-asyncio.

**Spec:** `docs/superpowers/specs/2026-09-04-pp-food-validation-engine-v0-design.md`

## Global Constraints

- Validation V0 is not the final miniprogram architecture freeze.
- Host agents are clients only; they may not alter art direction, prompt structure, category logic, retry policy, or QC.
- Product truth is a hard gate; creative scores cannot compensate for fidelity failure.
- Stage B requires a current-job Stage A pass reference.
- Stage B locks product DNA but does not lock the Stage A camera composition or the previous `<=15%` apparent-scale rule.
- Category is context/constraint, never a fixed visual template.
- Principle transfer from Goldens is allowed; exact skin, copy, palette, layout, props, and old brand transfer is forbidden.
- B produces exactly one Primary direction and one Challenger direction before winner selection.
- Generator reasoning/self-scores are not visible to the evaluator.
- Weighted Golden score is advisory only and cannot override hard failures.
- Maximum B creative cycles in Validation V0 is 3.
- Golden promotion remains human-only: machine outputs may be `GOLDEN_CANDIDATE`, never `GOLD`, `CANONICAL`, or `S-TIER`.
- Secrets are read from environment variables and are never stored in prompts, artifacts, test fixtures, manifests, or repository files.
- User Golden images are not committed to the repository; local asset paths are ignored by Git and validated against manifest hashes.
- Unit/contract tests must run with no network and no provider credentials.
- Real-provider tests are opt-in and must skip cleanly when credentials are absent.

---

## File Structure

Create the executable implementation alongside the legacy Markdown runtime. Do not delete the existing V1.4 documents during Validation V0.

```text
pyproject.toml
.env.example
.gitignore
src/pp_food_runtime/
  __init__.py
  cli.py
  config.py
  models/
    common.py
    job.py
    product.py
    visual.py
    evaluation.py
  artifacts/
    store.py
  golden/
    manifest.py
    repository.py
    retrieval.py
  providers/
    base.py
    openai_compatible.py
    mock.py
  vision/
    analyzer.py
  stage_a/
    contract.py
    runner.py
  stage_b/
    copy_firewall.py
    translator.py
    art_director.py
    compiler.py
    evaluator.py
    retry.py
    runner.py
  engine.py
goldens/
  manifests/
    S01.yaml
    S02.yaml
    A01.yaml
    A02.yaml
    A03.yaml
  assets/.gitkeep
tests/
  unit/
  contract/
  integration/
```

`goldens/assets/` is local-only; `.gitignore` must ignore all files beneath it except `.gitkeep`.

---

### Task 1: Python Package Skeleton and Runtime Configuration

**Files:**
- Create: `pyproject.toml`
- Create: `.env.example`
- Modify/Create: `.gitignore`
- Create: `src/pp_food_runtime/__init__.py`
- Create: `src/pp_food_runtime/config.py`
- Test: `tests/unit/test_config.py`

**Interfaces:**
- Produces: `RuntimeSettings.from_env() -> RuntimeSettings`
- Produces fields used by later tasks: `runtime_version`, `artifact_root`, `golden_root`, `vision_base_url`, `vision_model`, `vision_api_key`, `image_base_url`, `image_model`, `image_api_key`, `request_timeout_seconds`, `real_provider_enabled`.

- [ ] **Step 1: Write the failing configuration tests**

```python
# tests/unit/test_config.py
from pp_food_runtime.config import RuntimeSettings


def test_settings_defaults_are_local_and_safe(monkeypatch, tmp_path):
    for key in (
        "PP_VISION_BASE_URL", "PP_VISION_API_KEY", "PP_VISION_MODEL",
        "PP_IMAGE_BASE_URL", "PP_IMAGE_API_KEY", "PP_IMAGE_MODEL",
    ):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("PP_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    monkeypatch.setenv("PP_GOLDEN_ROOT", str(tmp_path / "goldens"))

    settings = RuntimeSettings.from_env()

    assert settings.real_provider_enabled is False
    assert settings.request_timeout_seconds == 120
    assert settings.runtime_version.startswith("validation-v0")


def test_real_provider_requires_complete_credentials(monkeypatch):
    monkeypatch.setenv("PP_VISION_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("PP_VISION_MODEL", "vision-model")
    monkeypatch.setenv("PP_VISION_API_KEY", "secret")
    monkeypatch.setenv("PP_IMAGE_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("PP_IMAGE_MODEL", "image-model")
    monkeypatch.setenv("PP_IMAGE_API_KEY", "secret")

    settings = RuntimeSettings.from_env()

    assert settings.real_provider_enabled is True
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `pytest tests/unit/test_config.py -v`
Expected: import/module failure because the package does not exist yet.

- [ ] **Step 3: Implement package metadata and `RuntimeSettings`**

`pyproject.toml` must declare Python `>=3.11`, dependencies `pydantic>=2.8`, `httpx>=0.27`, `typer>=0.12`, `PyYAML>=6.0`, `Pillow>=10.0`, and pytest dev dependencies. `RuntimeSettings.from_env()` must never print or serialize API keys.

Use environment names exactly:

```text
PP_RUNTIME_VERSION
PP_ARTIFACT_ROOT
PP_GOLDEN_ROOT
PP_VISION_BASE_URL
PP_VISION_API_KEY
PP_VISION_MODEL
PP_IMAGE_BASE_URL
PP_IMAGE_API_KEY
PP_IMAGE_MODEL
PP_REQUEST_TIMEOUT_SECONDS
```

- [ ] **Step 4: Add `.env.example` and Golden asset ignore rules**

`.env.example` contains empty credential values only. `.gitignore` includes:

```text
.env
.venv/
__pycache__/
.pytest_cache/
artifacts/
goldens/assets/*
!goldens/assets/.gitkeep
```

- [ ] **Step 5: Run the tests**

Run: `pytest tests/unit/test_config.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml .env.example .gitignore src/pp_food_runtime tests/unit/test_config.py
git commit -m "feat: scaffold validation runtime"
```

---

### Task 2: Typed Job, Product Truth, Visual Direction, and Evaluation Contracts

**Files:**
- Create: `src/pp_food_runtime/models/common.py`
- Create: `src/pp_food_runtime/models/job.py`
- Create: `src/pp_food_runtime/models/product.py`
- Create: `src/pp_food_runtime/models/visual.py`
- Create: `src/pp_food_runtime/models/evaluation.py`
- Test: `tests/contract/test_models.py`

**Interfaces:**
- Produces `JobMode`, `JobState`, `ImageRef`, `UserFacts`, `JobContract`.
- Produces `ProductTruth`, `SensorySemantic`, `ProductLockBridge`.
- Produces `CategoryVisualTranslation`, `ArtDirection`, `GoldenPrinciplePack`.
- Produces `GoldenVector`, `EvaluationResult`, `FailureCode`, `PassFreezeMap`.

- [ ] **Step 1: Write contract tests for forbidden invalid states**

```python
# tests/contract/test_models.py
import pytest
from pydantic import ValidationError
from pp_food_runtime.models.job import JobContract, JobMode, ImageRef, UserFacts
from pp_food_runtime.models.visual import ArtDirection


def test_b_job_requires_source_image():
    with pytest.raises(ValidationError):
        JobContract(mode=JobMode.B, source_image=None, user_facts=UserFacts())


def test_art_direction_requires_one_big_idea_and_product_hero():
    with pytest.raises(ValidationError):
        ArtDirection.model_validate({"concept_id": "primary"})


def test_user_facts_separates_verified_facts_from_default_copy():
    facts = UserFacts(
        product_name="椰椰西瓜冰",
        brand="有幸小食院",
        default_copy_authorized=True,
    )
    assert facts.product_name == "椰椰西瓜冰"
    assert facts.default_copy_authorized is True
```

- [ ] **Step 2: Run contract tests and verify failure**

Run: `pytest tests/contract/test_models.py -v`
Expected: FAIL because the model modules are absent.

- [ ] **Step 3: Implement enums and exact model fields**

`JobState` must include:

```text
B_REQUESTED
B_ENTRY_VALIDATION
STAGE_A_REQUIRED
STAGE_A_PASS
PRODUCT_LOCK_BRIDGE_READY
COPY_FIREWALL_READY
CURRENT_PRODUCT_ANALYSIS
CATEGORY_VISUAL_TRANSLATION
GOLDEN_RETRIEVAL
ART_DIRECTION
ART_DIRECTION_VALIDATION
PROMPT_CONTRACT_READY
FINALIST_RENDER
FINALIST_VISUAL_EVAL
WINNER_SELECTION
TARGETED_REFINEMENT
FINAL_QC
B_PASS
NEEDS_USER_FACT
PROVIDER_FAILURE
RUNTIME_FAILURE
NEEDS_HUMAN_REVIEW
```

`GoldenVector` fields are the eight approved dimensions and validate each score in `[0, 10]`.

- [ ] **Step 4: Add model-level invariants**

`JobContract` validates mode B has a source image. `ArtDirection` requires a non-empty one-big-idea sentence, product-hero strategy, typography relationship, composition, and forbidden-drift list. `EvaluationResult` rejects `PASS` when any critical failure is present.

- [ ] **Step 5: Run tests**

Run: `pytest tests/contract/test_models.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/pp_food_runtime/models tests/contract/test_models.py
git commit -m "feat: define validation contracts"
```

---

### Task 3: Artifact Store and Reproducibility Hashes

**Files:**
- Create: `src/pp_food_runtime/artifacts/store.py`
- Test: `tests/unit/test_artifact_store.py`

**Interfaces:**
- Produces `sha256_file(path: Path) -> str`
- Produces `ArtifactStore.create_job(job: JobContract) -> Path`
- Produces `ArtifactStore.write_json(job_id: str, name: str, payload: BaseModel | dict) -> Path`
- Produces `ArtifactStore.copy_image(job_id: str, label: str, source: Path) -> ImageRef`

- [ ] **Step 1: Write failing persistence tests**

```python
from pathlib import Path
from pp_food_runtime.artifacts.store import ArtifactStore, sha256_file


def test_copy_image_records_hash_and_never_overwrites(tmp_path):
    source = tmp_path / "source.png"
    source.write_bytes(b"image-bytes")
    store = ArtifactStore(tmp_path / "artifacts")

    first = store.copy_image("job-1", "source", source)
    second = store.copy_image("job-1", "source", source)

    assert first.sha256 == sha256_file(source)
    assert first.path != second.path
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/unit/test_artifact_store.py -v`
Expected: FAIL due to missing implementation.

- [ ] **Step 3: Implement atomic JSON/image writes**

Artifacts must use job-scoped directories and never include API keys. JSON writes use UTF-8, `ensure_ascii=False`, sorted keys, and a temporary-file + rename pattern.

- [ ] **Step 4: Run tests**

Run: `pytest tests/unit/test_artifact_store.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/pp_food_runtime/artifacts tests/unit/test_artifact_store.py
git commit -m "feat: add reproducible artifact store"
```

---

### Task 4: Golden Manifests, Local Asset Binding, and Principle Retrieval

**Files:**
- Create: `src/pp_food_runtime/golden/manifest.py`
- Create: `src/pp_food_runtime/golden/repository.py`
- Create: `src/pp_food_runtime/golden/retrieval.py`
- Create: `goldens/manifests/S01.yaml`
- Create: `goldens/manifests/S02.yaml`
- Create: `goldens/manifests/A01.yaml`
- Create: `goldens/manifests/A02.yaml`
- Create: `goldens/manifests/A03.yaml`
- Create: `goldens/assets/.gitkeep`
- Test: `tests/unit/test_golden_repository.py`

**Interfaces:**
- Produces `GoldenManifest`, `GoldenTier`.
- Produces `GoldenRepository.load_all() -> list[GoldenManifest]`.
- Produces `GoldenRepository.bind_local_asset(golden_id, path) -> GoldenManifest` with SHA verification.
- Produces `GoldenRetriever.retrieve(query, limit=3) -> list[GoldenPrinciplePack]`.

- [ ] **Step 1: Write tests that reject Bakery as an approved Golden and reject hash mismatches**

```python
from pathlib import Path
import pytest
from pp_food_runtime.golden.repository import GoldenRepository, GoldenAssetHashMismatch


def test_initial_manifests_have_two_s_tier_and_no_bakery_canonical(tmp_path):
    repo = GoldenRepository(Path("goldens/manifests"), tmp_path)
    manifests = repo.load_all()
    assert {m.golden_id for m in manifests if m.tier.value == "S_TIER"} == {"S01", "S02"}
    assert all(m.primary_category != "BAKERY" for m in manifests)


def test_bind_local_asset_rejects_wrong_hash(tmp_path):
    repo = GoldenRepository(Path("goldens/manifests"), tmp_path)
    bad = tmp_path / "bad.png"
    bad.write_bytes(b"wrong")
    with pytest.raises(GoldenAssetHashMismatch):
        repo.bind_local_asset("S01", bad)
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/unit/test_golden_repository.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement manifests using approved principles only**

Each YAML includes:

```yaml
golden_id: S01
tier: S_TIER
name: 椰椰西瓜冰夏日广告海报
primary_category: COLD_DRINK_FRUIT_DESSERT
asset_filename: S01.png
sha256: "LOCAL_BIND_REQUIRED"
transferable_principles:
  - strong product + strong headline dual-core hierarchy
  - sensory-to-material typography translation
  - multi-depth co-composition
prohibited_transfer:
  - old brand
  - old copy
  - exact palette
  - exact props
  - exact layout
```

`LOCAL_BIND_REQUIRED` means the manifest is structurally valid but cannot be used for live image-relative evaluation until the local asset is registered and the manifest copy in the artifact workspace contains the real SHA. Repository source manifests never receive secret/private image bytes.

- [ ] **Step 4: Implement deterministic de-skinned retrieval**

Retrieval scores category compatibility, `pack_or_food`, sensory-tag overlap, and target visual problem; it returns principle packs only. Ties sort by `tier_rank`, then `golden_id` so repeated calls are deterministic.

- [ ] **Step 5: Run tests**

Run: `pytest tests/unit/test_golden_repository.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/pp_food_runtime/golden goldens tests/unit/test_golden_repository.py
git commit -m "feat: add human-approved golden repository"
```

---

### Task 5: Provider Interfaces, OpenAI-Compatible Adapters, and Deterministic Mocks

**Files:**
- Create: `src/pp_food_runtime/providers/base.py`
- Create: `src/pp_food_runtime/providers/openai_compatible.py`
- Create: `src/pp_food_runtime/providers/mock.py`
- Test: `tests/unit/test_provider_contracts.py`
- Test: `tests/integration/test_real_provider_smoke.py`

**Interfaces:**
- Produces `VisionProvider.analyze(images, instruction, response_model) -> BaseModel`.
- Produces `ImageProvider.generate(reference_images, prompt, aspect_ratio, output_path) -> ImageRef`.
- Produces `ProviderCapabilityProfile`.
- `OpenAICompatibleVisionProvider` and `OpenAICompatibleImageProvider` consume only `RuntimeSettings`.

- [ ] **Step 1: Write provider-contract tests with fake transport**

Test that current-job reference images are always attached, API keys are sent only in authorization headers, and provider prompts never include the key.

```python
def test_image_provider_requires_reference_binding(mock_image_provider, tmp_path):
    result = mock_image_provider.generate(
        reference_images=[], prompt="test", aspect_ratio="9:16", output_path=tmp_path / "out.png"
    )
    assert result.reference_binding_verified is False
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/unit/test_provider_contracts.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement explicit provider capability profiles**

Minimum capability fields: `reference_edit`, `multiple_references`, `masks`, `seed`, `text_rendering`, `aspect_ratio`, `max_resolution`. Provider invocation records model/base URL/capabilities but not credentials.

- [ ] **Step 4: Implement OpenAI-compatible request builders**

Keep request-path construction isolated in the adapter. Accept aggregate APIs that expose OpenAI-compatible chat/vision and image endpoints; do not let Stage B know endpoint details.

- [ ] **Step 5: Implement deterministic mock providers**

Mock Vision returns fixture models. Mock Image copies a supplied fixture image and records the prompt/reference list so end-to-end unit tests are stable.

- [ ] **Step 6: Add opt-in real-provider smoke test**

`tests/integration/test_real_provider_smoke.py` uses `pytest.mark.integration` and calls `pytest.skip()` unless `RuntimeSettings.real_provider_enabled` is true. It must perform one tiny provider call and assert an image/structured response is returned; it must not run by default.

- [ ] **Step 7: Run offline tests**

Run: `pytest tests/unit/test_provider_contracts.py -v`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/pp_food_runtime/providers tests/unit/test_provider_contracts.py tests/integration/test_real_provider_smoke.py
git commit -m "feat: add provider abstraction"
```

---

### Task 6: Vision Product Truth, Stage A Contract, and Copy Firewall

**Files:**
- Create: `src/pp_food_runtime/vision/analyzer.py`
- Create: `src/pp_food_runtime/stage_a/contract.py`
- Create: `src/pp_food_runtime/stage_a/runner.py`
- Create: `src/pp_food_runtime/stage_b/copy_firewall.py`
- Test: `tests/unit/test_product_truth_and_copy.py`

**Interfaces:**
- Produces `ProductAnalyzer.analyze(source: ImageRef, user_facts: UserFacts) -> ProductTruth`.
- Produces `StageARunner.run(job, source, truth) -> StageAResult`.
- Produces `CopyFirewall.build(user_facts) -> CopyAllowlist`.

- [ ] **Step 1: Write tests for truth/copy behavior**

```python
def test_default_copy_does_not_invent_hard_facts(copy_firewall):
    allowlist = copy_firewall.build(UserFacts(
        product_name="阳光蜜橘罐头",
        brand="测试品牌",
        default_copy_authorized=True,
    ))
    assert allowlist.product_name == "阳光蜜橘罐头"
    assert allowlist.price is None
    assert allowlist.address is None
    assert allowlist.phone is None
```

Also test that `ProductTruth` distinguishes observed/inferred/unknown and that Stage A result stores the exact source hash it was derived from.

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/unit/test_product_truth_and_copy.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement Product Analyzer with a strict structured vision instruction**

Vision instruction explicitly states it is an observer, not a creative director. It must separate `observed`, `high_confidence_inferred`, and `unknown` values and must not invent business facts.

- [ ] **Step 4: Implement minimal Stage A path**

For Validation V0 vertical slice, Stage A runner must support two modes:

1. `provided_pass_reference`: use a known approved/local Stage A pass image, verify hash, and create `ProductLockBridge`.
2. `generate`: compile a fidelity-first Stage A prompt and invoke the ImageProvider.

The first live S01/S02 vertical slice may use provided pass references if available; it must still create the same typed `StageAResult` as generated mode.

- [ ] **Step 5: Implement Copy Firewall**

Output only verified hard facts plus separately flagged authorized soft-copy slots. Hard-fact absence remains `None`.

- [ ] **Step 6: Run tests**

Run: `pytest tests/unit/test_product_truth_and_copy.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/pp_food_runtime/vision src/pp_food_runtime/stage_a src/pp_food_runtime/stage_b/copy_firewall.py tests/unit/test_product_truth_and_copy.py
git commit -m "feat: lock product truth and copy facts"
```

---

### Task 7: Category Visual Translation and Primary/Challenger Art Direction

**Files:**
- Create: `src/pp_food_runtime/stage_b/translator.py`
- Create: `src/pp_food_runtime/stage_b/art_director.py`
- Test: `tests/unit/test_art_direction.py`

**Interfaces:**
- Produces `CategoryTranslator.translate(truth, user_facts) -> CategoryVisualTranslation`.
- Produces `BArtDirector.create_directions(truth, translation, copy, goldens) -> tuple[ArtDirection, ArtDirection]`.

- [ ] **Step 1: Write anti-template tests**

```python
def test_bakery_translation_does_not_force_oven_or_wood_sign(translator, bagel_truth):
    result = translator.translate(bagel_truth, UserFacts(product_name="碱水原味贝果"))
    joined = " ".join(result.forbidden_drift + [result.one_big_idea_seed])
    assert "oven tunnel" not in joined.lower()
    assert "wooden sign" not in joined.lower()


def test_primary_and_challenger_differ_in_two_structural_dimensions(art_director, fixtures):
    primary, challenger = art_director.create_directions(**fixtures)
    differences = sum([
        primary.composition.dominant_axis != challenger.composition.dominant_axis,
        primary.typography.spatial_behavior != challenger.typography.spatial_behavior,
        primary.product_hero.position != challenger.product_hero.position,
        primary.composition.depth_architecture != challenger.composition.depth_architecture,
    ])
    assert differences >= 2
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/unit/test_art_direction.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement sensory-to-visual translator**

Translator output must include sensory evidence, emotional semantics, one primary + at most one secondary material metaphor, typography behavior, color/light/spatial/motion translations, information density, and forbidden drift.

- [ ] **Step 4: Implement structured Art Director**

The Art Director may use Vision/LLM provider structured output, but returns only validated `ArtDirection`; it never returns a provider prompt. Add validator checks for product traceability, typography traceability, Big Idea traceability, no old brand/copy, and no literal category shortcut dependence.

- [ ] **Step 5: Run tests**

Run: `pytest tests/unit/test_art_direction.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/pp_food_runtime/stage_b/translator.py src/pp_food_runtime/stage_b/art_director.py tests/unit/test_art_direction.py
git commit -m "feat: derive product-specific kv directions"
```

---

### Task 8: Deterministic Stage B Prompt Compiler

**Files:**
- Create: `src/pp_food_runtime/stage_b/compiler.py`
- Test: `tests/unit/test_b_compiler.py`
- Test: `tests/contract/test_prompt_determinism.py`

**Interfaces:**
- Produces `compile_stage_b(contract: ValidatedBPromptContract, profile: ProviderCapabilityProfile) -> CompiledPrompt`.

- [ ] **Step 1: Write exact-order and determinism tests**

```python
def test_stage_b_prompt_uses_canonical_section_order(validated_b_contract, provider_profile):
    prompt = compile_stage_b(validated_b_contract, provider_profile).text
    headings = [
        "OUTPUT CONTRACT", "REFERENCE AUTHORITY", "PRODUCT IDENTITY LOCK",
        "PRODUCT SURFACE LOCK", "PACKAGE / VESSEL / TOPOLOGY LOCK",
        "CURRENT PRODUCT SEMANTICS", "ONE BIG IDEA", "PRODUCT HERO DIRECTION",
        "TYPOGRAPHY DIRECTION", "PRODUCT–TYPOGRAPHY RELATIONSHIP",
        "COMPOSITION / DEPTH", "CATEGORY-NATIVE ATMOSPHERE", "COLOR",
        "LIGHTING", "INFORMATION SYSTEM", "GOLDEN QUALITY TARGET",
        "HARD NEGATIVES", "FINAL CORE COMMAND",
    ]
    positions = [prompt.index(h) for h in headings]
    assert positions == sorted(positions)


def test_same_contract_same_profile_same_prompt(validated_b_contract, provider_profile):
    assert compile_stage_b(validated_b_contract, provider_profile).text == compile_stage_b(validated_b_contract, provider_profile).text
```

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/unit/test_b_compiler.py tests/contract/test_prompt_determinism.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement compiler as pure deterministic code**

No provider call and no LLM call occurs inside the compiler. Normalize lists, ordering, and whitespace. Do not include generator self-scores, rejected candidates, whole Golden manifests, or historical examples.

- [ ] **Step 4: Add provider-capability branching tests**

When native text rendering is weak, compiler emphasizes reserved typography-bearing structures and exact copy zones; when native text rendering is strong, it may request exact text but never alters copy content.

- [ ] **Step 5: Run tests**

Run: `pytest tests/unit/test_b_compiler.py tests/contract/test_prompt_determinism.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/pp_food_runtime/stage_b/compiler.py tests/unit/test_b_compiler.py tests/contract/test_prompt_determinism.py
git commit -m "feat: compile deterministic stage b prompts"
```

---

### Task 9: Independent Golden-Relative Evaluator and Retry Decisions

**Files:**
- Create: `src/pp_food_runtime/stage_b/evaluator.py`
- Create: `src/pp_food_runtime/stage_b/retry.py`
- Test: `tests/unit/test_evaluator.py`
- Test: `tests/unit/test_retry.py`

**Interfaces:**
- Produces `BEvaluator.evaluate(context: EvaluationContext) -> EvaluationResult`.
- Produces `RetryPlanner.plan(result: EvaluationResult, cycle: int) -> RetryPlan`.

- [ ] **Step 1: Write failure-logic tests before implementation**

```python
def test_hard_product_failure_cannot_be_compensated():
    result = EvaluationResult.for_test(
        product_truth_pass=False,
        golden_vector={
            "product_hero_strength": 10,
            "headline_aggression": 10,
            "typography_product_symbiosis": 10,
            "one_big_idea_clarity": 10,
            "compositional_depth_tension": 10,
            "category_inevitability": 10,
            "information_density_control": 10,
            "commercial_finish": 10,
        },
    )
    assert result.final_decision != "PASS"


def test_pairwise_winner_can_still_be_unqualified():
    result = make_eval(weighted_score=8.1, core_floor_fail=True, pairwise_winner="primary")
    assert result.final_decision == "RETRY"
```

Also test two `materially_weaker` core Golden-relative dimensions cause retry, evidence-insufficient score is capped at 7.5, and confidence `<0.65` causes `NEEDS_SECOND_EVALUATION`.

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/unit/test_evaluator.py tests/unit/test_retry.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement evaluator input isolation**

Evaluator context contains source, Stage A, current B image, truth/copy contracts, translation, and relevant Golden refs only. It has no fields for generator rationale or self-score.

- [ ] **Step 4: Implement approved evaluation sequence**

Mechanical -> Product Truth -> Copy Truth -> First Read -> Golden Vector -> Pairwise -> Golden Relative -> Anti-patterns -> Commercial Finish -> Decision.

Hard anti-patterns include `SAFE_EDITORIAL_COLLAPSE`, `SCENE_DOMINATES_PRODUCT`, `CATEGORY_CLICHE_DEPENDENCE`, `GENERIC_PREMIUM_SKIN`, `TEMPLATE_REUSE`, `PHOTO_PLUS_TEXT`, `INFORMATION_STARVATION`, and `INFORMATION_OVERLOAD`.

- [ ] **Step 5: Implement retry mapping and pass-freeze map**

Map failure codes to retry families exactly as defined in the spec. Cycle 1 is targeted repair, cycle 2 concept adjustment, cycle 3 art-direction rebuild; cycle >3 returns `NEEDS_HUMAN_REVIEW`.

- [ ] **Step 6: Run tests**

Run: `pytest tests/unit/test_evaluator.py tests/unit/test_retry.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/pp_food_runtime/stage_b/evaluator.py src/pp_food_runtime/stage_b/retry.py tests/unit/test_evaluator.py tests/unit/test_retry.py
git commit -m "feat: add independent golden evaluator"
```

---

### Task 10: Stage B Runner, Engine Orchestration, and Local CLI

**Files:**
- Create: `src/pp_food_runtime/stage_b/runner.py`
- Create: `src/pp_food_runtime/engine.py`
- Create: `src/pp_food_runtime/cli.py`
- Test: `tests/contract/test_engine_state_machine.py`
- Test: `tests/integration/test_mock_vertical_slice.py`

**Interfaces:**
- Produces `ValidationEngine.run(job: JobContract) -> JobResult`.
- Produces CLI command `ppfood validate-b`.

- [ ] **Step 1: Write state-machine test**

```python
def test_b_runner_never_renders_before_stage_a_pass(engine_with_mocks, job_b):
    result = engine_with_mocks.run(job_b)
    assert result.state_history.index("STAGE_A_PASS") < result.state_history.index("FINALIST_RENDER")
```

- [ ] **Step 2: Write mock end-to-end test**

Use deterministic mock Vision/Image providers and a bound local dummy Golden. Assert the run creates product analysis, translation, Golden retrieval, two directions, two compiled prompts, two finalist artifacts, evaluation, winner/refinement decision, and final artifact manifest.

- [ ] **Step 3: Run and verify failure**

Run: `pytest tests/contract/test_engine_state_machine.py tests/integration/test_mock_vertical_slice.py -v`
Expected: FAIL.

- [ ] **Step 4: Implement runner and engine orchestration**

`StageBRunner` owns the exact state transition order. `ValidationEngine` wires dependencies; CLI is only a client. No CLI option can inject a raw custom image prompt.

- [ ] **Step 5: Implement CLI**

Command shape:

```bash
ppfood validate-b \
  --source /path/to/source.png \
  --product-name "椰椰西瓜冰" \
  --brand "有幸小食院" \
  --default-copy \
  --golden-case S01
```

Optional verified facts are passed as explicit flags or a JSON facts file. CLI prints job ID, final state, artifact directory, and final image path only; it never prints credentials.

- [ ] **Step 6: Run tests**

Run: `pytest tests/contract/test_engine_state_machine.py tests/integration/test_mock_vertical_slice.py -v`
Expected: PASS.

- [ ] **Step 7: Run full offline suite**

Run: `pytest -m "not integration" -v`
Expected: all offline tests PASS.

- [ ] **Step 8: Commit**

```bash
git add src/pp_food_runtime/stage_b/runner.py src/pp_food_runtime/engine.py src/pp_food_runtime/cli.py tests/contract/test_engine_state_machine.py tests/integration/test_mock_vertical_slice.py
git commit -m "feat: run validation engine vertical slice"
```

---

### Task 11: Bind S01/S02 Private Golden Assets and Run First Real End-to-End Validation

**Files:**
- Create locally only: `goldens/assets/S01.png`
- Create locally only: `goldens/assets/S02.png`
- Create locally only: `validation_inputs/S01-source.png` and `validation_inputs/S02-source.png` when source images are available
- Create: `tests/integration/test_s01_s02_live.py`
- Artifacts: `artifacts/live/<job-id>/...`

**Interfaces:**
- Consumes real configured providers and exact S01/S02 private image assets.
- Produces real candidate images plus evaluation evidence.

- [ ] **Step 1: Materialize the approved S01/S02 images into the local Validation workspace**

Use the user's private Library versions already identified in the design phase. Compute SHA-256 and bind them through `GoldenRepository.bind_local_asset`; do not commit the image files.

- [ ] **Step 2: Verify live provider configuration before spending generation calls**

Run:

```bash
python -m pp_food_runtime.cli provider-check
```

Expected: both Vision and Image adapters report model name, capability profile, endpoint reachability, and `credentials_present=true` without printing keys.

If credentials are absent, stop here and request only the missing provider configuration from the user; do not ask for unrelated setup information.

- [ ] **Step 3: Run one S01 live vertical slice**

Run:

```bash
ppfood validate-b --case S01 --live
```

Expected: real Primary and Challenger images, independent evaluation JSON, a qualified winner or explicit retry/no-qualified-winner result, and complete artifacts.

- [ ] **Step 4: Inspect failure codes before changing creative logic**

If provider/reference binding fails, fix the provider adapter only. If product fidelity fails, fix truth/reference handling only. If creative quality fails, use evaluator failure codes and pass-freeze map; do not make a case-specific prompt patch.

- [ ] **Step 5: Run one S02 live vertical slice**

Run:

```bash
ppfood validate-b --case S02 --live
```

Expected: same artifact completeness as S01.

- [ ] **Step 6: Declare the visual-validation gate open only when both cases generate actual inspectable candidates**

At this exact point notify the user: `现在可以开始看图验证了。`

Do not claim stability yet.

- [ ] **Step 7: Commit only code/test changes**

Never commit live images or private inputs.

```bash
git add tests/integration/test_s01_s02_live.py
git commit -m "test: add s01 s02 live validation harness"
```

---

### Task 12: 3x Stability Harness and Canonical Regression Runner

**Files:**
- Create: `src/pp_food_runtime/eval_suite.py`
- Create: `tests/integration/test_stability_harness.py`
- Create: `goldens/regression_suite.yaml`

**Interfaces:**
- Produces `run_case(case_id: str, repeats: int = 3) -> StabilityReport`.
- Produces `run_release_suite() -> RegressionReport`.

- [ ] **Step 1: Write deterministic report aggregation tests**

Assert report fields include `fidelity_pass_rate`, `copy_pass_rate`, `category_pass_rate`, `upper_bound_pass_rate`, `worst_run_weighted_score`, `catastrophic_drift_count`, `best_run`, `median_run`, and `worst_run`.

- [ ] **Step 2: Run and verify failure**

Run: `pytest tests/integration/test_stability_harness.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement V0 stability gates exactly**

Per case: fidelity 3/3, copy 3/3, category 3/3, catastrophic drift 0, upper-bound pass >=2/3, worst-run score >=8.0.

- [ ] **Step 4: Define release suite**

```yaml
cases:
  - S01
  - S02
  - A01
  - A02
  - A03
repeats: 3
```

Bakery remains excluded until the user approves a newly generated Bakery Canonical.

- [ ] **Step 5: Run tests**

Run: `pytest tests/integration/test_stability_harness.py -v`
Expected: PASS with mocks.

- [ ] **Step 6: Run S01/S02 real 3x stability first**

Run:

```bash
ppfood eval --cases S01,S02 --repeats 3 --live
```

Only after S01/S02 pass should the suite expand to A01/A02/A03.

- [ ] **Step 7: Commit**

```bash
git add src/pp_food_runtime/eval_suite.py tests/integration/test_stability_harness.py goldens/regression_suite.yaml
git commit -m "feat: add golden stability regression suite"
```

---

### Task 13: Bakery Re-Entry and Human Canonical Promotion

**Files:**
- Create after successful generation only: `goldens/manifests/B01.yaml`
- Modify: `goldens/regression_suite.yaml`
- Test: `tests/contract/test_bakery_promotion.py`

**Interfaces:**
- Consumes the new human-approved Bakery result.
- Produces B01 only after explicit user approval.

- [ ] **Step 1: Run the new Bakery/贝果 case with the validated engine without any Bakery Golden anchor**

Use only S01/S02/A01-A03 transferable principles selected by retrieval. The old 欧丰园贝果 output remains forbidden as a Golden reference.

- [ ] **Step 2: Present only qualified Bakery candidates to the user**

If no candidate reaches the current quality floor, keep iterating through failure-code-driven engine changes and regression checks; do not promote a mediocre result to fill the category.

- [ ] **Step 3: Wait for explicit human approval**

Only a user statement equivalent to “这张可以作为烘焙 Canonical” authorizes B01.

- [ ] **Step 4: Write a failing promotion-guard test**

Test that `B01.yaml` cannot exist with `approval_status != HUMAN_APPROVED_CANONICAL`.

- [ ] **Step 5: Create B01 manifest and add it to regression suite**

Store only de-skinned principles and local asset hash binding; do not commit the image itself.

- [ ] **Step 6: Run full six-case regression**

Run:

```bash
ppfood eval --release --live
```

Expected: S01/S02 no major regression, no material degradation in two or more Canonicals, Bakery passes its 3x stability gate.

- [ ] **Step 7: Commit**

```bash
git add goldens/manifests/B01.yaml goldens/regression_suite.yaml tests/contract/test_bakery_promotion.py
git commit -m "feat: add human-approved bakery canonical"
```

---

### Task 14: Freeze Validation Runtime and Produce Handoff Readiness Evidence

**Files:**
- Create: `docs/validation/V0-RESULTS.md`
- Create: `docs/validation/V0-HANDOFF-GATE.md`
- Modify: `VERSION`
- Modify: `README.md`

**Interfaces:**
- Produces the evidence required before a separate miniprogram productionization design begins.

- [ ] **Step 1: Run the entire offline test suite**

Run: `pytest -m "not integration" -v`
Expected: PASS.

- [ ] **Step 2: Run the complete live release regression suite**

Run: `ppfood eval --release --live`
Expected: every approved case meets the V0 stability gates.

- [ ] **Step 3: Demonstrate host/client independence**

Run one identical serialized `JobContract` through the CLI and directly through `ValidationEngine.run()`. Assert the serialized validated contract, compiled prompt hash, provider profile hash, and QC policy hash are identical.

- [ ] **Step 4: Write results with evidence rather than claims**

`V0-RESULTS.md` records per case: run IDs, runtime version, provider model/profile hash, pass rates, best/median/worst scores, failure counts, and user promotion decisions. Do not embed private images or credentials.

- [ ] **Step 5: Evaluate the miniprogram handoff gate**

`V0-HANDOFF-GATE.md` must mark each design-spec acceptance condition PASS/FAIL. If any condition fails, do not freeze.

- [ ] **Step 6: Freeze runtime version only after all gates pass**

Set `VERSION` to a frozen validation release such as `2.0.0-validation.1` only after evidence is complete.

- [ ] **Step 7: Commit**

```bash
git add docs/validation VERSION README.md
git commit -m "release: freeze validated runtime"
```

At this point—and not earlier—start a separate productionization design for Docker/cloud API/API-key isolation and copy-paste miniprogram client integration code.

---

## Self-Review

### Spec coverage

- Host independence: Tasks 8, 10, 14.
- Product truth/Stage A bridge: Tasks 2, 6, 10.
- Category translation and de-skinned Golden retrieval: Tasks 4, 7.
- Primary/Challenger policy: Tasks 7, 10.
- Deterministic compiler: Task 8.
- Provider capability/reference binding: Task 5.
- Independent evaluator and anti-pattern rules: Task 9.
- Failure-code retry/pass-freeze: Task 9.
- Artifact logging/reproducibility: Tasks 3, 10.
- S01/S02 live validation milestone: Task 11.
- 3x stability and full regression: Task 12.
- Bakery human promotion: Task 13.
- Handoff acceptance gate: Task 14.

### Placeholder scan

The plan intentionally contains no TBD/TODO/“implement later” steps. The only conditional boundary is real provider configuration: Task 11 stops and requests only missing credentials if the environment does not contain them.

### Type consistency

Later tasks consume only interfaces introduced earlier: `RuntimeSettings`, typed contracts, `ArtifactStore`, `GoldenRepository`, provider interfaces, `ProductAnalyzer`, `StageARunner`, `CategoryTranslator`, `BArtDirector`, `compile_stage_b`, `BEvaluator`, `RetryPlanner`, `ValidationEngine`, and `StabilityReport`.
