import base64
import json
from pathlib import Path

import httpx
from PIL import Image
from pydantic import BaseModel

from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.providers.mock import MockImageProvider
from pp_food_runtime.providers.openai_compatible import (
    OpenAICompatibleImageProvider,
    OpenAICompatibleVisionProvider,
)


class TinyResponse(BaseModel):
    result: str


def _png_b64(tmp_path: Path) -> str:
    image_path = tmp_path / "tiny.png"
    Image.new("RGB", (9, 16), "orange").save(image_path)
    return base64.b64encode(image_path.read_bytes()).decode()


def _settings(tmp_path: Path) -> RuntimeSettings:
    return RuntimeSettings(
        artifact_root=tmp_path,
        golden_root=tmp_path,
        vision_base_url="https://vision.test/v1",
        vision_model="vision-model",
        vision_api_key="vision-secret",
        image_base_url="https://image.test/v1",
        image_model="image-model",
        image_api_key="image-secret",
        real_provider_enabled=True,
    )


def test_image_provider_requires_reference_binding(tmp_path):
    provider = MockImageProvider(fixture_image=tmp_path / "missing.png")
    result = provider.generate(
        reference_images=[], prompt="test", aspect_ratio="9:16", output_path=tmp_path / "out.png"
    )
    assert result.reference_binding_verified is False


def test_yunwu_request_attaches_current_reference_and_keeps_key_out_of_payload(tmp_path):
    reference = tmp_path / "reference.png"
    Image.new("RGB", (9, 16), "red").save(reference)
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["authorization"] = request.headers.get("authorization")
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"data": [{"b64_json": _png_b64(tmp_path), "id": "safe-request"}]})

    provider = OpenAICompatibleImageProvider(_settings(tmp_path), transport=httpx.MockTransport(handler))
    result = provider.generate([reference], "safe prompt", "9:16", tmp_path / "out.png")

    assert captured["path"] == "/v1/images/edits"
    assert captured["authorization"] == "Bearer image-secret"
    assert captured["body"]["images"][0]["image_url"].startswith("data:image/png;base64,")
    assert "image-secret" not in json.dumps(captured["body"])
    assert result.reference_binding_verified is True


def test_vision_provider_parses_structured_json(tmp_path):
    source = tmp_path / "source.png"
    Image.new("RGB", (9, 16), "green").save(source)

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["messages"][0]["content"][1]["type"] == "image_url"
        assert "vision-secret" not in json.dumps(body)
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": '{"result":"ok"}'}}]},
        )

    provider = OpenAICompatibleVisionProvider(_settings(tmp_path), transport=httpx.MockTransport(handler))
    assert provider.analyze([source], "observe", TinyResponse).result == "ok"
