from __future__ import annotations

import os
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class RuntimeMode(StrEnum):
    VALIDATION = "VALIDATION"
    PRODUCTION_FAST = "PRODUCTION_FAST"


class RuntimeSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    runtime_version: str = "1.0.0-rc.3"
    runtime_mode: RuntimeMode = RuntimeMode.VALIDATION
    artifact_root: Path = Path("artifacts")
    golden_root: Path = Path("goldens")
    vision_base_url: str = ""
    vision_model: str = ""
    vision_api_key: SecretStr = SecretStr("")
    image_base_url: str = ""
    image_model: str = ""
    image_api_key: SecretStr = SecretStr("")
    request_timeout_seconds: int = Field(default=120, ge=10, le=1800)
    production_max_creative_retries: int = Field(default=1, ge=0, le=1)
    validation_max_creative_cycles: int = Field(default=3, ge=1, le=3)
    real_provider_enabled: bool = False

    @classmethod
    def from_env(cls) -> "RuntimeSettings":
        raw_mode = os.getenv("PP_RUNTIME_MODE", RuntimeMode.VALIDATION.value)
        try:
            runtime_mode = RuntimeMode(raw_mode)
        except ValueError as exc:
            raise ValueError(f"invalid PP_RUNTIME_MODE: {raw_mode}") from exc

        values = {
            "runtime_version": os.getenv("PP_RUNTIME_VERSION", "1.0.0-rc.3"),
            "runtime_mode": runtime_mode,
            "artifact_root": Path(os.getenv("PP_ARTIFACT_ROOT", "artifacts")),
            "golden_root": Path(os.getenv("PP_GOLDEN_ROOT", "goldens")),
            "vision_base_url": os.getenv("PP_VISION_BASE_URL", ""),
            "vision_model": os.getenv("PP_VISION_MODEL", ""),
            "vision_api_key": SecretStr(os.getenv("PP_VISION_API_KEY", "")),
            "image_base_url": os.getenv("PP_IMAGE_BASE_URL", ""),
            "image_model": os.getenv("PP_IMAGE_MODEL", ""),
            "image_api_key": SecretStr(os.getenv("PP_IMAGE_API_KEY", "")),
            "request_timeout_seconds": int(os.getenv("PP_REQUEST_TIMEOUT_SECONDS", "120")),
            "production_max_creative_retries": int(
                os.getenv("PP_PRODUCTION_MAX_CREATIVE_RETRIES", "1")
            ),
            "validation_max_creative_cycles": int(
                os.getenv("PP_VALIDATION_MAX_CREATIVE_CYCLES", "3")
            ),
        }
        values["real_provider_enabled"] = all(
            [
                values["vision_base_url"],
                values["vision_model"],
                values["vision_api_key"].get_secret_value(),
                values["image_base_url"],
                values["image_model"],
                values["image_api_key"].get_secret_value(),
            ]
        )
        return cls(**values)

    def safe_provider_summary(self) -> dict[str, object]:
        return {
            "runtime_version": self.runtime_version,
            "runtime_mode": self.runtime_mode.value,
            "vision": {
                "base_url": self.vision_base_url,
                "model": self.vision_model,
                "credentials_present": bool(self.vision_api_key.get_secret_value()),
            },
            "image": {
                "base_url": self.image_base_url,
                "model": self.image_model,
                "credentials_present": bool(self.image_api_key.get_secret_value()),
            },
        }
