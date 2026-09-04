from pathlib import Path

from PIL import Image

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.engine import ValidationEngine
from pp_food_runtime.golden.repository import GoldenRepository
from pp_food_runtime.models.evaluation import GoldenVector
from pp_food_runtime.models.job import ImageRef, JobContract, JobMode, UserFacts
from pp_food_runtime.providers.mock import MockImageProvider, MockVisionProvider
from pp_food_runtime.stage_b.evaluator import RawEvaluation, RawPairwiseComparison
from pp_food_runtime.vision.analyzer import VisionProductObservation


def make_engine_and_job(tmp_path: Path):
    paths = {}
    for name, color in (("source", "orange"), ("stage-a", "gold"), ("golden", "yellow")):
        path = tmp_path / f"{name}.png"
        Image.new("RGB", (90, 160), color).save(path)
        paths[name] = path
    manifest_root = tmp_path / "manifests"
    manifest_root.mkdir()
    manifest_root.joinpath("S01.yaml").write_text(
        "\n".join(
            [
                "golden_id: S01",
                "tier: S_TIER",
                "name: test golden",
                "primary_category: COLD_DRINK_FRUIT_DESSERT",
                "pack_or_food: FOOD",
                "sensory_tags: [cold, fruit]",
                "visual_problems: [product_hero, headline_pressure]",
                "asset_filename: S01.png",
                f'sha256: "{sha256_file(paths["golden"])}"',
                "transferable_principles: [strong product and headline, multi-depth composition]",
                "prohibited_transfer: [old brand, old copy, exact layout]",
            ]
        ),
        encoding="utf-8",
    )
    source = ImageRef(path=paths["source"], sha256=sha256_file(paths["source"]), width=90, height=160)
    stage_a = ImageRef(path=paths["stage-a"], sha256=sha256_file(paths["stage-a"]), width=90, height=160)
    evidence = [
        {
            "dimension": field,
            "what_is_visible": "strong visible execution",
            "where_visible": "hero and headline planes",
            "why_it_helps_or_hurts": "supports campaign pressure",
        }
        for field in GoldenVector.model_fields
    ]
    vision = MockVisionProvider(
        {
            VisionProductObservation: {
                "identity_summary": "cold watermelon drink in a clear cup",
                "primary_category": "COLD_DRINK_FRUIT_DESSERT",
                "pack_or_food": "FOOD",
                "observed": {},
                "high_confidence_inferred": {},
                "unknown": [],
                "sensory_keywords": ["cold", "fruit"],
                "visual_locks": ["clear cup", "watermelon red liquid"],
            },
            RawEvaluation: {
                "mechanical_pass": True,
                "product_truth_pass": True,
                "copy_truth_pass": True,
                "first_read_order": ["product", "headline", "support"],
                "golden_vector": GoldenVector.all_at(9.2).model_dump(exclude_computed_fields=True),
                "critical_failures": [],
                "materially_weaker_core_dimensions": [],
                "evidence": evidence,
                "confidence": 0.9,
            },
            RawPairwiseComparison: {
                "winner_id": "primary",
                "visually_distinct": True,
                "winner_reason": "primary keeps the product strongest while retaining campaign depth",
                "evidence": ["both rendered candidates were compared side by side"],
                "confidence": 0.92,
            },
        }
    )
    settings = RuntimeSettings(
        artifact_root=tmp_path / "validation_runs",
        golden_root=tmp_path,
        vision_base_url="mock://vision",
        vision_model="mock-vision",
        vision_api_key="mock-secret",
        image_base_url="mock://image",
        image_model="mock-image",
        image_api_key="mock-secret",
        real_provider_enabled=False,
    )
    repository = GoldenRepository(manifest_root, tmp_path)
    repository.bind_local_asset("S01", paths["golden"])
    engine = ValidationEngine(settings, vision, MockImageProvider(paths["golden"]), repository)
    job = JobContract(
        job_id="S01-test",
        mode=JobMode.B,
        source_image=source,
        stage_a_pass=stage_a,
        golden_case="S01",
        user_facts=UserFacts(product_name="椰椰西瓜冰", brand="有幸小食院", default_copy_authorized=True),
    )
    return engine, job
