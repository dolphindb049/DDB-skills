<<<<<<< HEAD
# FICC 债券标准化参考

本技能聚焦债券 `Instrument` 与 `IrYieldCurve` 两张标准表，按 `parseInstrument` 与 `parseMktData` 字段契约建模。

当前支持两类来源：

- 债券 API 原始库：`dfs://ficc_api_pdf_2026`
- 上清所曲线原始库：`dfs://ficc_curve_raw_2026`
  - 持久化预处理表：`curve_shch_yield_prepare`（`dates/values` 字符串聚合）

## 文件说明

- `STANDARD_DICTIONARY.md`
  - 中文数据字典（必填/可选/条件必填 + 典型源字段）

## 执行脚本（位于 scripts 目录）

1. `01_create_standard_schema.dos`：建标准表与映射表；按 `curve_shch_yield_raw` 动态重建 `curve_shch_yield_prepare`（只额外带 `dates/values`）
2. `03_build_field_mapping.dos`：构建源字段到标准字段映射表
3. `04a_raw_to_prepare.dos`：执行 `curve_shch_yield_raw -> curve_shch_yield_prepare`（仅聚合 `dates/values`）
4. `04_transform_to_standard.dos`：执行 `curve_shch_yield_prepare -> MarketData` 映射写入

## 验收口径

- `std_instrument_bond` 与 `std_market_curve` 有数据；
- `std_field_mapping_instrument` 与 `std_field_mapping_marketdata` 覆盖两张标准表字段映射。
=======
# FICC 债券标准化参考

本技能聚焦债券 `Instrument` 与 `IrYieldCurve` 两张标准表，按 `parseInstrument` 与 `parseMktData` 字段契约建模。

当前支持两类来源：

- 债券 API 原始库：`dfs://ficc_api_pdf_2026`
- 上清所曲线原始库：`dfs://ficc_curve_raw_2026`

## 文件说明

- `STANDARD_DICTIONARY.md`
  - 中文数据字典（必填/可选/条件必填 + 典型源字段）

## 执行脚本（位于 scripts 目录）

1. `01_create_standard_schema.dos`：建标准表与注释
2. `02_probe_source_db.dos`：探查 `dfs://ficc_api_pdf_2026` 与 `dfs://ficc_curve_raw_2026` 关键表结构
3. `03_build_field_mapping.dos`：构建源字段到标准字段映射表
4. `04_transform_to_standard.dos`：执行转换写入标准表
5. `05_quality_check.dos`：输出行数、空值、向量长度等质检结论

## 验收口径

- `std_instrument_bond` 与 `std_market_curve` 有数据；
- `std_field_mapping` 覆盖两张标准表字段映射；
- `std_qc_summary` 指标可读，可定位 API 曲线与 curve_raw 曲线的缺失字段或异常值。
>>>>>>> 9d5b720b37ab39d8527dcefd33710ba118119305
