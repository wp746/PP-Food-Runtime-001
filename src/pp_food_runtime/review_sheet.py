from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


@dataclass(frozen=True)
class ReviewPanel:
    label: str
    path: Path


def _font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size, index=1 if bold and path.endswith(".ttc") else 0)
        except OSError:
            continue
    return ImageFont.load_default()


def create_review_sheet(
    panels: list[ReviewPanel],
    metrics: dict[str, float],
    decision: str,
    output_path: Path,
    *,
    title: str = "PP FOOD VALIDATION",
    candidate_scores: dict[str, float] | None = None,
) -> Path:
    if len(panels) != 5:
        raise ValueError("review sheet requires SOURCE, STAGE A, PRIMARY, CHALLENGER, and GOLDEN")
    panel_width, image_height = 360, 640
    margin, gap, label_height, footer_height = 24, 12, 54, 190
    width = margin * 2 + panel_width * 5 + gap * 4
    height = margin * 2 + label_height + image_height + footer_height
    canvas = Image.new("RGB", (width, height), "#11100e")
    draw = ImageDraw.Draw(canvas)
    label_font = _font(24, bold=True)
    metric_font = _font(22)
    title_font = _font(30, bold=True)
    for index, panel in enumerate(panels):
        x = margin + index * (panel_width + gap)
        draw.rectangle((x, margin, x + panel_width, margin + label_height - 6), fill="#26231f")
        draw.text((x + 14, margin + 9), panel.label, font=label_font, fill="#f7f1e7")
        with Image.open(panel.path) as source:
            image = ImageOps.contain(source.convert("RGB"), (panel_width, image_height), Image.Resampling.LANCZOS)
        frame = Image.new("RGB", (panel_width, image_height), "#050505")
        frame.paste(image, ((panel_width - image.width) // 2, (image_height - image.height) // 2))
        canvas.paste(frame, (x, margin + label_height))
    footer_top = margin + label_height + image_height
    draw.rectangle((0, footer_top, width, height), fill="#191714")
    draw.text((margin, footer_top + 20), title, font=title_font, fill="#f7f1e7")
    metric_line = "   |   ".join(f"{name} {value:.1f}" for name, value in metrics.items())
    draw.text((margin, footer_top + 72), metric_line, font=metric_font, fill="#ded4c3")
    score_line = ""
    if candidate_scores:
        score_line = "   ·   ".join(f"{name.upper()} {score:.2f}" for name, score in candidate_scores.items())
    decision_color = "#72d39a" if decision == "PASS" else "#ffb35c"
    draw.text((margin, footer_top + 121), score_line, font=metric_font, fill="#bfb3a2")
    draw.text((width - 390, footer_top + 112), f"DECISION  {decision}", font=title_font, fill=decision_color)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="JPEG", quality=92, optimize=True)
    return output_path.resolve()


def create_from_run(case: str, run_dir: Path, output: Path) -> Path:
    run_dir = Path(run_dir)
    output = Path(output)
    source = next((run_dir / "input").glob("source.*"))
    stage_a = next((run_dir / "input").glob("stage-a.*"))
    golden = next((run_dir / "input").glob(f"golden-{case}.*"), None)
    golden_label = "GOLDEN"
    if golden is None:
        output.parent.mkdir(parents=True, exist_ok=True)
        golden = output.parent / f".{case}-golden-not-retrieved.png"
        Image.new("RGB", (360, 640), "#26231f").save(golden)
        golden_label = "GOLDEN NOT RETRIEVED"
    primary_eval = json.loads((run_dir / "eval" / "primary.json").read_text(encoding="utf-8"))
    challenger_eval = json.loads((run_dir / "eval" / "challenger.json").read_text(encoding="utf-8"))
    decision = json.loads((run_dir / "final" / "decision.json").read_text(encoding="utf-8"))["decision"]
    vector = primary_eval["golden_vector"]
    metrics = {
        "Product Hero": vector["product_hero_strength"],
        "Headline": vector["headline_aggression"],
        "Symbiosis": vector["typography_product_symbiosis"],
        "Big Idea": vector["one_big_idea_clarity"],
        "Depth": vector["compositional_depth_tension"],
        "Category": vector["category_inevitability"],
        "Info": vector["information_density_control"],
        "Finish": vector["commercial_finish"],
    }
    return create_review_sheet(
        [
            ReviewPanel("SOURCE", source),
            ReviewPanel("STAGE A", stage_a),
            ReviewPanel("PRIMARY", run_dir / "primary" / "image.png"),
            ReviewPanel("CHALLENGER", run_dir / "challenger" / "image.png"),
            ReviewPanel(golden_label, golden),
        ],
        metrics,
        "RETRY" if decision == "NO_QUALIFIED_WINNER" else decision,
        output,
        title=f"PP FOOD VALIDATION  /  {case}",
        candidate_scores={
            "primary": primary_eval["golden_vector"]["weighted_score"],
            "challenger": challenger_eval["golden_vector"]["weighted_score"],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(create_from_run(args.case, args.run_dir, args.output))


if __name__ == "__main__":
    main()
