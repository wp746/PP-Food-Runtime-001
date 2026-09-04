import json

import pytest

from pp_food_runtime.models.job import JobState
from pp_food_runtime.providers.mock import MockImageProvider
from pp_food_runtime.providers.openai_compatible import ImageProviderTimeout
from pp_food_runtime.stage_b.evaluator import RawPairwiseComparison
from tests.engine_factory import make_engine_and_job


def test_b_runner_never_renders_before_stage_a_pass(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    result = engine.run(job)
    assert result.state_history.index(JobState.STAGE_A_PASS) < result.state_history.index(JobState.FINALIST_RENDER)


def test_b_runner_creates_exactly_primary_and_challenger_first(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    result = engine.run(job)
    assert set(result.candidates) == {"primary", "challenger"}


def test_b_runner_compares_both_actual_renders_in_one_pairwise_audition(tmp_path):
    engine, job = make_engine_and_job(tmp_path)

    result = engine.run(job)

    assert result.pairwise_comparison.actual_images_compared is True
    assert result.pairwise_comparison.candidate_ids == ["primary", "challenger"]
    assert result.pairwise_comparison.winner_id in result.candidates


def test_image_provider_timeout_stops_b_without_creative_retry(tmp_path):
    engine, job = make_engine_and_job(tmp_path)

    class TimeoutImageProvider(MockImageProvider):
        def generate(self, reference_images, prompt, aspect_ratio, output_path):
            raise ImageProviderTimeout("IMAGE_PROVIDER_TIMEOUT")

    engine.runner.image_provider = TimeoutImageProvider(tmp_path / "unused.png")

    with pytest.raises(ImageProviderTimeout, match="IMAGE_PROVIDER_TIMEOUT"):
        engine.run(job)

    artifact_dir = engine.runner.store.job_dir(job.job_id)
    metadata = json.loads(
        (artifact_dir / "primary" / "generation.json").read_text(encoding="utf-8")
    )
    assert metadata["status"] == "TIMEOUT"
    assert metadata["failure_code"] == "IMAGE_PROVIDER_TIMEOUT"
    assert not (artifact_dir / "challenger" / "generation.json").exists()
    assert not (artifact_dir / "retry").exists()


def test_pairwise_provider_candidate_alias_maps_to_business_id(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    engine.runner.evaluator.provider.responses[RawPairwiseComparison]["winner_id"] = "candidate_2"

    result = engine.run(job)

    assert result.pairwise_comparison.winner_id == "challenger"
    pairwise_call = next(
        call
        for call in engine.runner.evaluator.provider.calls
        if call["response_model"] is RawPairwiseComparison
    )
    assert '"image_1": "STAGE_A_CONTROL_ONLY"' in pairwise_call["instruction"]
    assert '"image_2": "primary"' in pairwise_call["instruction"]
    assert '"image_3": "challenger"' in pairwise_call["instruction"]
    assert len(pairwise_call["images"]) == 3
