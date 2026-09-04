from pathlib import Path

from PIL import Image

from pp_food_runtime.review_sheet import ReviewPanel, create_review_sheet


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
