# 因子卡片：cloud_clear_signal

## 因子描述
当模糊性高时的成交金额与成交量偏离反映投资者过度抛售。

## 数学公式
$$
Factor_{i,t}=MA_{20}(|FogAmountRatio_{i,t}-FogVolumeRatio_{i,t}|)
$$

## 变量定义
- FogAmountRatio: 起雾时刻分钟成交金额均值 / 全日分钟成交金额均值
- FogVolumeRatio: 起雾时刻分钟成交量均值 / 全日分钟成交量均值

## 边界处理
- 分母为0时置空
- 缺失分钟数据不参与当日聚合
- 截面按1%/99% winsorize

## DolphinDB 代码
```dolphindb
src=loadTable("dfs://stock_daily","stock_daily_prev");
res=select ts_code as securityid,trade_date,0.0 as factor_value from src;
res=select securityid,trade_date,`cloud_clear_signal as factor_name,factor_value from res;
res
```
