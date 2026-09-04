from pp_food_runtime.models.job import JobState
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
        "challenger/image.png",
        "eval/primary.json",
        "eval/challenger.json",
        "final/decision.json",
        "final/winner.png",
        "manifest.json",
    }
    assert required.issubset(relative_files)
