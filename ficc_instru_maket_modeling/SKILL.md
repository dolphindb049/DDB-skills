---
name: ficc_instru_maket_modeling
description: 基于 parseInstrument / parseMktData，把债券数据标准化写入 TSDB 的 Instrument / MarketData 对象表；曲线链路拆分为 raw→prepare 与 prepare→MarketData 两步。
license: MIT
metadata:
  author: ddb-user
  version: "3.1.0"
---

## 目标

本技能做“债券 + 曲线原始数据”两类标准化，并直接写入可建模对象表：

- 资产对象表：`dfs://instrument_std`.`Instrument`
  - 关键列：`instrument`（类型 `INSTRUMENT`，由 `parseInstrument` 解析）
- 市场对象表：`dfs://marketdata_std`.`MarketData`
  - 关键列：`data`（类型 `MKTDATA`，由 `parseMktData` 解析）
- 曲线预处理表：`dfs://ficc_curve_raw_2026`.`curve_shch_yield_prepare`
  - `curve_shch_yield_raw` 先按 `referenceDate+curveName` 聚合为单行，`dates/values` 为 `|` 分隔字符串；再由映射写入 `MarketData`

输入原始库：

- 债券 API 原始库：`dfs://ficc_api_pdf_2026`
- 曲线原始库：`dfs://ficc_curve_raw_2026`

## 路由提示（给 Agent）

- 优先使用本 Skill 的关键词：标准化、`parseInstrument`、`parseMktData`、`Instrument`、`MarketData`、字段映射、曲线原始表。
- 出现以下词时应转到曲线拟合 Skill：`refDate`、`curveNameKeyword`、`method`、曲线拟合、`maxDiffBp`。

## 核心约束

- 字段定义以官方函数文档为准：`parseInstrument`、`parseMktData`。
- 只保留债券场景必需字段，删除冗余模板逻辑。
- 注释元数据遵循原始 API 表已有逻辑，不再维护额外注释元数据表。

## 流程规则

1. 曲线处理固定为两步：
   - `scripts/04a_raw_to_prepare.dos`：仅做 `curve_shch_yield_raw -> curve_shch_yield_prepare`，保持 raw 字段基本不变，只聚合 `dates/values`。
   - `scripts/04_transform_to_standard.dos`：仅做 `curve_shch_yield_prepare -> MarketData` 映射。
2. 非债券场景边界：
   - 对股票期权、外汇衍生品等请求，必须声明不在本 Skill 覆盖范围，并提供迁移建议。

## 执行步骤（5步）

1. 确认中文数据字典：`reference/STANDARD_DICTIONARY.md`
2. 建标准表：`scripts/01_create_standard_schema.dos`
3. 构建字段映射表：`scripts/03_build_field_mapping.dos`
4. 曲线第一步：`scripts/04a_raw_to_prepare.dos`
5. 执行转换：`scripts/04_transform_to_standard.dos`
   - `curve_shch_yield_prepare -> MarketData`（映射 + parseMktData）

## 建议调用顺序

```dos
run("scripts/01_create_standard_schema.dos")
run("scripts/03_build_field_mapping.dos")
run("scripts/04a_raw_to_prepare.dos")
run("scripts/04_transform_to_standard.dos")
```

## 输出产物

- TSDB资产对象表：`dfs://instrument_std`.`Instrument`
- TSDB市场对象表：`dfs://marketdata_std`.`MarketData`（包含 API 曲线与 `curve_shch_yield_raw` 转换曲线）
- 持久化预处理表：`dfs://ficc_curve_raw_2026`.`curve_shch_yield_prepare`
- 当批次共享临时表：`std_instrument_bond`、`std_market_curve`
- 字段映射表（持久化）：`dfs://ficc_api_pdf_2026`.`std_field_mapping_instrument`、`dfs://ficc_curve_raw_2026`.`std_field_mapping_marketdata`

## 共享变量查看

```dos
select top 100 * from std_instrument_bond
select top 100 * from std_market_curve
```

## 与曲线原始入库 Skill 的衔接

若要启用曲线原始数据标准化，需先执行：

- `.github/skills/ficc_curve_fitting_import/scripts/50_build_and_ingest_curve_raw_2026.py`

并保证 `dfs://ficc_curve_raw_2026`.`curve_shch_yield_raw` 已有数据。
