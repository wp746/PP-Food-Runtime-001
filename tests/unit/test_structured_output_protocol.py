import json

import httpx
import pytest

from pp_food_runtime.config import RuntimeSettings
from pp_food_runtime.providers.openai_compatible import (
    OpenAICompatibleVisionProvider,
    StructuredOutputProtocolError,
)
from pp_food_runtime.stage_b.evaluator import RawEvaluation


def _settings(tmp_path):
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


def test_vision_provider_rejects_schema_echo_as_protocol_failure(tmp_path):
    schema_echo = RawEvaluation.model_json_schema()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": json.dumps(schema_echo)}}
                ]
            },
        )

    provider = OpenAICompatibleVisionProvider(
        _settings(tmp_path),
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(StructuredOutputProtocolError, match="SCHEMA_ECHO"):
        provider.analyze([], "production evaluator", RawEvaluation)
