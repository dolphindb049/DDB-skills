# 与 pricing skill 的联合调试

## 目标

- 先用 `prepare_data_for_pricing` 做数据准备与双案例验收。
- 再将结果或中间表映射给 `pricing` skill 的生产化流程。

## 建议顺序

1. 运行本 skill 全流程，确认：
   - `pricing_result_case1` 有数据
   - `pricing_result_case2` 有数据
   - 标准报告已生成
2. 再运行 `pricing` skill 中的发现/建模/批量定价脚本。

## 表层对齐建议

- 本 skill 原始层：
  - `raw_bond_info`, `raw_cfets_valuation`, `raw_irs_curve`, `raw_ib_bond_market`
- 本 skill 结果层：
  - `pricing_result_case1`, `pricing_result_case2`

当 `pricing` skill 需要更高频或更全量样本时，可复用本 skill 的下载与导入脚本，只替换：
- `PRICING_DATE`
- `PRICING_TICKERS`
- `DDB_DB_PATH`

## 常见不通点

- 服务器/端口不一致：统一 `DDB_HOST/DDB_PORT`。
- 库路径不一致：统一 `DDB_DB_PATH` 或在脚本中显式传入。
- 频率映射差异：检查 `cpnFreqCD -> frequency` 映射是否与目标模型一致。
- 报价口径差异：确认使用净价、全价还是YTM作为对照基准。
