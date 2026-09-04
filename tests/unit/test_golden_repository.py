from pathlib import Path

import pytest

from pp_food_runtime.golden.repository import GoldenAssetHashMismatch, GoldenRepository


def test_initial_manifests_have_two_s_tier_and_no_bakery_canonical(tmp_path):
    repo = GoldenRepository(Path("goldens/manifests"), tmp_path)
    manifests = repo.load_all()
    assert {m.golden_id for m in manifests if m.tier.value == "S_TIER"} == {"S01", "S02"}
    assert all(m.primary_category != "BAKERY" for m in manifests)


def test_street_food_human_accepted_canonical_is_loadable_without_private_asset(tmp_path):
    repo = GoldenRepository(Path("goldens/manifests"), tmp_path)
    manifests = {item.golden_id: item for item in repo.load_all()}

    canonical = manifests["C01_STREET_FOOD"]
    assert canonical.tier.value == "CANONICAL"
    assert canonical.human_accepted is True
    assert canonical.calibration_role == "HUMAN_ACCEPTED_CATEGORY_CANONICAL"
    assert canonical.sha256 == "LOCAL_BIND_REQUIRED"
    assert canonical.local_asset_path is None
    assert "strong product-first hero" in canonical.transferable_principles
    assert "exact old brand/copy/layout" in canonical.prohibited_transfer


def test_bind_local_asset_rejects_wrong_hash(tmp_path):
    repo = GoldenRepository(Path("goldens/manifests"), tmp_path)
    bad = tmp_path / "bad.png"
    bad.write_bytes(b"wrong")
    with pytest.raises(GoldenAssetHashMismatch):
        repo.bind_local_asset("S01", bad)


def test_retrieval_is_deterministic_and_de_skinned(tmp_path):
    repo = GoldenRepository(Path("goldens/manifests"), tmp_path)
    first = repo.retriever().retrieve(
        {"primary_category": "COLD_DRINK_FRUIT_DESSERT", "pack_or_food": "FOOD", "sensory_tags": ["cool", "fruit"]},
        limit=2,
    )
    second = repo.retriever().retrieve(
        {"primary_category": "COLD_DRINK_FRUIT_DESSERT", "pack_or_food": "FOOD", "sensory_tags": ["cool", "fruit"]},
        limit=2,
    )
    assert first == second
    assert first[0].golden_id == "S01"
    assert all(pack.local_asset_path is None for pack in first)
