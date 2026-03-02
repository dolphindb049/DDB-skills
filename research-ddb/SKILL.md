---
name: research-ddb
description: 研报复现专家技能。将 PDF 研报转成可执行因子：提取金融逻辑、公式化、DolphinDB 试错落地、统一因子表、评价可视化与报告输出。
license: MIT
metadata:
  author: ddb-user
  version: "1.0.0"
  tags: ["factor", "research", "dolphindb", "backtest", "report"]
---

# Research-to-Factor for DolphinDB

本技能用于指导一个全新的 AI Agent 完成完整“研报复现”流程：

1. 读取 PDF 研报并抽取金融逻辑。
2. 将逻辑写成数学表达式并生成因子卡片。
3. 在 DolphinDB 中对公式反复试错，直到可计算成功。
4. 产出可直接执行的 `.dos` 脚本并写入统一因子表。
5. 运行因子评价。
6. 用 Python 自动出图并输出最终报告。

## 触发条件

当用户提出以下需求时触发：

- 给定研报/PDF，复现其中因子。
- 生成“因子卡片（数学表达式 + 含义）”。
- 在 `dfs://day_factor` 上试算并落库。
- 因子评价与可视化报告自动化。

## 默认数据与目标

- 数据源：`dfs://day_factor` / `stock_daily_prev`
- 目标：统一因子表（建议 `stock_factor_unified`）
- 默认服务：`http://183.134.101.137:8657`

## 技能结构

```text
research-ddb/
├── SKILL.md
├── reference/
│   ├── WORKFLOW.md
│   ├── SUBAGENT_PROMPTS.md
│   └── QUALITY_GATES.md
├── templates/
│   └── factor_card_template.md
├── examples/
│   └── factor_card_example_mom20.md
├── scripts/
│   ├── 10_factor_compute_template.dos
│   ├── 20_retry_validate_factor.dos
│   ├── 30_merge_to_unified_table.dos
│   ├── 40_evaluate_factor.dos
│   ├── 50_export_eval_results.dos
│   ├── build_factor_report.py
│   └── requirements.txt
└── outputs/
    └── .gitkeep
```

## 执行流程（必须按顺序）

1. 按 `reference/WORKFLOW.md` 拆解研报。
2. 每个候选因子先写一张卡片（基于 `templates/factor_card_template.md`）。
3. 基于 `scripts/10_factor_compute_template.dos` 生成具体因子脚本。
4. 用 `scripts/20_retry_validate_factor.dos` 循环试错。
5. 成功后执行 `scripts/30_merge_to_unified_table.dos` 入统一因子表。
6. 执行 `scripts/40_evaluate_factor.dos` 计算 IC/分层收益等指标。
7. 执行 `scripts/50_export_eval_results.dos` 持久化评价结果。
8. 用 `python scripts/build_factor_report.py ...` 生成图表与报告。

## 并行子 Agent 建议

可并行启动多个子 Agent（例如使用 Gemini 3.1）执行：

- Agent A：从 PDF 抽取逻辑并提纯候选因子定义。
- Agent B：将候选因子转成严格数学表达式并补齐变量定义。
- Agent C：生成与修复 DolphinDB 公式实现。
- Agent D：跑评价与报告，核对质量门禁。

统一汇总负责人只接受满足 `reference/QUALITY_GATES.md` 的结果。

## 成功判定

满足以下全部条件才算完成：

- 每个因子都有卡片，且包含数学表达式与金融含义。
- 因子 `.dos` 脚本可直接拉数计算并落入统一表。
- 因子评价表有结果（IC、ICIR、分组收益、回撤等）。
- Python 报告输出成功（含图与摘要）。
- 全流程可由新 AI 按文档复现。