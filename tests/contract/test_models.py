from pathlib import Path

import pytest
from pydantic import ValidationError

from pp_food_runtime.models.evaluation import EvaluationResult, FinalDecision, GoldenVector
from pp_food_runtime.models.job import ImageRef, JobContract, JobMode, UserFacts
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


def test_image_ref_requires_a_sha256_digest():
    with pytest.raises(ValidationError):
        ImageRef(path=Path("source.png"), sha256="short")


def test_golden_vector_scores_are_bounded():
    with pytest.raises(ValidationError):
        GoldenVector(
            product_hero_strength=11,
            headline_aggression=9,
            typography_product_symbiosis=9,
            one_big_idea_clarity=9,
            compositional_depth_tension=9,
            category_inevitability=9,
            information_density_control=9,
            commercial_finish=9,
        )


def test_hard_failure_cannot_be_pass():
    with pytest.raises(ValidationError):
        EvaluationResult(
            candidate_id="primary",
            product_truth_pass=False,
            copy_truth_pass=True,
            mechanical_pass=True,
            golden_vector=GoldenVector.all_at(9.0),
            critical_failures=["PRODUCT_IDENTITY_DRIFT"],
            final_decision=FinalDecision.PASS,
            confidence=0.9,
        )
