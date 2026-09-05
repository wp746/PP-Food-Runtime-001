from pp_food_runtime.models.evaluation import (
    EvaluationResult,
    FailureCode,
    FinalDecision,
    GoldenVector,
)
from pp_food_runtime.stage_b.evaluator import decide_evaluation
from tests.engine_factory import make_engine_and_job


def test_hard_product_failure_cannot_be_compensated():
    result = decide_evaluation(
        candidate_id="primary",
        mechanical_pass=True,
        product_truth_pass=False,
        copy_truth_pass=True,
        golden_vector=GoldenVector.all_at(10),
        critical_failures=[FailureCode.PRODUCT_IDENTITY_DRIFT],
        materially_weaker_core_dimensions=[],
        evidence=[],
        confidence=0.9,
    )
    assert result.final_decision != FinalDecision.PASS


def test_pairwise_winner_can_still_be_unqualified():
    result = decide_evaluation(
        candidate_id="primary",
        mechanical_pass=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        golden_vector=GoldenVector.all_at(8.1),
        critical_failures=[],
        materially_weaker_core_dimensions=["product_hero_strength"],
        evidence=[],
        confidence=0.9,
        pairwise_winner="primary",
    )
    assert result.final_decision == FinalDecision.RETRY


def test_two_materially_weaker_core_dimensions_force_retry():
    result = decide_evaluation(
        candidate_id="candidate",
        mechanical_pass=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        golden_vector=GoldenVector.all_at(9.5),
        critical_failures=[],
        materially_weaker_core_dimensions=["headline_aggression", "commercial_finish"],
        evidence=[],
        confidence=0.9,
    )
    assert result.final_decision == FinalDecision.RETRY


def test_current_upper_bound_product_and_category_floors_are_fail_closed():
    vector = GoldenVector.all_at(9.5).model_copy(
        update={"product_hero_strength": 9.1, "category_inevitability": 8.9}
    )
    evidence = [
        {
            "dimension": field,
            "what_is_visible": "visible execution",
            "where_visible": "poster",
            "why_it_helps_or_hurts": "supports assessment",
        }
        for field in GoldenVector.model_fields
    ]

    result = decide_evaluation(
        candidate_id="candidate",
        mechanical_pass=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        golden_vector=vector,
        critical_failures=[],
        materially_weaker_core_dimensions=[],
        evidence=evidence,
        confidence=0.9,
    )

    assert result.final_decision == FinalDecision.RETRY


def test_evidence_insufficient_scores_are_capped():
    result = decide_evaluation(
        candidate_id="candidate",
        mechanical_pass=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        golden_vector=GoldenVector.all_at(10),
        critical_failures=[],
        materially_weaker_core_dimensions=[],
        evidence=[],
        confidence=0.9,
    )
    assert max(result.golden_vector.model_dump().values()) == 7.5


def test_low_confidence_requests_second_evaluation():
    result = decide_evaluation(
        candidate_id="candidate",
        mechanical_pass=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        golden_vector=GoldenVector.all_at(9),
        critical_failures=[],
        materially_weaker_core_dimensions=[],
        evidence=[],
        confidence=0.64,
    )
    assert result.final_decision == FinalDecision.NEEDS_SECOND_EVALUATION


def test_context_has_no_generator_reasoning_field():
    from pp_food_runtime.stage_b.evaluator import EvaluationContext

    assert "generator_reasoning" not in EvaluationContext.model_fields
    assert "generator_self_score" not in EvaluationContext.model_fields


def test_pairwise_uses_stage_a_and_two_candidates_only(tmp_path):
    engine, job = make_engine_and_job(tmp_path)

    engine.run(job)

    pairwise_calls = [
        call
        for call in engine.runner.evaluator.provider.calls
        if call["response_model"].__name__ == "RawPairwiseComparison"
    ]
    assert len(pairwise_calls) == 1
    images = pairwise_calls[0]["images"]
    assert len(images) == 3
    assert "stage-a" in str(images[0].path)
    assert "primary" in str(images[1].path)
    assert "challenger" in str(images[2].path)
