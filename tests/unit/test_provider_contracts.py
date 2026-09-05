import base64
import io
import json
from pathlib import Path
import time

import httpx
import pytest
from PIL import Image
from pydantic import BaseModel

from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.providers.mock import MockImageProvider
from pp_food_runtime.providers.openai_compatible import (
    ImageProviderTimeout,
    OpenAICompatibleImageProvider,
    OpenAICompatibleVisionProvider,
    QCProviderTimeout,
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


def test_yunwu_transport_retry_reuses_identical_generation_request(tmp_path):
    reference = tmp_path / "reference.png"
    Image.new("RGB", (9, 16), "red").save(reference)
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(
            {
                "path": request.url.path,
                "body": json.loads(request.content),
            }
        )
        if len(requests) == 1:
            raise httpx.ReadTimeout("first transport timeout", request=request)
        return httpx.Response(
            200,
            json={"data": [{"b64_json": _png_b64(tmp_path), "id": "retry-request"}]},
        )

    provider = OpenAICompatibleImageProvider(
        _settings(tmp_path),
        transport=httpx.MockTransport(handler),
        hard_timeout_seconds=240,
        transport_retries=1,
    )

    result = provider.generate([reference], "same prompt", "9:16", tmp_path / "out.png")

    assert len(requests) == 2
    assert requests[0] == requests[1]
    assert requests[1]["body"]["model"] == "image-model"
    assert requests[1]["body"]["prompt"] == "same prompt"
    assert requests[1]["body"]["images"][0]["image_url"].startswith("data:image/png;base64,")
    assert result.provider_request_id == "retry-request"


def test_yunwu_timeout_retries_once_then_returns_explicit_code(tmp_path):
    reference = tmp_path / "reference.png"
    Image.new("RGB", (9, 16), "red").save(reference)
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ReadTimeout("slow image response", request=request)

    provider = OpenAICompatibleImageProvider(
        _settings(tmp_path),
        transport=httpx.MockTransport(handler),
        hard_timeout_seconds=240,
        transport_retries=1,
    )

    with pytest.raises(ImageProviderTimeout, match="IMAGE_PROVIDER_TIMEOUT"):
        provider.generate([reference], "same prompt", "9:16", tmp_path / "out.png")

    assert calls == 2
    assert not (tmp_path / "out.png").exists()


def test_yunwu_wall_clock_deadline_interrupts_slow_transport(tmp_path):
    reference = tmp_path / "reference.png"
    Image.new("RGB", (9, 16), "red").save(reference)
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        time.sleep(0.2)
        return httpx.Response(
            200,
            json={"data": [{"b64_json": _png_b64(tmp_path), "id": "too-late"}]},
        )

    provider = OpenAICompatibleImageProvider(
        _settings(tmp_path),
        transport=httpx.MockTransport(handler),
        hard_timeout_seconds=0.05,
        transport_retries=1,
    )
    started = time.perf_counter()

    with pytest.raises(ImageProviderTimeout, match="IMAGE_PROVIDER_TIMEOUT"):
        provider.generate([reference], "same prompt", "9:16", tmp_path / "out.png")

    assert calls == 2
    assert time.perf_counter() - started < 0.3


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


def test_vision_provider_downscales_large_input_without_changing_source(tmp_path):
    source = tmp_path / "large.png"
    Image.new("RGB", (3000, 4000), "green").save(source)
    original_bytes = source.read_bytes()

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        data_url = body["messages"][0]["content"][1]["image_url"]["url"]
        encoded = data_url.split(",", 1)[1]
        with Image.open(io.BytesIO(base64.b64decode(encoded))) as uploaded:
            assert max(uploaded.size) == 1600
            assert uploaded.format == "JPEG"
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": '{"result":"ok"}'}}]},
        )

    provider = OpenAICompatibleVisionProvider(_settings(tmp_path), transport=httpx.MockTransport(handler))

    assert provider.analyze([source], "observe", TinyResponse).result == "ok"
    assert source.read_bytes() == original_bytes


def test_siliconflow_timeout_retries_once_then_returns_explicit_code(tmp_path):
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ReadTimeout("slow vision response", request=request)

    provider = OpenAICompatibleVisionProvider(
        _settings(tmp_path),
        transport=httpx.MockTransport(handler),
        hard_timeout_seconds=90,
        transport_retries=1,
    )

    with pytest.raises(QCProviderTimeout, match="QC_PROVIDER_TIMEOUT"):
        provider.analyze([], "text-only probe", TinyResponse)

    assert calls == 2


def test_siliconflow_wall_clock_deadline_interrupts_slow_transport(tmp_path):
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        time.sleep(0.2)
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": '{"result":"too late"}'}}]},
        )

    provider = OpenAICompatibleVisionProvider(
        _settings(tmp_path),
        transport=httpx.MockTransport(handler),
        hard_timeout_seconds=0.05,
        transport_retries=1,
    )
    started = time.perf_counter()

    with pytest.raises(QCProviderTimeout, match="QC_PROVIDER_TIMEOUT"):
        provider.analyze([], "text-only probe", TinyResponse)

    assert calls == 2
    assert time.perf_counter() - started < 0.3


def test_siliconflow_reachability_uses_same_timeout_and_retry_contract(tmp_path):
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ReadTimeout("slow models response", request=request)

    provider = OpenAICompatibleVisionProvider(
        _settings(tmp_path),
        transport=httpx.MockTransport(handler),
        hard_timeout_seconds=90,
        transport_retries=1,
    )

    with pytest.raises(QCProviderTimeout, match="QC_PROVIDER_TIMEOUT"):
        provider.check_reachability()

    assert calls == 2
