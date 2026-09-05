import json

from pp_food_runtime.config import RuntimeMode
from pp_food_runtime.models.evaluation import FinalDecision
from pp_food_runtime.stage_b.evaluator import RawEvaluation, RawPairwiseComparison
from tests.engine_factory import make_engine_and_job


def _set_mode(engine, mode: RuntimeMode):
    engine.runner.settings = engine.runner.settings.model_copy(update={"runtime_mode": mode})


def test_production_fast_generates_one_initial_b_candidate_and_skips_pairwise(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    _set_mode(engine, RuntimeMode.PRODUCTION_FAST)

    result = engine.run(job)

    assert result.final_decision is FinalDecision.PASS
    assert set(result.candidates) == {"primary"}
    assert result.pairwise_comparison is None
    assert result.production_gate is not None
    assert result.production_gate.decision is FinalDecision.PASS
    assert len(engine.runner.image_provider.calls) == 1
    assert not any(
        call["response_model"] is RawPairwiseComparison
        for call in engine.runner.evaluator.provider.calls
    )


def test_validation_keeps_two_finalists_and_pairwise(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    _set_mode(engine, RuntimeMode.VALIDATION)

    result = engine.run(job)

    assert set(result.candidates) == {"primary", "challenger"}
    assert result.pairwise_comparison is not None
    assert len(engine.runner.image_provider.calls) == 2
    assert any(
        call["response_model"] is RawPairwiseComparison
        for call in engine.runner.evaluator.provider.calls
    )


def test_production_fast_uses_at_most_one_targeted_creative_retry(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    _set_mode(engine, RuntimeMode.PRODUCTION_FAST)
    engine.runner.evaluator.provider.responses[RawEvaluation]["product_truth_pass"] = False
    engine.runner.evaluator.provider.responses[RawEvaluation]["critical_failures"] = [
        "PRODUCT_IDENTITY_DRIFT"
    ]

    result = engine.run(job)

    assert len(engine.runner.image_provider.calls) == 2
    assert set(result.candidates) == {"primary", "retry-1"}
    assert len(result.retry_history) == 1
    assert result.final_decision is not FinalDecision.PASS
    assert result.pairwise_comparison is None


def test_production_fast_records_runtime_mode_hashes_and_step_timing(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    _set_mode(engine, RuntimeMode.PRODUCTION_FAST)

    result = engine.run(job)
    timing_path = result.artifact_dir / "final" / "timing.json"
    manifest_path = result.artifact_dir / "manifest.json"

    timing = json.loads(timing_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert timing["product_analysis_seconds"] >= 0
    assert timing["stage_a_total_seconds"] >= 0
    assert timing["b_generation_primary_seconds"] >= 0
    assert timing["production_gate_primary_seconds"] >= 0
    assert manifest["runtime_mode"] == "PRODUCTION_FAST"
    assert manifest["runtime_version"] == "1.0.0-rc.2"
    assert manifest["source_sha256"] == job.source_image.sha256
    assert manifest["stage_a_sha256"] == job.stage_a_pass.sha256
