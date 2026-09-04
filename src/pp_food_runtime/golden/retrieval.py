from __future__ import annotations

from collections.abc import Mapping

from pp_food_runtime.models.visual import GoldenPrinciplePack

from .manifest import GoldenManifest


class GoldenRetriever:
    def __init__(self, manifests: list[GoldenManifest]):
        self.manifests = manifests

    def retrieve(self, query: Mapping[str, object], limit: int = 3) -> list[GoldenPrinciplePack]:
        category = str(query.get("primary_category", ""))
        pack_or_food = str(query.get("pack_or_food", ""))
        sensory = {str(value).lower() for value in query.get("sensory_tags", []) or []}
        problems = {str(value).lower() for value in query.get("visual_problems", []) or []}

        def rank(manifest: GoldenManifest) -> tuple[int, int, str]:
            score = 0
            score += 10 if manifest.primary_category == category else 0
            score += 4 if manifest.pack_or_food == pack_or_food else 0
            score += len(sensory.intersection(tag.lower() for tag in manifest.sensory_tags)) * 2
            score += len(problems.intersection(tag.lower() for tag in manifest.visual_problems)) * 2
            return (-score, manifest.tier_rank, manifest.golden_id)

        packs = []
        for manifest in sorted(self.manifests, key=rank)[:limit]:
            packs.append(
                GoldenPrinciplePack(
                    golden_id=manifest.golden_id,
                    tier=manifest.tier.value,
                    principles=manifest.transferable_principles,
                    prohibited_transfer=manifest.prohibited_transfer,
                    local_asset_path=str(manifest.local_asset_path) if manifest.local_asset_path else None,
                    local_asset_sha256=manifest.local_asset_sha256,
                )
            )
        return packs

