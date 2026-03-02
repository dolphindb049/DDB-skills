# prepare_data_for_pricing：库表结构与工作流

## 1. 目标

把通联债券相关 API 数据整理为可定价的 DolphinDB 数据层，并跑通两条定价链路：
- Case1：`IRS曲线 -> bondPricer`
- Case2：`bondYieldCurveBuilder -> bondPricer`

数据库默认：`dfs://data_pricing_skill`

## 2. 库表分层

### 原始层（Raw）
- `raw_bond_info`：债券静态信息（起息、到期、票息、频率、类型）
- `raw_cfets_valuation`：CFETS估值（净价、YTM、久期、凸性）
- `raw_irs_curve`：IRS期限点（含 `curveDate`）
- `raw_ib_bond_market`：银行间行情样本

### 准备层（Prepared）
- `case2_bond_basket`：用于曲线反推的国债样本篮子
- `instrument_cache`：定价时的债券对象缓存（JSON）
- `curve_cache`：定价时的曲线对象缓存（JSON）

### 结果层（Result）
- `pricing_result_case1`：Case1定价结果（含Delta/Gamma等）
- `pricing_result_case2`：Case2定价结果

## 3. 脚本执行顺序

1) `scripts/10_probe_uqer_api.py`：探测API返回结构
2) `scripts/20_download_minimal_samples.py`：下载最小样本到 `reference/sample_data`
3) `scripts/30_create_pricing_schema.dos`：建库建表
4) `scripts/40_ingest_raw_to_ddb.py`：Python直连导入DFS
5) `scripts/50_run_case1_irs_pricing.dos`：运行 Case1
6) `scripts/60_run_case2_curve_bootstrap.dos`：运行 Case2
7) `scripts/70_generate_standard_report.py`：输出标准化报告

## 4. 输出物

- 数据：`pricing_result_case1` / `pricing_result_case2`
- 报告：`reference/reports/pricing_report_*.md`
- 图表（可选）：`reference/reports/case1_diff_*.png`、`case2_diff_*.png`

## 5. 新 Agent 复跑要点

- 先确认 `execute-dlang` 可用。
- 再执行建表 DOS，否则导入会报表不存在。
- 若 API 临时无数据，先换 `PRICING_DATE` 再跑下载脚本。
- 若要切换服务器，只改环境变量 `DDB_HOST/DDB_PORT/DDB_USER/DDB_PASSWORD`。
