from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from uuid import uuid4

from pydantic import Field, model_validator

from .common import FrozenModel


class JobMode(StrEnum):
    A = "A"
    B = "B"


class JobState(StrEnum):
    B_REQUESTED = "B_REQUESTED"
    B_ENTRY_VALIDATION = "B_ENTRY_VALIDATION"
    STAGE_A_REQUIRED = "STAGE_A_REQUIRED"
    STAGE_A_PASS = "STAGE_A_PASS"
    PRODUCT_LOCK_BRIDGE_READY = "PRODUCT_LOCK_BRIDGE_READY"
    COPY_FIREWALL_READY = "COPY_FIREWALL_READY"
    CURRENT_PRODUCT_ANALYSIS = "CURRENT_PRODUCT_ANALYSIS"
    CATEGORY_VISUAL_TRANSLATION = "CATEGORY_VISUAL_TRANSLATION"
    GOLDEN_RETRIEVAL = "GOLDEN_RETRIEVAL"
    ART_DIRECTION = "ART_DIRECTION"
    ART_DIRECTION_VALIDATION = "ART_DIRECTION_VALIDATION"
    PROMPT_CONTRACT_READY = "PROMPT_CONTRACT_READY"
    FINALIST_RENDER = "FINALIST_RENDER"
    FINALIST_VISUAL_EVAL = "FINALIST_VISUAL_EVAL"
    WINNER_SELECTION = "WINNER_SELECTION"
    TARGETED_REFINEMENT = "TARGETED_REFINEMENT"
    FINAL_QC = "FINAL_QC"
    B_PASS = "B_PASS"
    NEEDS_USER_FACT = "NEEDS_USER_FACT"
    PROVIDER_FAILURE = "PROVIDER_FAILURE"
    RUNTIME_FAILURE = "RUNTIME_FAILURE"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


class ImageRef(FrozenModel):
    path: Path
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    mime_type: str = "image/png"
    width: int | None = Field(default=None, ge=1)
    height: int | None = Field(default=None, ge=1)
    reference_binding_verified: bool = True
    provider_request_id: str | None = None


class UserFacts(FrozenModel):
    product_name: str = ""
    brand: str | None = None
    address: str | None = None
    verified_soft_facts: list[str] = Field(default_factory=list)
    verified_hard_facts: dict[str, str] = Field(default_factory=dict)
    default_copy_authorized: bool = False


class JobContract(FrozenModel):
    job_id: str = Field(default_factory=lambda: uuid4().hex)
    mode: JobMode
    source_image: ImageRef | None
    stage_a_pass: ImageRef | None = None
    golden_case: str | None = None
    user_facts: UserFacts = Field(default_factory=UserFacts)
    aspect_ratio: str = "9:16"
    stage_a_mode: str = "provided_pass_reference"

    @model_validator(mode="after")
    def validate_required_inputs(self) -> "JobContract":
        if self.mode is JobMode.B and self.source_image is None:
            raise ValueError("Stage B requires a source image")
        if self.aspect_ratio != "9:16":
            raise ValueError("Validation V0 accepts only 9:16")
        return self

