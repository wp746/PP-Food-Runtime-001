from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.job import ImageRef


ResponseT = TypeVar("ResponseT", bound=BaseModel)


class ProviderCapabilityProfile(FrozenModel):
    provider_id: str
    model_id: str
    reference_edit: bool
    multiple_references: bool
    masks: bool
    seed: bool
    text_rendering: str
    aspect_ratio: list[str]
    max_resolution: str


class VisionProvider(ABC):
    capability_profile: ProviderCapabilityProfile

    @abstractmethod
    def analyze(
        self,
        images: list[Path | ImageRef],
        instruction: str,
        response_model: type[ResponseT],
    ) -> ResponseT:
        raise NotImplementedError


class ImageProvider(ABC):
    capability_profile: ProviderCapabilityProfile

    @abstractmethod
    def generate(
        self,
        reference_images: list[Path | ImageRef],
        prompt: str,
        aspect_ratio: str,
        output_path: Path,
    ) -> ImageRef:
        raise NotImplementedError

