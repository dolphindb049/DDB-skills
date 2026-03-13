---
name: research-ddb
description: 研报分析通用技能。把研报文本转为多因子资产包（因子描述、数学公式、DolphinDB 代码），用于后续评价与可视化。
license: MIT
metadata:
  author: ddb-user
  version: "2.0.0"
  tags: ["factor", "research", "dolphindb", "multi-factor"]
  dependencies: [".github/skills/pdf", ".github/skills/execute-dlang", ".github/skills/ddb-data-analysis"]
---

# Research Analysis for DolphinDB

本技能只做“研报分析”本身，不做页面渲染。

## 输出资产（每个因子必须有）

1. 因子描述（金融含义与假设）
2. 数学公式（KaTeX）
3. 变量定义与边界处理
4. 最终 DolphinDB 代码（`.dos`）

一个研报可生成多个因子，统一输出到同一资产包目录。

## 目录（精简）

```text
research-ddb/
├── SKILL.md
└── modules/
    └── research-analysis/
        ├── SKILL.md
        └── scripts/
            └── analyze_and_render.py
```

## 使用方式

```powershell
python .github/skills/research-ddb/modules/research-analysis/scripts/analyze_and_render.py --text <report.txt> --factor-spec <factor_spec.json> --outdir <out_dir>
```

`factor_spec.json` 支持多因子：

```json
{
  "factors": [
    {
      "name": "factor_a",
      "description": "...",
      "formula": "...",
      "variables": [{"name": "x", "meaning": "..."}],
      "ddb_code": "select ..."
    }
  ]
}
```

## 与可视化技能分工

- 本技能：只负责“分析产物”（卡片+公式+代码）。
- `ddb-visualization`：负责表格/图表/页面渲染（包括 FICC 定价展示）。