from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image
from pydantic import BaseModel

from pp_food_runtime.models.job import ImageRef, JobContract


SECRET_FIELD_FRAGMENTS = ("api_key", "authorization", "bearer", "secret", "access_token")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_no_secret_fields(value: Any, trail: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            if any(fragment in normalized for fragment in SECRET_FIELD_FRAGMENTS):
                raise ValueError(f"secret-shaped field rejected at {trail}.{key}")
            _assert_no_secret_fields(child, f"{trail}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _assert_no_secret_fields(child, f"{trail}[{index}]")


class ArtifactStore:
    def __init__(self, root: Path):
        self.root = Path(root)

    def job_dir(self, job_id: str) -> Path:
        if not job_id or Path(job_id).is_absolute() or ".." in Path(job_id).parts:
            raise ValueError("invalid job id")
        path = self.root / job_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def target(self, job_id: str, relative: str) -> Path:
        if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError("invalid artifact path")
        root = self.job_dir(job_id).resolve()
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            raise ValueError("artifact path escapes job directory")
        target.parent.mkdir(parents=True, exist_ok=True)
        return target

    def create_job(self, job: JobContract) -> Path:
        path = self.job_dir(job.job_id)
        self.write_json(job.job_id, "contracts/job", job)
        return path

    def write_json(self, job_id: str, name: str, payload: BaseModel | dict) -> Path:
        data = payload.model_dump(mode="json") if isinstance(payload, BaseModel) else payload
        _assert_no_secret_fields(data)
        destination = self.target(job_id, f"{name}.json")
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            delete=False,
        ) as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            temp_path = Path(handle.name)
        os.replace(temp_path, destination)
        return destination

    def copy_image(self, job_id: str, label: str, source: Path) -> ImageRef:
        source = Path(source)
        if not source.is_file():
            raise FileNotFoundError(source)
        target_dir = self.job_dir(job_id)
        suffix = source.suffix.lower() or ".img"
        candidate = self.target(job_id, f"{label}{suffix}")
        counter = 2
        while candidate.exists():
            candidate = self.target(job_id, f"{label}-{counter}{suffix}")
            counter += 1
        fd, temp_name = tempfile.mkstemp(dir=candidate.parent, prefix=f".{candidate.name}.", suffix=suffix)
        os.close(fd)
        temp_path = Path(temp_name)
        try:
            shutil.copy2(source, temp_path)
            os.replace(temp_path, candidate)
        finally:
            temp_path.unlink(missing_ok=True)

        width = height = None
        try:
            with Image.open(candidate) as image:
                width, height = image.size
        except Exception:
            pass
        mime = "image/jpeg" if suffix in {".jpg", ".jpeg"} else "image/png"
        return ImageRef(
            path=candidate.resolve(),
            sha256=sha256_file(candidate),
            mime_type=mime,
            width=width,
            height=height,
        )
