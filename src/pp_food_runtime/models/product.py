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


class StageAQCEvaluation(FrozenModel):
    candidate_id: str
    status: str
    mechanical_pass: bool
    reference_binding_verified: bool
    product_identity_score: float = Field(ge=0, le=10)
    geometry_count_score: float = Field(ge=0, le=10)
    ingredient_topology_score: float = Field(ge=0, le=10)
    plating_arrangement_score: float = Field(ge=0, le=10)
    physical_relationships_score: float = Field(ge=0, le=10)
    surface_state_score: float = Field(ge=0, le=10)
    vessel_package_score: float = Field(ge=0, le=10)
    commercial_photography_score: float = Field(ge=0, le=10)
    semantic_relevance_score: float = Field(ge=0, le=10)
    hero_spatial_score: float = Field(ge=0, le=10)
    appetite_score: float = Field(ge=0, le=10)
    failed_dimensions: list[str] = Field(default_factory=list)
    critical_drifts: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class StageAResult(FrozenModel):
    status: str
    mode: str
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    image: ImageRef
    bridge: ProductLockBridge
    qc: StageAQCEvaluation | None = None
