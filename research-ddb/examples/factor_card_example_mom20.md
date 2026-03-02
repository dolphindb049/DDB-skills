# 因子卡片：mom20

## 1. 基本信息

- 因子名称：mom20
- 因子别名：20日动量
- 来源研报：示例
- 版本：v1
- 创建日期：2026-03-02

## 2. 金融学逻辑

中期价格动量体现投资者行为惯性。过去 20 个交易日累计上涨更强的股票，在短期内继续获得超额收益的概率更高。

## 3. 数学表达式

$$
mom20_{i,t} = \frac{P_{i,t}}{P_{i,t-20}} - 1
$$

变量定义：

- $P_{i,t}$: 股票 $i$ 在交易日 $t$ 的收盘价。
- $P_{i,t-20}$: 向前 20 个交易日的收盘价。

## 4. 计算约定

- 频率：日频
- 取值方向：越大越好
- 缺失值处理：窗口不足时为 NULL，不参与当日截面排序
- 极值处理：截面 1%/99% 分位 winsorize
- 标准化：按交易日做 zscore

## 5. DolphinDB 字段映射

- 基础表：`dfs://day_factor.stock_daily_prev`
- 字段映射：
  - trade_date -> trade_date
  - securityid -> ts_code
  - close -> close

## 6. 可复现执行

1. 用 `scripts/10_factor_compute_template.dos` 生成 `mom20` 计算脚本。
2. 用 `scripts/20_retry_validate_factor.dos` 验证非空率和覆盖率。
3. 用 `scripts/30_merge_to_unified_table.dos` 落 `stock_factor_unified`。
4. 用 `scripts/40_evaluate_factor.dos` + `scripts/build_factor_report.py` 输出报告。
