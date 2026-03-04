# .github/skills/pricing

## 技能概述 / Overview

此技能集成了FICC债券资产在DolphinDB中的定价逻辑，贯穿从数据准备、模型映射、再到最终输出价格结果的完整工作流。主要负责将标准化的原始数据处理为您定义的资产定价模型表。

## 核心流程 / Core Workflow

完成整个工作流需要执行以下脚本，更多细节请查阅相关文档：

### 1. 准备输出数据的表结构
- **用途**: 创建基于原始数据的各种输出结构表。它包括了资产定义（Instrument）、市场数据（MarketData）以及最终得到的定价和风险结果。
- **脚本**: [`scripts/02_prepare_output_schema.dos`](scripts/02_prepare_output_schema.dos)
  - 根据输入数据和定价模型建立相应的输出存储。
- **说明文档**: [`reference/TABLE_SCHEMA_AND_WORKFLOW.md`](reference/TABLE_SCHEMA_AND_WORKFLOW.md)

### 2. 运行统一的定价流水线
- **用途**: 串联之前建立的库表结构，执行统一的计算逻辑和核心函数，产生输出数据并存入指定的分析或展示表中。
- **脚本**: [`scripts/05_run_unified_pipeline.dos`](scripts/05_run_unified_pipeline.dos)
  - 调用相关的定价函数和参数设置。具体函数和参数信息参考相关说明文档。
- **说明文档**: [`reference/TABLE_SCHEMA_AND_WORKFLOW.md`](reference/TABLE_SCHEMA_AND_WORKFLOW.md)
  - 在相关文档中提供了对应定价函数的说明和调用方法，方便后续调整或独立调用各个计算步骤。

## 参考文档
请参阅 [`reference/INTERFACE_CONTRACT.md`](reference/INTERFACE_CONTRACT.md) 获取校验库表所需信息的介绍，以及 [`reference/TABLE_SCHEMA_AND_WORKFLOW.md`](reference/TABLE_SCHEMA_AND_WORKFLOW.md) 以了解各个函数的调用要求。
