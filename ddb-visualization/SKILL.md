---
name: ddb-visualization
description: DolphinDB 因子评价结果可视化技能。使用 Python 将评价 JSON 渲染为可交互单页 HTML 仪表板。
license: MIT
metadata:
  author: ddb-user
  version: "1.0.0"
  tags: ["visualization", "plotly", "factor", "dashboard"]
---

# DDB Visualization

来源参考（find-skills 实测候选）：

- `vamseeachanta/workspace-hub@plotly`
- skills.sh: https://skills.sh/vamseeachanta/workspace-hub/plotly

## 单一职责

只做可视化渲染，不负责因子计算。

## 输入

- 指标 JSON（summary、desc_stats、ic_analysis、returns_analysis）

## DDB 因子场景适配

- 面向“分层统计 + IC + Top-Bottom Spread”单页看板。
- 输出为离线 HTML，适合直接归档到因子研究结果目录。
- 可通过 `python -m http.server` 发布为本地 URL。

## 输出

- 单页 HTML Dashboard

## 使用方式

```powershell
python .github/skills/ddb-visualization/scripts/render_factor_dashboard.py --input <metrics.json> --out <report.html>
```
