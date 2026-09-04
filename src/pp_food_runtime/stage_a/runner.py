from __future__ import annotations

from pathlib import Path

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.models.job import ImageRef, JobContract
from pp_food_runtime.models.product import ProductLockBridge, ProductTruth, StageAResult
from pp_food_runtime.providers.base import ImageProvider


class StageARunner:
    def __init__(self, image_provider: ImageProvider, artifact_root: Path):
        self.image_provider = image_provider
        self.artifact_root = Path(artifact_root)

    def run(self, job: JobContract, source: ImageRef, truth: ProductTruth) -> StageAResult:
        if source.sha256 != truth.source_sha256:
            raise ValueError("ProductTruth source hash does not match current job source")
        if job.stage_a_mode == "provided_pass_reference":
            if job.stage_a_pass is None:
                raise ValueError("provided_pass_reference requires stage_a_pass")
            if sha256_file(job.stage_a_pass.path) != job.stage_a_pass.sha256:
                raise ValueError("Stage A reference hash mismatch")
            image = job.stage_a_pass
        elif job.stage_a_mode == "generate":
            prompt = self._compile_stage_a_prompt(truth)
            image = self.image_provider.generate(
                [source], prompt, job.aspect_ratio, self.artifact_root / job.job_id / "stage-a.png"
            )
            if not image.reference_binding_verified:
                raise RuntimeError("Stage A reference binding could not be verified")
        else:
            raise ValueError(f"unsupported Stage A mode: {job.stage_a_mode}")

        observed_keys = sorted(truth.observed)
        bridge = ProductLockBridge(
            source_sha256=source.sha256,
            stage_a=image,
            identity_locks=truth.visual_locks or [truth.identity_summary],
            surface_locks=[f"preserve observed {key}" for key in observed_keys] or ["preserve visible surface state"],
            topology_locks=["preserve package/vessel/ingredient topology and physical relationships"],
        )
        return StageAResult(
            status="PASS",
            mode=job.stage_a_mode,
            source_sha256=source.sha256,
            image=image,
            bridge=bridge,
        )

    @staticmethod
    def _compile_stage_a_prompt(truth: ProductTruth) -> str:
        locks = "; ".join(truth.visual_locks or [truth.identity_summary])
        return (
            "Create a clean 9:16 commercial product photograph from the attached current source. "
            f"Identity locks: {locks}. Preserve exact geometry, surface state, topology, package/vessel, "
            "count, ingredient relationships, and visible text. Improve only lighting, cleanup, and product clarity."
        )

