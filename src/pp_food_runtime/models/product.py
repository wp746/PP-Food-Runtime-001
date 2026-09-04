from __future__ import annotations

from pydantic import Field

from .common import FrozenModel
from .job import ImageRef


class EvidenceValue(FrozenModel):
    value: str
    confidence: float = Field(ge=0, le=1)
    visible_evidence: str


class ProductTruth(FrozenModel):
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    identity_summary: str
    primary_category: str
    pack_or_food: str
    observed: dict[str, EvidenceValue] = Field(default_factory=dict)
    high_confidence_inferred: dict[str, EvidenceValue] = Field(default_factory=dict)
    unknown: list[str] = Field(default_factory=list)
    sensory_keywords: list[str] = Field(default_factory=list)
    visual_locks: list[str] = Field(default_factory=list)


class ProductLockBridge(FrozenModel):
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    stage_a: ImageRef
    identity_locks: list[str]
    surface_locks: list[str]
    topology_locks: list[str]


class StageAResult(FrozenModel):
    status: str
    mode: str
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    image: ImageRef
    bridge: ProductLockBridge

