import json

from pp_food_runtime.models.job import JobState
from pp_food_runtime.artifacts.store import sha256_file
from tests.engine_factory import make_engine_and_job


def test_mock_vertical_slice_persists_complete_evidence(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    result = engine.run(job)

    assert result.final_state == JobState.B_PASS
    assert result.winner_id in {"primary", "challenger"}
    assert result.final_image is not None
    relative_files = {
        str(path.relative_to(result.artifact_dir)) for path in result.artifact_dir.rglob("*") if path.is_file()
    }
    required = {
        "contracts/job.json",
        "input/source.png",
        "input/stage-a.png",
        "contracts/product_truth.json",
        "contracts/visual_translation.json",
        "contracts/golden_retrieval.json",
        "prompts/primary.json",
        "prompts/challenger.json",
        "primary/image.png",
        "primary/generation.json",
        "challenger/image.png",
        "challenger/generation.json",
        "eval/primary.json",
        "eval/challenger.json",
        "final/decision.json",
        "final/winner.png",
        "manifest.json",
    }
    assert required.issubset(relative_files)
    assert list(result.candidates) == ["primary", "challenger"]
    for candidate_id in ("primary", "challenger"):
        metadata = json.loads(
            (result.artifact_dir / candidate_id / "generation.json").read_text(encoding="utf-8")
        )
        assert metadata["status"] == "PASS"
        assert metadata["stage_a_reference_sha256"] == job.stage_a_pass.sha256
        assert metadata["compiled_prompt_sha256"] == result.prompt_hashes[candidate_id]
        assert metadata["provider"] == "mock"
        assert metadata["model"] == "deterministic-mock"
        assert metadata["request_id"] == "mock-request"
        assert metadata["started_at"].endswith("Z")
        assert metadata["ended_at"].endswith("Z")
        assert metadata["latency_seconds"] >= 0
        assert metadata["output_sha256"] == sha256_file(result.candidates[candidate_id].path)
