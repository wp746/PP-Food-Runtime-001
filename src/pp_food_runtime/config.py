from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class RuntimeSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    runtime_version: str = "validation-v0.1.0"
    artifact_root: Path = Path("artifacts")
    golden_root: Path = Path("goldens")
    vision_base_url: str = ""
    vision_model: str = ""
    vision_api_key: SecretStr = SecretStr("")
    image_base_url: str = ""
    image_model: str = ""
    image_api_key: SecretStr = SecretStr("")
    request_timeout_seconds: int = Field(default=120, ge=10, le=1800)
    real_provider_enabled: bool = False

    @classmethod
    def from_env(cls) -> "RuntimeSettings":
        values = {
            "runtime_version": os.getenv("PP_RUNTIME_VERSION", "validation-v0.1.0"),
            "artifact_root": Path(os.getenv("PP_ARTIFACT_ROOT", "artifacts")),
            "golden_root": Path(os.getenv("PP_GOLDEN_ROOT", "goldens")),
            "vision_base_url": os.getenv("PP_VISION_BASE_URL", ""),
            "vision_model": os.getenv("PP_VISION_MODEL", ""),
            "vision_api_key": SecretStr(os.getenv("PP_VISION_API_KEY", "")),
            "image_base_url": os.getenv("PP_IMAGE_BASE_URL", ""),
            "image_model": os.getenv("PP_IMAGE_MODEL", ""),
            "image_api_key": SecretStr(os.getenv("PP_IMAGE_API_KEY", "")),
            "request_timeout_seconds": int(os.getenv("PP_REQUEST_TIMEOUT_SECONDS", "120")),
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
