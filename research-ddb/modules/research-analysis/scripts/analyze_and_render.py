from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="research-ddb internal analysis module")
    parser.add_argument("--text", required=True)
    parser.add_argument("--factor", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--metrics")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    txt = Path(args.text).read_text(encoding="utf-8", errors="ignore")
    logic = txt.split("投资要点", 1)[-1][:700] if "投资要点" in txt else "请补充金融逻辑"
    card = f"# 因子卡片：{args.factor}\n\n## 金融含义\n{logic}\n\n## 数学表达式\n$$\n请填写可执行表达式\n$$\n"
    card_path = outdir / f"factor_card_{args.factor}.md"
    card_path.write_text(card, encoding="utf-8")
    print(f"factor card generated: {card_path}")

    if args.metrics:
        payload = json.loads(Path(args.metrics).read_text(encoding="utf-8"))
        summary = payload["summary"]
        html = f"<html><head><meta charset='utf-8'/><script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script></head><body><h1>{summary['factor']}</h1><p>{summary['status']}</p></body></html>"
        html_path = outdir / f"{args.factor}_report.html"
        html_path.write_text(html, encoding="utf-8")
        print(f"web report generated: {html_path}")


if __name__ == "__main__":
    main()
