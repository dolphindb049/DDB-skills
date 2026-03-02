from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build factor evaluation report from csv files")
    parser.add_argument("--factor", required=True, help="factor name")
    parser.add_argument("--daily", required=True, help="path of *_daily.csv")
    parser.add_argument("--summary", required=True, help="path of *_summary.csv")
    parser.add_argument("--out", required=True, help="output directory")
    return parser.parse_args()


def ensure_datetime(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col])
    return df


def plot_ic(daily: pd.DataFrame, out_dir: Path, factor: str) -> Path:
    fig, ax = plt.subplots(figsize=(10, 4))
    daily = ensure_datetime(daily, "trade_date")
    ax.plot(daily["trade_date"], daily["ic"], label="IC", linewidth=1.2)
    ax.axhline(0.0, color="gray", linestyle="--", linewidth=1)
    ax.set_title(f"{factor} - Daily IC")
    ax.set_xlabel("trade_date")
    ax.set_ylabel("IC")
    ax.legend()
    fig.tight_layout()
    p = out_dir / f"{factor}_ic.png"
    fig.savefig(p, dpi=160)
    plt.close(fig)
    return p


def plot_group_and_ls(daily: pd.DataFrame, out_dir: Path, factor: str) -> tuple[Path, Path]:
    daily = ensure_datetime(daily, "trade_date")

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    if "top_ret" in daily.columns:
        top_nav = (1 + daily["top_ret"].fillna(0.0)).cumprod()
        ax1.plot(daily["trade_date"], top_nav, label="Top NAV", linewidth=1.2)
    if "bottom_ret" in daily.columns:
        bottom_nav = (1 + daily["bottom_ret"].fillna(0.0)).cumprod()
        ax1.plot(daily["trade_date"], bottom_nav, label="Bottom NAV", linewidth=1.2)
    ax1.set_title(f"{factor} - Group NAV")
    ax1.legend()
    fig1.tight_layout()
    p1 = out_dir / f"{factor}_group_nav.png"
    fig1.savefig(p1, dpi=160)
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    if "ls_nav" in daily.columns:
        ax2.plot(daily["trade_date"], daily["ls_nav"], label="Long-Short NAV", linewidth=1.2)
    ax2.set_title(f"{factor} - Long/Short NAV")
    ax2.legend()
    fig2.tight_layout()
    p2 = out_dir / f"{factor}_ls_nav.png"
    fig2.savefig(p2, dpi=160)
    plt.close(fig2)
    return p1, p2


def build_markdown_report(
    factor: str,
    daily: pd.DataFrame,
    summary: pd.DataFrame,
    out_dir: Path,
    ic_fig: Path,
    group_fig: Path,
    ls_fig: Path,
) -> Path:
    latest = summary.iloc[0].to_dict()
    report_path = out_dir / f"{factor}_report.md"

    text = []
    text.append(f"# 因子评价报告：{factor}")
    text.append("")
    text.append(f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    text.append(f"- 样本点数：{len(daily)}")
    text.append("")
    text.append("## 关键指标")
    for key in ["mean_ic", "ic_ir", "ann_ls_ret", "ann_ls_vol", "sharpe_ls", "max_dd"]:
        if key in latest:
            text.append(f"- {key}: {latest[key]}")

    text.append("")
    text.append("## 图表")
    text.append(f"![IC]({ic_fig.name})")
    text.append(f"![Group NAV]({group_fig.name})")
    text.append(f"![LS NAV]({ls_fig.name})")
    text.append("")

    advice = "建议继续观察"
    mean_ic = float(latest.get("mean_ic", 0.0))
    sharpe = float(latest.get("sharpe_ls", 0.0))
    if mean_ic > 0.02 and sharpe > 0.8:
        advice = "建议进入候选因子池"
    if mean_ic < 0.0:
        advice = "不建议上线，需重构逻辑"

    text.append("## 结论")
    text.append(f"- 结论：{advice}")

    report_path.write_text("\n".join(text), encoding="utf-8")
    return report_path


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    daily = pd.read_csv(args.daily)
    summary = pd.read_csv(args.summary)

    if summary.empty:
        raise ValueError("summary csv is empty")

    ic_fig = plot_ic(daily, out_dir, args.factor)
    group_fig, ls_fig = plot_group_and_ls(daily, out_dir, args.factor)
    report = build_markdown_report(args.factor, daily, summary, out_dir, ic_fig, group_fig, ls_fig)
    print(f"report generated: {report}")


if __name__ == "__main__":
    main()
