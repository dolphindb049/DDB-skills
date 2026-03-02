---
name: research-ddb
description: 研报复现专家技能。将 PDF 研报转成可执行因子：提取金融逻辑、公式化、DolphinDB 试错落地、统一因子表、评价可视化与报告输出。
license: MIT
metadata:
  author: ddb-user
  version: "1.0.0"
  tags: ["factor", "research", "dolphindb", "backtest", "report"]
  dependencies: [".github/skills/pdf", ".github/skills/execute-dlang", ".github/skills/ddb-data-analysis", ".github/skills/ddb-visualization"]
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

## 技能结构（目录单一职责）

```text
research-ddb/
├── SKILL.md
├── reference/
│   ├── WORKFLOW.md
│   ├── SUBAGENT_PROMPTS.md
│   └── QUALITY_GATES.md
│   └── practice_case_vol_of_vol.md
├── templates/
│   └── factor_card_template.md
├── examples/
│   └── factor_card_example_mom20.md
├── scripts/
│   ├── probe/      # 只负责库表与环境探测
│   ├── factor/     # 只负责因子计算
│   ├── eval/       # 只负责因子评价
│   └── report/     # 只负责报告渲染与发布
├── legacy_scripts/ # 历史脚本，保留兼容
└── outputs/
    └── .gitkeep
```

## 执行流程（Skill 与 Agent 分层）

- Skill 层（通用、不随任务变化）：由 `modules/research-analysis` 负责公式抽取+报告；由 `ddb-visualization` 负责看板渲染。
- Agent 层（任务化、随目标变化）：指定某篇研报、指定因子、指定输出路径。

执行步骤（agent 编排时）：

1. 按 `reference/WORKFLOW.md` 拆解研报。
2. 每个候选因子先写一张卡片（基于 `templates/factor_card_template.md`）。
3. 在 `scripts/factor/` 生成具体因子脚本。
4. 在 `scripts/eval/` 执行评价脚本。
5. 在 `scripts/report/` 渲染单页 HTML 并输出链接。

## 实战案例（已跑通）

研报：`reference/pdf-report/（5）波动率的波动率与投资者模糊性厌恶.pdf`

对应脚本：

- 环境探测：`scripts/practice_probe.dos`
- 表结构探测：`scripts/practice_probe_tables.dos`
- 日频代理因子实跑：`scripts/practice_run_average_monthly_dazzling_volatility.dos`

执行命令：

```powershell
uv run .github/skills/execute-dlang/scripts/ddb_runner/execute.py .github/skills/research-ddb/scripts/practice_run_average_monthly_dazzling_volatility.dos
```

本次实跑结论见：`reference/practice_case_vol_of_vol.md`

## 关键排障结论（来自实战）

1. 不能假设数据库路径固定。示例环境中 `dfs://day_factor` 不存在，而可用的是 `dfs://stock_daily.stock_daily_prev`。
2. PowerShell 下 `-c` 代码字符串容易被引号吞噬，优先使用 `.dos` 文件执行。
3. `quantileSeries + asof + 1` 可能出现超边界分组（第 6 组），要强制截断到 1~5。
4. 分钟库存在但表名不可直接推断时，必须给出降级方案（先跑日频代理）并在因子卡片标明“近似实现”。

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