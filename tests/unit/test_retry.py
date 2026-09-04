from pp_food_runtime.models.evaluation import EvaluationResult, FailureCode, FinalDecision, GoldenVector
from pp_food_runtime.stage_b.retry import RetryFamily, RetryLevel, RetryPlanner


def make_result(code, *, passing_dimensions=()):
    vector = GoldenVector.all_at(8).model_copy(
        update={dimension: 10 for dimension in passing_dimensions}
    )
    return EvaluationResult(
        candidate_id="primary",
        mechanical_pass=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        golden_vector=vector,
        critical_failures=[code],
        final_decision=FinalDecision.RETRY,
        confidence=0.9,
    )


def test_retry_maps_scene_dominance_to_hero_repair():
    plan = RetryPlanner().plan(make_result(FailureCode.SCENE_DOMINATES_PRODUCT), cycle=1)
    assert plan.family == RetryFamily.HERO_RETRY
    assert plan.level == RetryLevel.TARGETED_REPAIR


def test_retry_escalates_and_preserves_passing_dimensions():
    plan = RetryPlanner().plan(
        make_result(
            FailureCode.HEADLINE_WEAK,
            passing_dimensions=("information_density_control",),
        ),
        cycle=2,
    )
    assert plan.level == RetryLevel.CONCEPT_ADJUSTMENT
    assert "information_density_control" in plan.pass_freeze.passing_dimensions


def test_more_than_three_cycles_requires_human_review():
    plan = RetryPlanner().plan(make_result(FailureCode.GOLDEN_DISTANCE), cycle=4)
    assert plan.final_decision == FinalDecision.NEEDS_HUMAN_REVIEW
