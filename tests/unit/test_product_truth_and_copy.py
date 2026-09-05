from pathlib import Path

import pytest
from PIL import Image

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.models.job import ImageRef, JobContract, JobMode, UserFacts
from pp_food_runtime.models.product import EvidenceValue, ProductTruth
from pp_food_runtime.providers.mock import MockImageProvider
from pp_food_runtime.stage_a.runner import StageARunner
from pp_food_runtime.stage_b.copy_firewall import CopyFirewall


def _image_ref(path: Path, color: str) -> ImageRef:
    Image.new("RGB", (90, 160), color).save(path)
    return ImageRef(path=path, sha256=sha256_file(path), width=90, height=160)


def test_default_copy_does_not_invent_hard_facts():
    allowlist = CopyFirewall().build(
        UserFacts(
            product_name="阳光蜜橘罐头",
            brand="测试品牌",
            default_copy_authorized=True,
        )
    )
    assert allowlist.product_name == "阳光蜜橘罐头"
    assert allowlist.price is None
    assert allowlist.address is None
    assert allowlist.phone is None


def test_product_truth_separates_observed_inferred_and_unknown():
    truth = ProductTruth(
        source_sha256="a" * 64,
        identity_summary="sealed citrus can with orange label",
        primary_category="CANNED_FRUIT_RETAIL",
        pack_or_food="PACK",
        observed={"package": EvidenceValue(value="metal can", confidence=0.99, visible_evidence="center")},
        high_confidence_inferred={"taste": EvidenceValue(value="sweet citrus", confidence=0.8, visible_evidence="fruit imagery")},
        unknown=["net weight"],
    )
    assert "package" in truth.observed
    assert "taste" in truth.high_confidence_inferred
    assert truth.unknown == ["net weight"]


def test_provided_stage_a_bridge_records_exact_source_hash(tmp_path):
    source = _image_ref(tmp_path / "source.png", "orange")
    stage_a = _image_ref(tmp_path / "stage-a.png", "yellow")
    job = JobContract(
        mode=JobMode.B,
        source_image=source,
        stage_a_pass=stage_a,
        user_facts=UserFacts(product_name="桔子罐头"),
    )
    truth = ProductTruth(
        source_sha256=source.sha256,
        identity_summary="orange can",
        primary_category="CANNED_FRUIT_RETAIL",
        pack_or_food="PACK",
        visual_locks=["can silhouette", "orange label"],
    )
    runner = StageARunner(MockImageProvider(tmp_path / "unused.png"), tmp_path / "artifacts")
    result = runner.run(job, source, truth)
    assert result.status == "PASS"
    assert result.source_sha256 == source.sha256
    assert result.bridge.stage_a.sha256 == stage_a.sha256


def test_provided_stage_a_rejects_tampered_file(tmp_path):
    source = _image_ref(tmp_path / "source.png", "orange")
    stage_a = _image_ref(tmp_path / "stage-a.png", "yellow")
    stage_a.path.write_bytes(b"tampered")
    job = JobContract(mode=JobMode.B, source_image=source, stage_a_pass=stage_a)
    truth = ProductTruth(
        source_sha256=source.sha256,
        identity_summary="product",
        primary_category="OTHER",
        pack_or_food="FOOD",
    )
    with pytest.raises(ValueError, match="hash"):
        StageARunner(MockImageProvider(tmp_path / "unused.png"), tmp_path / "artifacts").run(job, source, truth)
