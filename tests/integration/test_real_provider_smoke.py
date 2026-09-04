import os

import pytest

from pp_food_runtime.config import RuntimeSettings


@pytest.mark.integration
def test_real_provider_smoke_is_explicitly_opt_in():
    settings = RuntimeSettings.from_env()
    if not settings.real_provider_enabled or os.getenv("PP_RUN_LIVE_PROVIDER_TESTS") != "1":
        pytest.skip("real provider smoke is opt-in and requires complete credentials")
    assert settings.vision_model
    assert settings.image_model
