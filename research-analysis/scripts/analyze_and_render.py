from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Research analysis: factor card + single-page report")
    parser.add_argument("--text", required=True, help="report extracted txt file")
    parser.add_argument("--factor", required=True, help="factor name")
    parser.add_argument("--outdir", required=True, help="output directory")
    parser.add_argument("--metrics", help="metrics json for html report")
    return parser.parse_args()


def build_factor_card(text: str, factor: str) -> str:
    logic = ""
    if "投资要点" in text:
        logic = text.split("投资要点", 1)[-1][:700].strip()
    if not logic:
        logic = "请从研报中补充金融逻辑。"

    lines = [
        f"# 因子卡片：{factor}",
        "",
        "## 金融含义",
        logic,
        "",
        "## 数学表达式",
        "$$",
        "请填写可执行数学表达式",
        "$$",
        "",
        "## 变量定义",
        "- 变量1：含义",
        "- 变量2：含义",
        "",
        "## 边界处理",
        "- 缺失值处理",
        "- 除零处理",
        "- 极值处理",
    ]
    return "\n".join(lines)


def table_html(headers: list[str], rows: list[list]) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = ""
    for row in rows:
        tr += "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


def build_html(payload: dict) -> str:
    summary = payload["summary"]
    desc = payload.get("desc_stats", [])
    ic = payload.get("ic_analysis", [])
    ret = payload.get("returns_analysis", [])

    return f"""
<!doctype html>
<html><head>
<meta charset='utf-8'/>
<title>{summary['factor']} Report</title>
<script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>
<style>
body {{font-family: Arial; margin: 24px;}}
table {{border-collapse: collapse; width: 100%; margin-bottom: 16px;}}
th,td {{border:1px solid #ddd; padding:8px; font-size:13px;}}
th {{background:#f3f3f3;}}
</style>
</head><body>
<h1>因子评价单页报告</h1>
<p><b>状态:</b> {summary['status']} | <b>因子:</b> {summary['factor']} | <b>区间:</b> {summary['start_date']} ~ {summary['end_date']}</p>
<h2>分层统计</h2>
{table_html(["quantile","min","max","std","count","pct"], [[r['factor_quantile'], r['min_value'], r['max_value'], r['std_value'], r['cnt'], r['pct']] for r in desc])}
<h2>IC分析</h2>
{table_html(["horizon","IC_Mean","IC_Std","IC_Risk_Adjusted","IC_t_stat"], [[r['horizon'], r['IC_Mean'], r['IC_Std'], r['IC_Risk_Adjusted'], r['IC_t_stat']] for r in ic])}
<h2>收益分析（bps）</h2>
{table_html(["metric","1D","5D","10D"], [[r['metric'], r['forward_returns_1D'], r['forward_returns_5D'], r['forward_returns_10D']] for r in ret])}
<div id='ic' style='height:300px;'></div>
<script>
const icLabels = {json.dumps([x['horizon'] for x in ic])};
const icVals = {json.dumps([x['IC_Mean'] for x in ic])};
Plotly.newPlot('ic', [{{x:icLabels, y:icVals, type:'bar'}}], {{title:'IC Mean'}});
</script>
</body></html>
"""


def main() -> None:
    args = parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    text = Path(args.text).read_text(encoding="utf-8", errors="ignore")
    card = build_factor_card(text, args.factor)
    card_path = outdir / f"factor_card_{args.factor}.md"
    card_path.write_text(card, encoding="utf-8")

    print(f"factor card generated: {card_path}")

    if args.metrics:
        payload = json.loads(Path(args.metrics).read_text(encoding="utf-8"))
        html = build_html(payload)
        html_path = outdir / f"{args.factor}_report.html"
        html_path.write_text(html, encoding="utf-8")
        print(f"web report generated: {html_path}")


if __name__ == "__main__":
    main()
