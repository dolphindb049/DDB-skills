# 因子卡片：{{factor_name}}

## 1. 基本信息

- 因子名称：{{factor_name}}
- 因子别名：{{factor_alias}}
- 来源研报：{{report_name}}
- 版本：{{version}}
- 创建日期：{{date}}

## 2. 金融学逻辑

{{finance_logic}}

## 3. 数学表达式

$$
{{math_formula}}
$$

变量定义：

- {{var_1}}: {{var_1_meaning}}
- {{var_2}}: {{var_2_meaning}}
- {{var_3}}: {{var_3_meaning}}

## 4. 计算约定

- 频率：{{frequency}}
- 取值方向：{{direction}}
- 缺失值处理：{{na_policy}}
- 极值处理：{{winsor_policy}}
- 标准化：{{normalization}}

## 5. DolphinDB 字段映射

- 基础表：`dfs://day_factor.stock_daily_prev`
- 字段映射：
  - trade_date -> {{date_col}}
  - securityid -> {{security_col}}
  - close -> {{close_col}}
  - vol -> {{vol_col}}

## 6. 可复现执行

1. 复制 `scripts/10_factor_compute_template.dos` 并替换 `FACTOR_NAME` 与公式。
2. 运行 `scripts/20_retry_validate_factor.dos` 做试错。
3. 成功后执行 `scripts/30_merge_to_unified_table.dos`。
4. 执行 `scripts/40_evaluate_factor.dos` 与 `scripts/build_factor_report.py`。
