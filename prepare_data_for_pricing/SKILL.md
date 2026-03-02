````skill
---
name: prepare_data_for_pricing
description: 债券定价前的数据准备与双案例验证技能：API探测、样本下载、建库建表、导入、曲线构建与标准化报告输出。
license: MIT
metadata:
  author: jrzhang
  version: "1.0.0"
  tags: ["DolphinDB", "Bond", "Pricing", "UQER", "execute-dlang", "report"]
---

# prepare_data_for_pricing

这个 skill 的定位不是“最终策略定价系统”，而是**定价前准备与校验基线**：
- 从 API 拿到可定价数据
- 在 DDB 中落成规范库表
- 跑通两条可复现定价链路
- 产出标准化报告，方便新 agent 直接复跑与交接

## 目录（精简）

```text
prepare_data_for_pricing/
├── SKILL.md
├── reference/
│   ├── API文档/
│   ├── API_CATALOG.md
│   ├── WORKFLOW.md
│   ├── TABLE_SCHEMA_AND_WORKFLOW.md
│   └── sample_data/
└── scripts/
    ├── requirements.txt
    ├── pricing_common.py
    ├── 10_probe_uqer_api.py
    ├── 20_download_minimal_samples.py
    ├── 30_create_pricing_schema.dos
    ├── 40_ingest_raw_to_ddb.py
    ├── 50_run_case1_irs_pricing.dos
    ├── 60_run_case2_curve_bootstrap.dos
    └── 70_generate_standard_report.py
```

## 依赖关系

### 必需
- `execute-dlang`：执行 `.dos` 脚本（建表/定价）
- Python 依赖：`dolphindb`, `requests`, `pandas`, `matplotlib`

### 建议（可选）
- `ddb-deployment-skill`：新机器部署或排障时先打通 DDB 服务
- `pricing`：如果你已有“基于现有库表结构”的完整定价流水线，可在本 skill 完成后接续使用
- `find-skills`：扩展可视化、报告或数据发现能力时快速检索其他 skill

## 一次跑通（新 agent 最小命令）

```bash
cd /hdd/hdd9/jrzhang

# 0) 依赖
/home/jrzhang/miniconda3/bin/python -m pip install -r .github/skills/prepare_data_for_pricing/scripts/requirements.txt
/home/jrzhang/miniconda3/bin/python -m pip install python-dotenv

# 1) 探测与下载
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/10_probe_uqer_api.py
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/20_download_minimal_samples.py

# 2) 建表
/home/jrzhang/miniconda3/bin/python .github/skills/execute-dlang/scripts/ddb_runner/execute.py \
  .github/skills/prepare_data_for_pricing/scripts/30_create_pricing_schema.dos \
  --host 127.0.0.1 --port 8848 --user admin --password 123456

# 3) 导入
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/40_ingest_raw_to_ddb.py

# 4) 案例1 + 案例2
/home/jrzhang/miniconda3/bin/python .github/skills/execute-dlang/scripts/ddb_runner/execute.py \
  .github/skills/prepare_data_for_pricing/scripts/50_run_case1_irs_pricing.dos \
  --host 127.0.0.1 --port 8848 --user admin --password 123456

/home/jrzhang/miniconda3/bin/python .github/skills/execute-dlang/scripts/ddb_runner/execute.py \
  .github/skills/prepare_data_for_pricing/scripts/60_run_case2_curve_bootstrap.dos \
  --host 127.0.0.1 --port 8848 --user admin --password 123456

# 5) 标准报告
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/70_generate_standard_report.py
```

## 你会得到什么

- 数据库：`dfs://data_pricing_skill`
- 结果表：
  - `pricing_result_case1`
  - `pricing_result_case2`
- 报告文件：`reference/reports/pricing_report_*.md`
- 可视化（若 matplotlib 可用）：`reference/reports/case1_diff_*.png`、`case2_diff_*.png`

## 对业务的直接含义（报告会给出）

- 模型价格（NPV）与 CFETS 净价偏差是否可接受
- 贴现曲线（IRS）与同类券曲线（bondYieldCurveBuilder）哪个更贴合样本
- 偏差最大的券种与可能原因（期限段、票息频率、报价口径）

## 参考文档

- 流程：`reference/WORKFLOW.md`
- 库表结构：`reference/TABLE_SCHEMA_AND_WORKFLOW.md`
- API字典：`reference/API_CATALOG.md`
- 联合调试：`reference/COMPATIBILITY_WITH_PRICING_SKILL.md`
- 函数文档：
  - `bondPricer`: https://docs.dolphindb.cn/zh/funcs/b/bondPricer.html
  - `bondYieldCurveBuilder`: https://docs.dolphindb.cn/zh/funcs/b/bondYieldCurveBuilder.html

````
