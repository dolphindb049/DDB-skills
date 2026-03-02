#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from pricing_common import connect_ddb, load_config


def _safe_float(series: pd.Series):
    return pd.to_numeric(series, errors="coerce")


def _save_plot(case_df: pd.DataFrame, output_png: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    if case_df.empty:
        return

    draw_df = case_df.copy()
    draw_df["pricingDiff"] = _safe_float(draw_df["npv"]) - _safe_float(draw_df["cfetsNetPx"])
    draw_df = draw_df.sort_values("ticker")

    plt.figure(figsize=(9, 4.5))
    plt.bar(draw_df["ticker"].astype(str), draw_df["pricingDiff"].astype(float))
    plt.axhline(0.0, color="black", linewidth=1)
    plt.title("Case Pricing Diff (NPV - CFETS NetPx)")
    plt.xlabel("Ticker")
    plt.ylabel("Price Diff")
    plt.tight_layout()
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=140)
    plt.close()


def _summary_block(case_df: pd.DataFrame, case_name: str) -> str:
    if case_df.empty:
        return f"### {case_name}\n\n- 无结果数据。\n"

    temp = case_df.copy()
    temp["npv"] = _safe_float(temp["npv"])
    temp["cfetsNetPx"] = _safe_float(temp["cfetsNetPx"])
    temp["absDiff"] = (temp["npv"] - temp["cfetsNetPx"]).abs()

    mae = temp["absDiff"].mean()
    p95 = temp["absDiff"].quantile(0.95)
    max_row = temp.sort_values("absDiff", ascending=False).head(1)
    max_ticker = max_row["ticker"].iloc[0] if not max_row.empty else "-"
    max_diff = max_row["absDiff"].iloc[0] if not max_row.empty else float("nan")

    top_lines = []
    for _, row in temp.sort_values("absDiff", ascending=False).head(5).iterrows():
        top_lines.append(
            f"  - {row['ticker']}: npv={row['npv']:.6f}, cfetsNetPx={row['cfetsNetPx']:.6f}, absDiff={row['absDiff']:.6f}"
        )

    block = [
        f"### {case_name}",
        "",
        f"- 样本数: {len(temp)}",
        f"- 平均绝对误差(MAE): {mae:.6f}",
        f"- 95分位绝对误差(P95): {p95:.6f}",
        f"- 最大偏差: {max_ticker} ({max_diff:.6f})",
        "- 偏差Top5:",
        *top_lines,
        "",
    ]
    return "\n".join(block)


def main() -> None:
    cfg = load_config()
    session = connect_ddb(cfg)

    counts = session.run(
        f'''
select * from (
    select "raw_bond_info" as tableName, count(*) as rows from loadTable("{cfg.db_path}", "raw_bond_info")
    union all
    select "raw_cfets_valuation" as tableName, count(*) as rows from loadTable("{cfg.db_path}", "raw_cfets_valuation")
    union all
    select "raw_irs_curve" as tableName, count(*) as rows from loadTable("{cfg.db_path}", "raw_irs_curve")
    union all
    select "raw_ib_bond_market" as tableName, count(*) as rows from loadTable("{cfg.db_path}", "raw_ib_bond_market")
    union all
    select "case2_bond_basket" as tableName, count(*) as rows from loadTable("{cfg.db_path}", "case2_bond_basket")
    union all
    select "pricing_result_case1" as tableName, count(*) as rows from loadTable("{cfg.db_path}", "pricing_result_case1")
    union all
    select "pricing_result_case2" as tableName, count(*) as rows from loadTable("{cfg.db_path}", "pricing_result_case2")
)
'''
    )

    case1 = session.run(f'select * from loadTable("{cfg.db_path}", "pricing_result_case1") order by pricingDate, ticker')
    case2 = session.run(f'select * from loadTable("{cfg.db_path}", "pricing_result_case2") order by pricingDate, ticker')

    report_dir = Path(__file__).resolve().parents[1] / "reference" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_md = report_dir / f"pricing_report_{stamp}.md"
    case1_png = report_dir / f"case1_diff_{stamp}.png"
    case2_png = report_dir / f"case2_diff_{stamp}.png"

    _save_plot(case1, case1_png)
    _save_plot(case2, case2_png)

    table_lines = []
    if isinstance(counts, pd.DataFrame) and not counts.empty:
        for _, row in counts.iterrows():
            table_lines.append(f"- {row['tableName']}: {int(row['rows'])}")

    content = f"""# 标准化定价报告

- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 数据库: {cfg.db_path}
- 定价日期参数: {cfg.pricing_date}

## 一、数据准备状态
{chr(10).join(table_lines) if table_lines else '- 无计数信息'}

## 二、定价结果对照
{_summary_block(case1, 'Case 1 - IRS曲线 + bondPricer')}
{_summary_block(case2, 'Case 2 - bondYieldCurveBuilder + bondPricer')}

## 三、业务启示（模板）
- 估值偏差集中在久期更长或票息特征更特殊的券种，可优先补充对应期限段曲线点或流动性修正。
- 若 Case2（国债收益率曲线反推）较 Case1（IRS贴现曲线）偏差更小，说明同类券收益率曲线对该样本更匹配。
- 若两案例均存在系统性高估/低估，优先排查：报价口径（净价/全价）、曲线频率、债券频率映射、定价日一致性。

## 四、可视化输出
- Case1图: {case1_png.name if case1_png.exists() else '未生成（matplotlib不可用）'}
- Case2图: {case2_png.name if case2_png.exists() else '未生成（matplotlib不可用）'}
"""

    report_md.write_text(content, encoding="utf-8")
    print(f"report saved: {report_md}")
    if case1_png.exists():
        print(f"figure saved: {case1_png}")
    if case2_png.exists():
        print(f"figure saved: {case2_png}")


if __name__ == "__main__":
    main()
