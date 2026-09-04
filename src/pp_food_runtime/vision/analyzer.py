from __future__ import annotations

from pydantic import Field

from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.job import ImageRef, UserFacts
from pp_food_runtime.models.product import EvidenceValue, ProductTruth
from pp_food_runtime.providers.base import VisionProvider


class VisionProductObservation(FrozenModel):
    identity_summary: str
    primary_category: str
    pack_or_food: str
    observed: dict[str, EvidenceValue] = Field(default_factory=dict)
    high_confidence_inferred: dict[str, EvidenceValue] = Field(default_factory=dict)
    unknown: list[str] = Field(default_factory=list)
    sensory_keywords: list[str] = Field(default_factory=list)
    visual_locks: list[str] = Field(default_factory=list)


PRODUCT_OBSERVER_INSTRUCTION = """
You are a forensic product observer, never a creative director. Inspect only the supplied current source image.
Separate directly visible observations, high-confidence sensory inferences, and unknowns. Do not invent business
facts, ingredients, quantities, awards, origins, processes, health claims, or copy. Describe identity, geometry,
surface/material state, ingredient or package topology, vessel/package, readable text, and critical physical
relationships. User-confirmed facts may disambiguate identity but cannot turn invisible packaging claims into
visual observations. Return concise structured JSON only.
""".strip()


class ProductAnalyzer:
    def __init__(self, provider: VisionProvider):
        self.provider = provider

    def analyze(self, source: ImageRef, user_facts: UserFacts) -> ProductTruth:
        facts = {
            "product_name": user_facts.product_name,
            "brand": user_facts.brand,
            "address": user_facts.address,
            "verified_soft_facts": user_facts.verified_soft_facts,
        }
        instruction = f"{PRODUCT_OBSERVER_INSTRUCTION}\nUser-confirmed facts (exact): {facts}"
        observed = self.provider.analyze([source], instruction, VisionProductObservation)
        return ProductTruth(source_sha256=source.sha256, **observed.model_dump())

