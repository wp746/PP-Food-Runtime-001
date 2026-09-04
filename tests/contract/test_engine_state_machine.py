from pp_food_runtime.models.job import JobState
from tests.engine_factory import make_engine_and_job


def test_b_runner_never_renders_before_stage_a_pass(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    result = engine.run(job)
    assert result.state_history.index(JobState.STAGE_A_PASS) < result.state_history.index(JobState.FINALIST_RENDER)


def test_b_runner_creates_exactly_primary_and_challenger_first(tmp_path):
    engine, job = make_engine_and_job(tmp_path)
    result = engine.run(job)
    assert set(result.candidates) == {"primary", "challenger"}
