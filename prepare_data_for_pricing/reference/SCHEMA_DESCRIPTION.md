# 数据库与表结构详细说明

本文档包含 `prepare_data_for_pricing` 技能所涉及的库表规划与字段说明。
在运行创建库表、探测现有数据以及向表内写入数据的脚本时，若需修改参数或排查错误，请参考本文档。

## 核心库表设计 (Pricing Schema)

我们创建的数据库路径默认为 `dfs://ficc_raw_data_mcp`，所有原始数据都存放在这个数据库的下属表中。
如果你需要修改库名或表名，请在调用 [`scripts/30_create_pricing_schema.dos`](../scripts/30_create_pricing_schema.dos) 时关注其入参或顶部的变量定义。

### 1. 市场基础信息表 (ficc_market_info)
用于存放机构、交易日历等静态或低频更新的基础信息。

**核心字段示例**:
- `tradeDate` (DATE): 交易日
- `marketCode` (SYMBOL): 市场代码（如 CIB, SSE）

### 2. 债券基础特征表 (ficc_bond_info)
存放债券的基本信息，如起息日、到期日、票面利率、付息频率等。定价模块需要根据这些信息生成现金流。

**核心字段示例**:
- `ticker` (SYMBOL): 债券代码
- `issueDate` (DATE): 起息日/发行日
- `maturityDate` (DATE): 到期日
- `couponRate` (DOUBLE): 票面利率
- `paymentFrequency` (INT): 付息频率（如一年付息次数：1, 2, 4）

### 3. 收益率曲线表 (ficc_yield_curve)
存放各种类型、不同期限的市场收益率或国债收益率曲线关键点。定价模块基于此进行折现计算。

**核心字段示例**:
- `tradeDate` (DATE): 日期
- `curveType` (SYMBOL): 曲线类型（如 "CDB" 国开行, "BOND" 国债）
- `tenor` (DOUBLE): 期限（年）
- `yield` (DOUBLE): 对应收益率

## 脚本入参说明

### 30_create_pricing_schema.dos
- `dbPath`: 字符串，默认 `dfs://ficc_raw_data_mcp`。你要创建的库名。
- `bondInfoTable`: 字符串，默认 `ficc_bond_info`。

### 40_ingest_raw_to_ddb.py
- `--token`: 优矿API的Token。
- `--start-date` / `--end-date`: 数据拉取区间。
- `--db-path`: 连接并写入DolphinDB用的数据库路径。