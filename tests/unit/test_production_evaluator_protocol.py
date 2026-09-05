from pathlib import Path

from PIL import Image

from pp_food_runtime.artifacts.store import sha256_file
from pp_food_runtime.models.evaluation import FailureCode, FinalDecision, GoldenVector
from pp_food_runtime.models.job import ImageRef
from pp_food_runtime.models.product import ProductTruth
from pp_food_runtime.models.visual import CategoryVisualTranslation
from pp_food_runtime.providers.openai_compatible import StructuredOutputProtocolError
from pp_food_runtime.stage_b.copy_firewall import CopyAllowlist
from pp_food_runtime.stage_b.evaluator import BEvaluator, EvaluationContext, RawEvaluation


class SequenceVisionProvider:
    def __init__(self, sequence):
        self.sequence = list(sequence)
        self.calls = []

    def analyze(self, images, instruction, response_model):
        self.calls.append(
            {
                "images": list(images),
                "instruction": instruction,
                "response_model": response_model,
            }
        )
        value = self.sequence.pop(0)
        if isinstance(value, Exception):
            raise value
        return value


def _context(tmp_path: Path) -> EvaluationContext:
    image_path = tmp_path / "candidate.png"
    Image.new("RGB", (90, 160), "orange").save(image_path)
    digest = sha256_file(image_path)
    source = ImageRef(path=image_path, sha256=digest, width=90, height=160)
    stage_a = ImageRef(path=image_path, sha256=digest, width=90, height=160)
    candidate = ImageRef(
        path=image_path,
        sha256=digest,
        width=90,
        height=160,
        reference_binding_verified=True,
    )
    truth = ProductTruth(
        source_sha256=digest,
        identity_summary="glass jar of canned mandarins",
        primary_category="CANNED_FRUIT_RETAIL",
        pack_or_food="PACK",
        sensory_keywords=["citrus", "juicy"],
        visual_locks=["glass jar", "orange mandarin segments"],
    )
    translation = CategoryVisualTranslation(
        primary_category="CANNED_FRUIT_RETAIL",
        sensory_evidence=["bright citrus", "juicy fruit"],
        emotional_semantics=["fresh", "sunlit"],
        brand_temperament=["retail", "clean"],
        primary_material_metaphor="translucent citrus glass",
        typography_translation="bold retail headline with citrus-derived material cues",
        color_translation="orange, warm white, fresh green accents",
        lighting_translation="bright directional sunlight that reveals jar and fruit",
        spatial_translation="package-led multi-depth retail campaign composition",
        motion_energy_translation="fresh citrus lift",
        information_system="controlled retail information hierarchy",
        one_big_idea_seed="sunlight concentrated into the mandarin jar",
        forbidden_drift=["night market", "generic black-gold food poster"],
    )
    return EvaluationContext(
        candidate_id="primary",
        source=source,
        stage_a=stage_a,
        candidate=candidate,
        truth=truth,
        copy_allowlist=CopyAllowlist(product_name="桔子罐头"),
        translation=translation,
        goldens=[],
    )


def _passing_raw() -> RawEvaluation:
    return RawEvaluation(
        mechanical_pass=True,
        product_truth_pass=True,
        copy_truth_pass=True,
        first_read_order=["product", "headline"],
        golden_vector=GoldenVector.all_at(9.0),
        critical_failures=[],
        materially_weaker_core_dimensions=[],
        evidence=[],
        confidence=0.9,
    )


def test_production_evaluator_retries_protocol_once_without_changing_images(tmp_path):
    provider = SequenceVisionProvider(
        [StructuredOutputProtocolError("SCHEMA_ECHO"), _passing_raw()]
    )
    evaluator = BEvaluator(provider)
    context = _context(tmp_path)

    gate = evaluator.evaluate_production(context)

    assert gate.decision is FinalDecision.PASS
    assert len(provider.calls) == 2
    assert provider.calls[0]["images"] == provider.calls[1]["images"]
    assert "INSTANCE_RETRY" in provider.calls[1]["instruction"]


def test_production_evaluator_protocol_failure_twice_goes_human_review_not_image_retry(tmp_path):
    provider = SequenceVisionProvider(
        [
            StructuredOutputProtocolError("SCHEMA_ECHO"),
            StructuredOutputProtocolError("MODEL_VALIDATION"),
        ]
    )
    evaluator = BEvaluator(provider)

    gate = evaluator.evaluate_production(_context(tmp_path))

    assert gate.decision is FinalDecision.NEEDS_HUMAN_REVIEW
    assert gate.failure_codes == [FailureCode.EVALUATOR_PROTOCOL_FAILURE]
    assert gate.retry_eligible is False
    assert gate.failure_class == "EVALUATOR_PROTOCOL"
    assert len(provider.calls) == 2
    assert "do not regenerate" in gate.repair_instruction.lower()
