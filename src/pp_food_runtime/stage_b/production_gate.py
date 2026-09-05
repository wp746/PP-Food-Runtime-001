from __future__ import annotations

from pydantic import Field

from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.evaluation import FailureCode, FinalDecision


class ProductionGateResult(FrozenModel):
    decision: FinalDecision
    failure_codes: list[FailureCode] = Field(default_factory=list)
    retry_eligible: bool = False
    failure_class: str = "NONE"
    evidence: list[str] = Field(default_factory=list)
    repair_instruction: str = ""


_HARD_RAW_FAILURES = {
    FailureCode.PRODUCT_IDENTITY_DRIFT,
    FailureCode.COPY_TRUTH_FAILURE,
    FailureCode.MECHANICAL_FAILURE,
    FailureCode.REFERENCE_BINDING_FAILURE,
    FailureCode.HERO_WEAK,
    FailureCode.SCENE_DOMINATES_PRODUCT,
    FailureCode.COMMERCIAL_FINISH_WEAK,
}


def _parse_failure_codes(values: list[str]) -> list[FailureCode]:
    parsed: list[FailureCode] = []
    for value in values:
        try:
            code = FailureCode(value)
        except ValueError:
            continue
        if code in _HARD_RAW_FAILURES and code not in parsed:
            parsed.append(code)
    return parsed


def decide_production_gate(
    *,
    mechanical_pass: bool,
    reference_binding_verified: bool,
    product_truth_pass: bool,
    copy_truth_pass: bool,
    product_first_hero: bool,
    commercially_broken: bool,
    raw_failure_codes: list[str],
    evidence: list[str],
    confidence: float,
) -> ProductionGateResult:
    """Apply the Production Fast delivery gate.

    Golden-relative style disagreements are deliberately excluded here. This gate
    blocks only a broken deliverable or product/copy/reference truth failure.
    """
    if confidence < 0.65:
        return ProductionGateResult(
            decision=FinalDecision.NEEDS_SECOND_EVALUATION,
            failure_codes=[FailureCode.EVALUATOR_FAILURE],
            retry_eligible=False,
            failure_class="EVALUATOR",
            evidence=evidence,
            repair_instruction="Re-run evaluation only; do not regenerate the image.",
        )

    failures = _parse_failure_codes(raw_failure_codes)
    if not mechanical_pass and FailureCode.MECHANICAL_FAILURE not in failures:
        failures.append(FailureCode.MECHANICAL_FAILURE)
    if not reference_binding_verified and FailureCode.REFERENCE_BINDING_FAILURE not in failures:
        failures.append(FailureCode.REFERENCE_BINDING_FAILURE)
    if not product_truth_pass and FailureCode.PRODUCT_IDENTITY_DRIFT not in failures:
        failures.append(FailureCode.PRODUCT_IDENTITY_DRIFT)
    if not copy_truth_pass and FailureCode.COPY_TRUTH_FAILURE not in failures:
        failures.append(FailureCode.COPY_TRUTH_FAILURE)
    if not product_first_hero and FailureCode.HERO_WEAK not in failures:
        failures.append(FailureCode.HERO_WEAK)
    if commercially_broken and FailureCode.COMMERCIAL_FINISH_WEAK not in failures:
        failures.append(FailureCode.COMMERCIAL_FINISH_WEAK)

    if failures:
        codes = ", ".join(code.value for code in failures)
        return ProductionGateResult(
            decision=FinalDecision.RETRY,
            failure_codes=failures,
            retry_eligible=True,
            failure_class="DELIVERY_HARD_GATE",
            evidence=evidence,
            repair_instruction=(
                f"Repair only these delivery-blocking failures: {codes}. "
                "Preserve current Stage A reference, product truth, passing visual dimensions, and authorized copy."
            ),
        )

    return ProductionGateResult(
        decision=FinalDecision.PASS,
        failure_codes=[],
        retry_eligible=False,
        failure_class="NONE",
        evidence=evidence,
    )
