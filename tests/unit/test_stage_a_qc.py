from pathlib import Path

import pytest
from PIL import Image

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.models.job import ImageRef, JobContract, JobMode
from pp_food_runtime.models.product import ProductTruth
from pp_food_runtime.providers.mock import MockImageProvider, MockVisionProvider
from pp_food_runtime.stage_a.evaluator import RawStageAEvaluation, StageAEvaluator, decide_stage_a_qc
from pp_food_runtime.stage_a.runner import StageAQCFailure, StageARunner


def _image_ref(path: Path, color: str) -> ImageRef:
    Image.new("RGB", (90, 160), color).save(path)
    return ImageRef(path=path, sha256=sha256_file(path), width=90, height=160)


def _raw(**updates) -> RawStageAEvaluation:
    values = {
        "product_identity_score": 9.6,
        "geometry_count_score": 9.6,
        "ingredient_topology_score": 9.6,
        "plating_arrangement_score": 9.6,
        "physical_relationships_score": 9.6,
        "surface_state_score": 9.6,
        "vessel_package_score": 9.9,
        "commercial_photography_score": 9.3,
        "semantic_relevance_score": 9.3,
        "hero_spatial_score": 9.3,
        "appetite_score": 9.3,
        "critical_drifts": [],
        "evidence": ["source and candidate retain the same visible product structure"],
        "confidence": 0.94,
    }
    values.update(updates)
    return RawStageAEvaluation(**values)


@pytest.mark.parametrize(
    ("dimension", "score"),
    [
        ("product_identity_score", 9.4),
        ("geometry_count_score", 9.4),
        ("ingredient_topology_score", 9.4),
        ("plating_arrangement_score", 9.4),
        ("physical_relationships_score", 9.4),
        ("surface_state_score", 9.4),
        ("vessel_package_score", 9.7),
        ("commercial_photography_score", 8.4),
        ("semantic_relevance_score", 8.4),
        ("hero_spatial_score", 8.4),
        ("appetite_score", 8.4),
    ],
)
def test_stage_a_qc_blocks_one_subfloor_dimension(dimension, score):
    result = decide_stage_a_qc(
        candidate_id="attempt-1",
        mechanical_pass=True,
        reference_binding_verified=True,
        raw=_raw(**{dimension: score}),
    )
    assert result.status == "RETRY"
    assert dimension in result.failed_dimensions


def test_stage_a_prompt_uses_exact_six_block_contract():
    truth = ProductTruth(
        source_sha256="a" * 64,
        identity_summary="five meat-filled flatbreads on one plate",
        primary_category="BBQ_NIGHTMARKET",
        pack_or_food="FOOD",
        visual_locks=["exactly five buns", "white plate with thin gold rim"],
    )

    prompt = StageARunner._compile_stage_a_prompt(truth)

    assert [line for line in prompt.splitlines() if line.startswith("## A")] == [
        "## A1 REFERENCE LOCK",
        "## A2 PRODUCT DNA + SURFACE STATE",
        "## A3 VESSEL / PACKAGE / DIRECT SUPPORT",
        "## A4 COMMERCIAL HERO PHOTOGRAPHY",
        "## A5 CURRENT CATEGORY BACKGROUND ARCHITECTURE",
        "## A6 HARD NEGATIVES",
    ]
    assert "remove source watermark" in prompt.lower()


def test_generated_stage_a_does_not_return_pass_when_visual_qc_fails(tmp_path):
    source = _image_ref(tmp_path / "source.png", "orange")
    fixture = _image_ref(tmp_path / "fixture.png", "yellow")
    job = JobContract(
        job_id="stage-a-fail",
        mode=JobMode.B,
        source_image=source,
        stage_a_mode="generate",
    )
    truth = ProductTruth(
        source_sha256=source.sha256,
        identity_summary="visible food product",
        primary_category="FOOD",
        pack_or_food="FOOD",
        visual_locks=["preserve exact ingredient topology"],
    )
    vision = MockVisionProvider(
        {RawStageAEvaluation: _raw(product_identity_score=7.0, critical_drifts=["identity changed"])}
    )
    runner = StageARunner(
        MockImageProvider(fixture.path),
        tmp_path / "artifacts",
        evaluator=StageAEvaluator(vision),
        max_attempts=2,
    )

    with pytest.raises(StageAQCFailure, match="failed visual QC") as exc:
        runner.run(job, source, truth)

    assert len(exc.value.evaluations) == 2
    assert all(result.status == "RETRY" for result in exc.value.evaluations)


def test_generated_stage_a_pass_records_visual_qc_evidence(tmp_path):
    source = _image_ref(tmp_path / "source.png", "orange")
    fixture = _image_ref(tmp_path / "fixture.png", "yellow")
    job = JobContract(
        job_id="stage-a-pass",
        mode=JobMode.B,
        source_image=source,
        stage_a_mode="generate",
    )
    truth = ProductTruth(
        source_sha256=source.sha256,
        identity_summary="visible food product",
        primary_category="FOOD",
        pack_or_food="FOOD",
        visual_locks=["preserve exact ingredient topology"],
    )
    vision = MockVisionProvider({RawStageAEvaluation: _raw()})
    runner = StageARunner(
        MockImageProvider(fixture.path),
        tmp_path / "artifacts",
        evaluator=StageAEvaluator(vision),
    )

    result = runner.run(job, source, truth)

    assert result.status == "PASS"
    assert result.qc is not None
    assert result.qc.status == "PASS"
    assert result.qc.evidence
