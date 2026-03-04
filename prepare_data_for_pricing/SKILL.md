# .github/skills/prepare_data_for_pricing

## 技能概述 / Overview

此技能提供从优矿等API获取FICC定价所需基础数据，并将其导入到DolphinDB指定表中的完整流程。

## 核心流程 / Core Workflow

完成整个数据准备过程，请依次执行以下步骤。如果在任何步骤中遇到需要修改表名或理解字段的疑问，请参考对应的说明文档。

### 1. 探测API连通性
- **用途**: 检查能否正常访问数据API源。
- **脚本**: [`scripts/10_probe_uqer_api.py`](scripts/10_probe_uqer_api.py)
  - 这是一个需要传入 `token` 的Python脚本。
- **说明文档**: 暂无。

### 2. 下载极小样本数据
- **用途**: 下载少量（20条以内）样本数据，用于检查数据结构和字段。
- **脚本**: [`scripts/20_download_minimal_samples.py`](scripts/20_download_minimal_samples.py)
  - 该脚本会在本地 `sample_data/` 目录生成对应的CSV文件。
  - *如果 `sample_data/` 目录中已经有数据，可以跳过此步骤直接查看。*
- **说明文档**: [`reference/SCHEMA_DESCRIPTION.md`](reference/SCHEMA_DESCRIPTION.md)

### 3. 创建DolphinDB库表 (Schema)
- **用途**: 在DolphinDB中创建用于存放定价基础数据的分布式数据库和表。
- **脚本**: [`scripts/30_create_pricing_schema.dos`](scripts/30_create_pricing_schema.dos)
  - 如果DolphinDB上已存在目标库表，可以不执行此脚本。
  - 支持传入参数自定义库表名称，详情参见说明文档。
- **说明文档**: [`reference/SCHEMA_DESCRIPTION.md`](reference/SCHEMA_DESCRIPTION.md)

### 4. 探查现有数据
- **用途**: 在DolphinDB中探测现有数据，验证前一个步骤创建的库表，并校验表结构和字段信息。
- **脚本**: [`../pricing/scripts/01_data_discovery.dos`](../pricing/scripts/01_data_discovery.dos)
  - 检查现有的库表中的数据情况。
- **说明文档**: [`reference/SCHEMA_DESCRIPTION.md`](reference/SCHEMA_DESCRIPTION.md)

### 5. 导入全量数据至DolphinDB
- **用途**: 从API获取全量或指定日期范围内的数据，并直接导入DolphinDB的对应表中。
- **脚本**: [`scripts/40_ingest_raw_to_ddb.py`](scripts/40_ingest_raw_to_ddb.py)
  - 该步骤需要结合前几步创建好的库表结构。
- **说明文档**: [`reference/SCHEMA_DESCRIPTION.md`](reference/SCHEMA_DESCRIPTION.md)

## 参考文档
请参阅 [`reference/SCHEMA_DESCRIPTION.md`](reference/SCHEMA_DESCRIPTION.md) 获取每个表的具体用途，各字段的含义、类型，以及在各个脚本中支持的入参说明。
