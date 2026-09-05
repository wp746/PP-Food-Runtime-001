from pp_food_runtime.models.evaluation import FailureCode, FinalDecision
from pp_food_runtime.stage_b.production_gate import decide_production_gate


def test_production_gate_passes_without_golden_floor_requirement():
    result = decide_production_gate(
        mechanical_pass=True,
        reference_binding_verified=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        product_first_hero=True,
        commercially_broken=False,
        raw_failure_codes=[],
        evidence=["product is first read and copy is legible"],
        confidence=0.9,
    )

    assert result.decision is FinalDecision.PASS
    assert result.retry_eligible is False
    assert result.failure_codes == []


def test_production_gate_blocks_product_truth_failure_and_allows_one_creative_repair():
    result = decide_production_gate(
        mechanical_pass=True,
        reference_binding_verified=True,
        product_truth_pass=False,
        copy_truth_pass=True,
        product_first_hero=True,
        commercially_broken=False,
        raw_failure_codes=[FailureCode.PRODUCT_IDENTITY_DRIFT.value],
        evidence=["filling geometry changed"],
        confidence=0.9,
    )

    assert result.decision is FinalDecision.RETRY
    assert FailureCode.PRODUCT_IDENTITY_DRIFT in result.failure_codes
    assert result.retry_eligible is True
    assert "PRODUCT_IDENTITY_DRIFT" in result.repair_instruction


def test_low_confidence_is_evaluator_failure_not_creative_retry():
    result = decide_production_gate(
        mechanical_pass=True,
        reference_binding_verified=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        product_first_hero=True,
        commercially_broken=False,
        raw_failure_codes=[],
        evidence=[],
        confidence=0.4,
    )

    assert result.decision is FinalDecision.NEEDS_SECOND_EVALUATION
    assert result.failure_codes == [FailureCode.EVALUATOR_FAILURE]
    assert result.retry_eligible is False
    assert result.failure_class == "EVALUATOR"


def test_soft_aesthetic_codes_do_not_block_production_delivery():
    result = decide_production_gate(
        mechanical_pass=True,
        reference_binding_verified=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        product_first_hero=True,
        commercially_broken=False,
        raw_failure_codes=[
            FailureCode.CATEGORY_CLICHE_DEPENDENCE.value,
            FailureCode.GOLDEN_DISTANCE.value,
            FailureCode.PHOTO_PLUS_TEXT.value,
        ],
        evidence=["style is conservative but usable"],
        confidence=0.9,
    )

    assert result.decision is FinalDecision.PASS
    assert result.failure_codes == []
