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
