from pathlib import Path

from PIL import Image

from pp_food_runtime.review_sheet import ReviewPanel, create_from_run, create_review_sheet


def test_review_sheet_contains_five_panels_and_footer(tmp_path):
    panels = []
    for index, label in enumerate(("SOURCE", "STAGE A", "PRIMARY", "CHALLENGER", "GOLDEN")):
        path = tmp_path / f"{index}.png"
        Image.new("RGB", (90, 160), (index * 30, 80, 120)).save(path)
        panels.append(ReviewPanel(label=label, path=path))
    output = create_review_sheet(
        panels,
        {"Product Hero": 9.0, "Headline": 8.8, "Finish": 9.0},
        "RETRY",
        tmp_path / "review.jpg",
    )
    with Image.open(output) as image:
        assert image.width > image.height
        assert image.height >= 500


def test_create_from_run_handles_missing_case_golden_with_placeholder(tmp_path):
    run_dir = tmp_path / "run"
    for folder in ("input", "primary", "challenger", "eval", "final"):
        (run_dir / folder).mkdir(parents=True, exist_ok=True)
    for path, color in [
        (run_dir / "input" / "source.jpg", "red"),
        (run_dir / "input" / "stage-a.png", "orange"),
        (run_dir / "primary" / "image.png", "yellow"),
        (run_dir / "challenger" / "image.png", "green"),
    ]:
        Image.new("RGB", (90, 160), color).save(path)
    vector = {
        "product_hero_strength": 9.0,
        "headline_aggression": 9.0,
        "typography_product_symbiosis": 9.0,
        "one_big_idea_clarity": 9.0,
        "compositional_depth_tension": 9.0,
        "category_inevitability": 9.0,
        "information_density_control": 9.0,
        "commercial_finish": 9.0,
        "weighted_score": 9.0,
    }
    import json

    (run_dir / "eval" / "primary.json").write_text(
        json.dumps({"golden_vector": vector}), encoding="utf-8"
    )
    (run_dir / "eval" / "challenger.json").write_text(
        json.dumps({"golden_vector": vector}), encoding="utf-8"
    )
    (run_dir / "final" / "decision.json").write_text(
        json.dumps({"decision": "NO_QUALIFIED_WINNER"}), encoding="utf-8"
    )

    output = create_from_run("S02", run_dir, tmp_path / "review.jpg")

    assert output.is_file()
