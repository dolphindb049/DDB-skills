# 实战复现记录：波动率的波动率与投资者模糊性厌恶

## 1) 输入研报

- 文件：`reference/pdf-report/（5）波动率的波动率与投资者模糊性厌恶.pdf`
- 抽取文本：`reference/pdf-report/（5）波动率的波动率与投资者模糊性厌恶.extracted.txt`

## 2) 研报逻辑提炼

论文核心：先计算分钟级“波动率的波动率（模糊性）”，再构造“模糊金额比”“模糊数量比”“修正模糊价差”，最终合成“云开雾散”因子。

## 3) 环境探测与限制

通过 `practice_probe.dos` 与 `practice_probe_tables.dos` 实测：

- `dfs://day_factor` 不存在。
- 可用日频表：`dfs://stock_daily.stock_daily_prev`。
- `stockMinKSH` 库存在，但分钟表名不可直接解析。

因此本次先落地“日频代理版”因子，确保流程跑通并可复现。

## 4) 实跑因子（代理版）

因子名：`average_monthly_dazzling_volatility`

核心表达：

1. $r_{i,t}=\frac{close_{i,t}}{pre\_close_{i,t}}-1$
2. $\Delta V_{i,t}=vol_{i,t}-vol_{i,t-1}$
3. $surge_{i,t}=\mathbb{I}(\Delta V_{i,t}>MA_{20}(\Delta V)+STD_{20}(\Delta V))$
4. $vol5_{i,t}=STD_5(r_{i,t})$，$vov5_{i,t}=STD_5(vol5_{i,t})$
5. $dazzle_{i,t}=MA_{20}(surge_{i,t}\cdot vov5_{i,t})$
6. $mod_{i,t}=|dazzle_{i,t}-\overline{dazzle}_{\cdot,t}|$
7. $factor_{i,t}=MA_{20}(mod_{i,t})$

实现脚本：`scripts/practice_run_average_monthly_dazzling_volatility.dos`

## 5) 运行命令

```powershell
uv run .github/skills/execute-dlang/scripts/ddb_runner/execute.py .github/skills/research-ddb/scripts/practice_run_average_monthly_dazzling_volatility.dos
```

## 6) 实际运行结果（2023-02-06 ~ 2025-12-03）

- 状态：`success`
- 样本行数：`3,617,710`
- 分组统计：5组分布约均衡，每组约 20%
- IC 分析：
  - 1D: IC Mean = -0.002484, IC Std = 0.035301, IC Risk Adjusted = -0.070365
  - 5D: IC Mean = -0.004779, IC Std = 0.032605, IC Risk Adjusted = -0.146562
  - 10D: IC Mean = -0.005827, IC Std = 0.032532, IC Risk Adjusted = -0.179114
- Top-Bottom 平均收益差（bps）：
  - 1D: 7.7660
  - 5D: -7.1654
  - 10D: -7.7000

## 7) 可复用踩坑经验

1. **路径漂移**：不要写死 `dfs://day_factor`，先探测可用库再落公式。
2. **命令行引号**：PowerShell 下复杂 `-c` 极易失败，优先脚本文件。
3. **分组越界**：`quantileSeries` 分桶要做上界截断（防止出现第 6 组）。
4. **分钟表不可见时**：必须给出可运行代理版，保证流程不断裂。
