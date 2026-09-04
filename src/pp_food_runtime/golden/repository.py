from __future__ import annotations

from pathlib import Path

import yaml

from pp_food_runtime.artifacts.store import sha256_file

from .manifest import GoldenManifest
from .retrieval import GoldenRetriever


class GoldenAssetHashMismatch(ValueError):
    pass


class GoldenRepository:
    def __init__(self, manifest_root: Path, asset_root: Path):
        self.manifest_root = Path(manifest_root)
        self.asset_root = Path(asset_root)
        self._bound: dict[str, GoldenManifest] = {}

    def load_all(self) -> list[GoldenManifest]:
        manifests = []
        for path in sorted(self.manifest_root.glob("*.yaml")):
            loaded = GoldenManifest.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
            manifests.append(self._bound.get(loaded.golden_id, loaded))
        return manifests

    def get(self, golden_id: str) -> GoldenManifest:
        for manifest in self.load_all():
            if manifest.golden_id == golden_id:
                return manifest
        raise KeyError(golden_id)

    def bind_local_asset(self, golden_id: str, path: Path) -> GoldenManifest:
        manifest = self.get(golden_id)
        path = Path(path).resolve()
        actual = sha256_file(path)
        if manifest.sha256 != "LOCAL_BIND_REQUIRED" and actual != manifest.sha256:
            raise GoldenAssetHashMismatch(
                f"{golden_id} expected {manifest.sha256}, received {actual}"
            )
        bound = manifest.model_copy(
            update={"local_asset_path": path, "local_asset_sha256": actual}
        )
        self._bound[golden_id] = bound
        return bound

    def retriever(self) -> GoldenRetriever:
        return GoldenRetriever(self.load_all())

