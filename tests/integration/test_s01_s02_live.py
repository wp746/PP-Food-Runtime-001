import os
from pathlib import Path

import pytest

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.golden.repository import GoldenRepository


EXPECTED = {
    "S01": {
        "source": "039d597cce391d696b608e772c213440210e43804b8a5dede83dcef0453b4543",
        "stage_a": "3b5bf2c44673bd7e4af300532e11e395e96947a246b6a458dba684a38426258e",
        "golden": "22fd444fb390c2f7a3fdc83da193b13d3ab858cfa48ec5a0213a99a5e43c5837",
    },
    "S02": {
        "source": "2dfa9170e778866b6675452581396beb43f55fb85294228bc408bb996ab5da3f",
        "stage_a": "2a67c852cf179ce1a797721409e3d81f956bf97f017ecf71e34942002df0d142",
        "golden": "041af8ec16bea960f79babfe479298deed2bba8caa28e132d862d5ad4cb6926f",
    },
}


@pytest.mark.integration
@pytest.mark.parametrize("case", ["S01", "S02"])
def test_private_live_assets_are_exact_and_bindable(case):
    if os.getenv("PP_RUN_S01_S02_LIVE_TEST") != "1":
        pytest.skip("private S01/S02 live validation is opt-in")
    root = Path.cwd()
    source = root / "validation_inputs" / f"{case}-source.jpg"
    stage_a = root / "validation_inputs" / f"{case}-stage-a.png"
    golden = root / "goldens" / "assets" / f"{case}.png"
    assert sha256_file(source) == EXPECTED[case]["source"]
    assert sha256_file(stage_a) == EXPECTED[case]["stage_a"]
    assert sha256_file(golden) == EXPECTED[case]["golden"]
    repository = GoldenRepository(root / "goldens" / "manifests", root / "goldens" / "assets")
    assert repository.bind_local_asset(case, golden).local_asset_sha256 == EXPECTED[case]["golden"]
