# 研报复现工作流（Research → Factor）

## Phase 1: 研报解析

输入：1~N 个 PDF 研报。

输出：候选因子列表（含变量字典）。

步骤：

1. 提取研报中的“经济机制/行为机制”。
2. 识别可观测变量（价格、成交量、估值、财务、行业标签）。
3. 判断变量粒度（日频/周频/截面/时序）。
4. 形成候选因子定义，不允许模糊术语。

## Phase 2: 公式化

每个因子必须给出：

- 严格数学表达式。
- 变量定义与单位。
- 边界处理（停牌、缺失值、极值、分母为 0）。
- 方向性（值越大越好/越小越好）。

产出文件：单因子卡片（见 `templates/factor_card_template.md`）。

## Phase 3: DDB 试算与修复

基础表：`loadTable("dfs://day_factor", "stock_daily_prev")`

目标：因子计算成功并可落表。

策略：

1. 先跑最小样本（10~30 个交易日，100~300 支股票）。
2. 仅检验字段是否存在、类型是否匹配、空值率是否可接受。
3. 出错后定位为：字段缺失 / 类型冲突 / 窗口越界 / 除零 / SQL 拼接。
4. 修复后重跑，直到结果稳定。

## Phase 4: 统一表落库

推荐统一结构：

- `trade_date` DATE
- `securityid` SYMBOL
- `factor_name` SYMBOL
- `factor_value` DOUBLE
- `source_report` STRING
- `version` STRING
- `updated_at` TIMESTAMP

要求：同日同股票同因子唯一。

## Phase 5: 因子评价

至少产出：

- 日度 IC 序列与均值、标准差、ICIR。
- 分层收益（5 分组）。
- 多空（Top-Bottom）收益与净值。
- 年化收益、波动、夏普、最大回撤。

## Phase 6: Python 可视化报告

报告必须包含：

1. 评价摘要表。
2. IC 时间序列图。
3. 分组净值图。
4. 多空净值与回撤图。
5. 文字结论（优点、缺点、是否建议入库）。
