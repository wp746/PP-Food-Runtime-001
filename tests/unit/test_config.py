from pp_food_runtime.config import RuntimeMode, RuntimeSettings


def test_settings_defaults_are_local_and_safe(monkeypatch, tmp_path):
    for key in (
        "PP_VISION_BASE_URL",
        "PP_VISION_API_KEY",
        "PP_VISION_MODEL",
        "PP_IMAGE_BASE_URL",
        "PP_IMAGE_API_KEY",
        "PP_IMAGE_MODEL",
        "PP_RUNTIME_MODE",
    ):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("PP_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    monkeypatch.setenv("PP_GOLDEN_ROOT", str(tmp_path / "goldens"))

    settings = RuntimeSettings.from_env()

    assert settings.real_provider_enabled is False
    assert settings.request_timeout_seconds == 120
    assert settings.runtime_version == "1.0.0-rc.1"
    assert settings.runtime_mode is RuntimeMode.VALIDATION
    assert settings.production_max_creative_retries == 1
    assert settings.validation_max_creative_cycles == 3


def test_runtime_mode_can_be_selected_from_env(monkeypatch):
    monkeypatch.setenv("PP_RUNTIME_MODE", "PRODUCTION_FAST")

    settings = RuntimeSettings.from_env()

    assert settings.runtime_mode is RuntimeMode.PRODUCTION_FAST


def test_invalid_runtime_mode_fails_closed(monkeypatch):
    monkeypatch.setenv("PP_RUNTIME_MODE", "FASTEST")

    try:
        RuntimeSettings.from_env()
    except ValueError as exc:
        assert "FASTEST" in str(exc)
    else:
        raise AssertionError("invalid runtime mode must fail closed")


def test_real_provider_requires_complete_credentials(monkeypatch):
    monkeypatch.setenv("PP_VISION_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("PP_VISION_MODEL", "vision-model")
    monkeypatch.setenv("PP_VISION_API_KEY", "secret")
    monkeypatch.setenv("PP_IMAGE_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("PP_IMAGE_MODEL", "image-model")
    monkeypatch.setenv("PP_IMAGE_API_KEY", "secret")

    settings = RuntimeSettings.from_env()

    assert settings.real_provider_enabled is True
