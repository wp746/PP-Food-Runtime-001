from __future__ import annotations

from pathlib import Path

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.models.job import ImageRef, JobContract
from pp_food_runtime.models.product import ProductLockBridge, ProductTruth, StageAQCEvaluation, StageAResult
from pp_food_runtime.providers.base import ImageProvider

from .evaluator import StageAEvaluator


class StageAQCFailure(RuntimeError):
    def __init__(self, evaluations: list[StageAQCEvaluation]):
        self.evaluations = evaluations
        super().__init__(f"Stage A failed visual QC after {len(evaluations)} attempt(s)")


class StageARunner:
    def __init__(
        self,
        image_provider: ImageProvider,
        artifact_root: Path,
        evaluator: StageAEvaluator | None = None,
        max_attempts: int = 3,
    ):
        self.image_provider = image_provider
        self.artifact_root = Path(artifact_root)
        self.evaluator = evaluator
        self.max_attempts = max_attempts

    def run(self, job: JobContract, source: ImageRef, truth: ProductTruth) -> StageAResult:
        if source.sha256 != truth.source_sha256:
            raise ValueError("ProductTruth source hash does not match current job source")
        if job.stage_a_mode == "provided_pass_reference":
            if job.stage_a_pass is None:
                raise ValueError("provided_pass_reference requires stage_a_pass")
            if sha256_file(job.stage_a_pass.path) != job.stage_a_pass.sha256:
                raise ValueError("Stage A reference hash mismatch")
            image = job.stage_a_pass
            qc = None
        elif job.stage_a_mode == "generate":
            if self.evaluator is None:
                raise RuntimeError("generated Stage A requires an independent visual QC evaluator")
            evaluations: list[StageAQCEvaluation] = []
            repair_notes: list[str] = []
            for attempt in range(1, self.max_attempts + 1):
                prompt = self._compile_stage_a_prompt(truth, repair_notes)
                candidate_id = f"attempt-{attempt}"
                image = self.image_provider.generate(
                    [source],
                    prompt,
                    job.aspect_ratio,
                    self.artifact_root / job.job_id / "stage-a" / f"{candidate_id}.png",
                )
                qc = self.evaluator.evaluate(
                    candidate_id=candidate_id,
                    source=source,
                    candidate=image,
                    truth=truth,
                )
                evaluations.append(qc)
                if qc.status == "PASS":
                    break
                repair_notes = list(dict.fromkeys(qc.critical_drifts + qc.failed_dimensions))
            else:
                raise StageAQCFailure(evaluations)
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
            qc=qc,
        )

    @staticmethod
    def _compile_stage_a_prompt(truth: ProductTruth, repair_notes: list[str] | None = None) -> str:
        locks = "; ".join(truth.visual_locks or [truth.identity_summary])
        observed = "; ".join(
            f"{key}: {item.value}" for key, item in truth.observed.items()
        )
        repairs = "; ".join(repair_notes or [])
        return "\n\n".join(
            [
                "## A1 REFERENCE LOCK\n"
                "Use only the attached current-job source as binding visual truth. This is reference editing, not loose inspiration. "
                "Preserve the exact visible food/product identity. Remove source watermark and other non-product overlays.",
                "## A2 PRODUCT DNA + SURFACE STATE\n"
                f"Identity locks: {locks}. Visible evidence: {observed or truth.identity_summary}. "
                "Lock exact product type, count, dimensions, proportions, browned/cooked state, moisture, ingredient identity, "
                "ingredient sizes, ingredient topology, and every identity-critical physical relationship.",
                "## A3 VESSEL / PACKAGE / DIRECT SUPPORT\n"
                "Preserve the current vessel/package/direct support identity, shape, rim, contact points, overlap pattern, plating "
                "and arrangement. Do not replace the plate, invent packaging, add servings, remove servings, or restyle the food.",
                "## A4 COMMERCIAL HERO PHOTOGRAPHY\n"
                "Create one exact 9:16 premium commercial hero photograph. The food/product is the unmistakable first read, large "
                "and tactile, with controlled perspective, appetizing texture, dimensional key light, clean separation and realistic physics. "
                "Upgrade only camera, light, cleanup, focus, background and commercial finish.",
                "## A5 CURRENT CATEGORY BACKGROUND ARCHITECTURE\n"
                f"Current category signal: {truth.primary_category}. Build a restrained product-derived photographic stage from the current "
                "food's own palette, heat, texture and geometry. Use foreground, hero and atmospheric depth without themed scenery, "
                "generic prop packs, literal restaurant sets, or environment dominance.",
                "## A6 HARD NEGATIVES\n"
                "No poster, headline, subtitle, slogan, promotion, badge, logo, QR code, price, phone, address, people, hands, duplicate food, "
                "missing food, changed count, changed filling, invented topping, changed vessel, fake steam physics, illustration, collage, border, "
                f"or source watermark. Targeted repair notes: {repairs or 'none; preserve all locked dimensions'}.",
            ]
        )
