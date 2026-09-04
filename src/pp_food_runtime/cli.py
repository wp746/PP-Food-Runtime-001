from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import typer
from PIL import Image

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.engine import ValidationEngine
from pp_food_runtime.golden.repository import GoldenRepository
from pp_food_runtime.models.job import ImageRef, JobContract, JobMode, UserFacts
from pp_food_runtime.providers.openai_compatible import (
    OpenAICompatibleImageProvider,
    OpenAICompatibleVisionProvider,
)


app = typer.Typer(no_args_is_help=True, add_completion=False)

CASE_FACTS = {
    "S01": {
        "product_name": "椰椰西瓜冰",
        "brand": "有幸小食院",
        "address": "安康市高新区天一广场",
        "verified_soft_facts": ["纯手制"],
        "default_copy_authorized": True,
    },
    "S02": {
        "product_name": "桔子罐头",
        "brand": "林家铺子",
        "default_copy_authorized": True,
    },
}


def image_ref(path: Path) -> ImageRef:
    path = path.resolve()
    with Image.open(path) as image:
        width, height = image.size
        image.verify()
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return ImageRef(path=path, sha256=sha256_file(path), mime_type=mime, width=width, height=height)


def providers(settings: RuntimeSettings):
    return OpenAICompatibleVisionProvider(settings), OpenAICompatibleImageProvider(settings)


@app.command("provider-check")
def provider_check() -> None:
    settings = RuntimeSettings.from_env()
    summary = settings.safe_provider_summary()
    if not settings.real_provider_enabled:
        typer.echo(json.dumps({**summary, "reachable": False}, ensure_ascii=False, sort_keys=True))
        raise typer.Exit(code=2)
    vision, image = providers(settings)
    result = {
        **summary,
        "vision_reachable": vision.check_reachability(),
        "image_reachable": image.check_reachability(),
        "vision_capabilities": vision.capability_profile.model_dump(mode="json"),
        "image_capabilities": image.capability_profile.model_dump(mode="json"),
    }
    typer.echo(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["vision_reachable"] or not result["image_reachable"]:
        raise typer.Exit(code=3)


@app.command("validate-b")
def validate_b(
    case: str = typer.Option(..., "--case"),
    source: Path | None = typer.Option(None, "--source"),
    stage_a: Path | None = typer.Option(None, "--stage-a"),
    golden: Path | None = typer.Option(None, "--golden"),
    product_name: str | None = typer.Option(None, "--product-name"),
    brand: str | None = typer.Option(None, "--brand"),
    address: str | None = typer.Option(None, "--address"),
    default_copy: bool = typer.Option(False, "--default-copy"),
    live: bool = typer.Option(False, "--live"),
) -> None:
    case = case.upper()
    if case not in CASE_FACTS:
        raise typer.BadParameter("Validation V0 first milestone supports S01 and S02")
    if not live:
        raise typer.BadParameter("real candidate generation requires explicit --live")
    repo_root = Path.cwd()
    source = source or repo_root / "validation_inputs" / f"{case}-source.jpg"
    stage_a = stage_a or repo_root / "validation_inputs" / f"{case}-stage-a.png"
    golden = golden or repo_root / "goldens" / "assets" / f"{case}.png"
    for label, path in (("source", source), ("stage-a", stage_a), ("golden", golden)):
        if not path.is_file():
            raise typer.BadParameter(f"missing {label} image: {path}")

    settings = RuntimeSettings.from_env()
    if not settings.real_provider_enabled:
        raise typer.BadParameter("complete PP Vision and Image provider configuration is required")
    settings = settings.model_copy(update={"artifact_root": settings.artifact_root / case})
    vision, image = providers(settings)
    repository = GoldenRepository(repo_root / "goldens" / "manifests", repo_root / "goldens" / "assets")
    repository.bind_local_asset(case, golden)
    facts_data = dict(CASE_FACTS[case])
    if product_name: facts_data["product_name"] = product_name
    if brand: facts_data["brand"] = brand
    if address: facts_data["address"] = address
    if default_copy: facts_data["default_copy_authorized"] = True
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    job = JobContract(
        job_id=f"{timestamp}-{uuid4().hex[:8]}",
        mode=JobMode.B,
        source_image=image_ref(source),
        stage_a_pass=image_ref(stage_a),
        golden_case=case,
        user_facts=UserFacts(**facts_data),
    )
    result = ValidationEngine(settings, vision, image, repository).run(job)
    typer.echo(
        json.dumps(
            {
                "job_id": result.job_id,
                "final_state": result.final_state.value,
                "final_decision": result.final_decision.value,
                "artifact_dir": str(result.artifact_dir),
                "final_image": str(result.final_image.path) if result.final_image else None,
                "candidates": {key: str(value.path) for key, value in result.candidates.items()},
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    app()
