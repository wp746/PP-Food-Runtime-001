from __future__ import annotations

import base64
import io
import json
import os
import time
from pathlib import Path
from typing import Any

import httpx
from PIL import Image, ImageOps

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.models.job import ImageRef

from .base import ImageProvider, ProviderCapabilityProfile, ResponseT, VisionProvider


BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _path_of(item: Path | ImageRef) -> Path:
    return Path(item.path if isinstance(item, ImageRef) else item)


def _image_data_url(item: Path | ImageRef) -> str:
    path = _path_of(item)
    with Image.open(path) as image:
        normalized = ImageOps.exif_transpose(image)
        changed = normalized.size != image.size or image.getexif().get(274) not in (None, 1)
        if changed:
            buffer = io.BytesIO()
            normalized.convert("RGB").save(buffer, format="JPEG", quality=95)
            return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _extract_json_text(content: Any) -> str:
    if isinstance(content, list):
        content = "".join(str(part.get("text", "")) for part in content if isinstance(part, dict))
    text = str(content).strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"): lines = lines[1:]
        if lines and lines[-1].strip() == "```": lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


class OpenAICompatibleVisionProvider(VisionProvider):
    def __init__(self, settings: RuntimeSettings, transport: httpx.BaseTransport | None = None):
        self.settings = settings
        self._transport = transport
        self.capability_profile = ProviderCapabilityProfile(
            provider_id="siliconflow-openai-compatible",
            model_id=settings.vision_model,
            reference_edit=False,
            multiple_references=True,
            masks=False,
            seed=False,
            text_rendering="observer-only",
            aspect_ratio=["any-input"],
            max_resolution="provider-managed",
        )

    def analyze(self, images, instruction: str, response_model: type[ResponseT]) -> ResponseT:
        schema = json.dumps(response_model.model_json_schema(), ensure_ascii=False, sort_keys=True)
        content: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": f"{instruction}\nReturn one JSON object matching this schema exactly:\n{schema}",
            }
        ]
        content.extend(
            {"type": "image_url", "image_url": {"url": _image_data_url(image)}} for image in images
        )
        payload = {
            "model": self.settings.vision_model,
            "messages": [{"role": "user", "content": content}],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self.settings.vision_api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "User-Agent": BROWSER_UA,
        }
        with httpx.Client(
            base_url=self.settings.vision_base_url.rstrip("/") + "/",
            timeout=self.settings.request_timeout_seconds,
            transport=self._transport,
        ) as client:
            response = client.post("chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        text = _extract_json_text(data["choices"][0]["message"]["content"])
        return response_model.model_validate_json(text)

    def check_reachability(self) -> bool:
        headers = {"Authorization": f"Bearer {self.settings.vision_api_key.get_secret_value()}", "User-Agent": BROWSER_UA}
        with httpx.Client(timeout=min(self.settings.request_timeout_seconds, 30), transport=self._transport) as client:
            response = client.get(self.settings.vision_base_url.rstrip("/") + "/models", headers=headers)
            return response.status_code == 200


class OpenAICompatibleImageProvider(ImageProvider):
    def __init__(self, settings: RuntimeSettings, transport: httpx.BaseTransport | None = None):
        self.settings = settings
        self._transport = transport
        self.capability_profile = ProviderCapabilityProfile(
            provider_id="yunwu-openai-compatible",
            model_id=settings.image_model,
            reference_edit=True,
            multiple_references=True,
            masks=False,
            seed=False,
            text_rendering="strong",
            aspect_ratio=["9:16"],
            max_resolution="4k-provider-managed",
        )

    def generate(self, reference_images, prompt: str, aspect_ratio: str, output_path: Path) -> ImageRef:
        refs = [_image_data_url(item) for item in reference_images]
        payload: dict[str, Any] = {
            "model": self.settings.image_model,
            "prompt": prompt,
            "size": aspect_ratio,
            "resolution": "4k",
            "n": 1,
        }
        if refs:
            payload["images"] = [{"image_url": item} for item in refs]
        endpoint = "images/edits" if refs else "images/generations"
        headers = {
            "Authorization": f"Bearer {self.settings.image_api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "User-Agent": BROWSER_UA,
        }
        with httpx.Client(
            base_url=self.settings.image_base_url.rstrip("/") + "/",
            timeout=self.settings.request_timeout_seconds,
            transport=self._transport,
        ) as client:
            response = client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            request_id = response.headers.get("x-request-id") or _safe_request_id(data)
            image_url = _extract_image_url(data)
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = output_path.with_name(f".{output_path.name}.{os.getpid()}.tmp")
            try:
                if image_url.startswith("data:"):
                    temp_path.write_bytes(base64.b64decode(image_url.split(",", 1)[1]))
                else:
                    self._download(client, image_url, headers, temp_path)
                with Image.open(temp_path) as image:
                    image.verify()
                os.replace(temp_path, output_path)
            finally:
                temp_path.unlink(missing_ok=True)
        with Image.open(output_path) as image:
            width, height = image.size
        return ImageRef(
            path=output_path.resolve(),
            sha256=sha256_file(output_path),
            width=width,
            height=height,
            reference_binding_verified=bool(refs),
            provider_request_id=request_id,
        )

    def _download(self, client: httpx.Client, url: str, headers: dict[str, str], path: Path) -> None:
        last_error: Exception | None = None
        for attempt in range(4):
            try:
                response = client.get(url, headers=headers, follow_redirects=True)
                response.raise_for_status()
                path.write_bytes(response.content)
                if path.stat().st_size == 0:
                    raise RuntimeError("provider image download returned zero bytes")
                return
            except Exception as exc:
                last_error = exc
                if attempt < 3:
                    time.sleep(2 * (attempt + 1))
        raise RuntimeError("provider image download failed") from last_error

    def check_reachability(self) -> bool:
        headers = {"Authorization": f"Bearer {self.settings.image_api_key.get_secret_value()}", "User-Agent": BROWSER_UA}
        with httpx.Client(timeout=min(self.settings.request_timeout_seconds, 30), transport=self._transport) as client:
            response = client.get(self.settings.image_base_url.rstrip("/") + "/models", headers=headers)
            return response.status_code == 200


def _safe_request_id(data: dict[str, Any]) -> str | None:
    root = data.get("data")
    node = root[0] if isinstance(root, list) and root else root
    if isinstance(node, dict):
        value = node.get("request_id") or node.get("task_id") or node.get("id")
        return str(value) if value else None
    value = data.get("request_id") or data.get("task_id") or data.get("id")
    return str(value) if value else None


def _extract_image_url(data: dict[str, Any]) -> str:
    root = data.get("data")
    nodes = root if isinstance(root, list) else [root] if isinstance(root, dict) else []
    for node in nodes:
        if isinstance(node, dict):
            if isinstance(node.get("url"), str):
                return node["url"]
            if isinstance(node.get("b64_json"), str):
                return "data:image/png;base64," + node["b64_json"]
            result = node.get("result")
            if isinstance(result, str):
                try: result = json.loads(result)
                except json.JSONDecodeError: result = None
            if isinstance(result, dict):
                for image in result.get("images", []):
                    if isinstance(image.get("url"), str): return image["url"]
                    if isinstance(image.get("b64_json"), str): return "data:image/png;base64," + image["b64_json"]
    raise RuntimeError("provider response contained no image URL or base64 image")
