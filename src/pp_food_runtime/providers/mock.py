from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import Any

from PIL import Image
from pydantic import BaseModel

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.models.job import ImageRef

from .base import ImageProvider, ProviderCapabilityProfile, ResponseT, VisionProvider


MOCK_PROFILE = ProviderCapabilityProfile(
    provider_id="mock",
    model_id="deterministic-mock",
    reference_edit=True,
    multiple_references=True,
    masks=False,
    seed=True,
    text_rendering="strong",
    aspect_ratio=["9:16"],
    max_resolution="936x1664",
)


class MockVisionProvider(VisionProvider):
    capability_profile = MOCK_PROFILE

    def __init__(self, responses: dict[type[BaseModel], BaseModel | dict[str, Any]] | None = None):
        self.responses = responses or {}
        self.calls: list[dict[str, Any]] = []

    def analyze(self, images, instruction: str, response_model: type[ResponseT]) -> ResponseT:
        self.calls.append({"images": images, "instruction": instruction, "response_model": response_model})
        value = self.responses.get(response_model)
        if value is None:
            raise KeyError(f"no mock response for {response_model.__name__}")
        if isinstance(value, response_model):
            return value
        return response_model.model_validate(value)


class MockImageProvider(ImageProvider):
    capability_profile = MOCK_PROFILE

    def __init__(self, fixture_image: Path):
        self.fixture_image = Path(fixture_image)
        self.calls: list[dict[str, Any]] = []

    def generate(self, reference_images, prompt: str, aspect_ratio: str, output_path: Path) -> ImageRef:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        bound = bool(reference_images)
        self.calls.append(
            {
                "reference_images": [str(item.path if isinstance(item, ImageRef) else item) for item in reference_images],
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
            }
        )
        if self.fixture_image.is_file():
            shutil.copy2(self.fixture_image, output_path)
            digest = sha256_file(output_path)
            with Image.open(output_path) as image:
                width, height = image.size
        else:
            digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            width = height = None
        return ImageRef(
            path=output_path.resolve(),
            sha256=digest,
            width=width,
            height=height,
            reference_binding_verified=bound,
            provider_request_id="mock-request",
        )

