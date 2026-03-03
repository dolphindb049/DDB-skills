# 因子卡片：ambiguity_correlation

## 因子描述
模糊性与成交额相关性刻画厌恶强度。

## 数学公式
$$
Corr_{i,d}=corr(Fog_{i,d,m},Amount_{i,d,m}),\;Factor_{i,t}=MA_{20}(Corr_{i,t})
$$

## 变量定义
- Fog: 波动率的波动率
- Amount: 分钟成交金额

## 边界处理
- 缺失值处理
- 除零处理
- 极值处理

## DolphinDB 代码
```dolphindb
// TODO: replace with minute-level implementation
```
