from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import Field, field_validator

from pp_food_runtime.models.common import FrozenModel


class GoldenTier(StrEnum):
    S_TIER = "S_TIER"
    CANONICAL = "CANONICAL"


class GoldenManifest(FrozenModel):
    golden_id: str
    tier: GoldenTier
    name: str
    primary_category: str
    pack_or_food: str
    sensory_tags: list[str] = Field(default_factory=list)
    visual_problems: list[str] = Field(default_factory=list)
    asset_filename: str
    sha256: str
    transferable_principles: list[str] = Field(min_length=1)
    prohibited_transfer: list[str] = Field(min_length=1)
    human_accepted: bool = False
    calibration_role: str | None = None
    local_asset_path: Path | None = None
    local_asset_sha256: str | None = None

    @field_validator("sha256")
    @classmethod
    def validate_digest(cls, value: str) -> str:
        if value != "LOCAL_BIND_REQUIRED" and (
            len(value) != 64 or any(c not in "0123456789abcdef" for c in value)
        ):
            raise ValueError("sha256 must be a lowercase digest or LOCAL_BIND_REQUIRED")
        return value

    @property
    def tier_rank(self) -> int:
        return 0 if self.tier is GoldenTier.S_TIER else 1
