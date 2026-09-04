from __future__ import annotations

from pp_food_runtime.artifacts.store import ArtifactStore
from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.golden.repository import GoldenRepository
from pp_food_runtime.models.job import JobContract
from pp_food_runtime.providers.base import ImageProvider, VisionProvider
from pp_food_runtime.stage_b.runner import JobResult, StageBRunner


class ValidationEngine:
    def __init__(
        self,
        settings: RuntimeSettings,
        vision_provider: VisionProvider,
        image_provider: ImageProvider,
        golden_repository: GoldenRepository,
    ):
        self.runner = StageBRunner(
            settings,
            vision_provider,
            image_provider,
            golden_repository,
            ArtifactStore(settings.artifact_root),
        )

    def run(self, job: JobContract) -> JobResult:
        return self.runner.run(job)

