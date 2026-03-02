---
name: research-analysis
description: 研报分析通用技能。统一完成文本解析、因子卡片生成、评价数据整合、单页网页报告输出。
license: MIT
metadata:
  author: ddb-user
  version: "1.0.0"
  tags: ["research", "factor-card", "report", "html", "analysis"]
---

# Research Analysis Skill

> Deprecated alias：已归并到 `.github/skills/research-ddb/modules/research-analysis`。
> 建议直接使用 `research-ddb` 主技能与其内部模块。

## 单一职责

以“研报分析”为核心能力，一站式完成：

1. 文本提取后的结构化因子卡片。
2. 评价 JSON 到单页 HTML 报告。
3. 输出可发布的本地网页文件。

## 输入

- `--text`：研报文本文件（txt）
- `--factor`：因子名
- `--metrics`：评价指标 JSON（可选）
- `--outdir`：输出目录

## 输出

- `factor_card_<factor>.md`
- `<factor>_report.html`（当提供 metrics 时）

## 快速使用

```powershell
python .github/skills/research-analysis/scripts/analyze_and_render.py --text <report.txt> --factor <factor_name> --metrics <metrics.json> --outdir <out_dir>
```
