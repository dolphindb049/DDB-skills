# invLogistic

## 语法

`invLogistic(mean, s, X)`

## 参数

**mean** 是Logistic分布的均值。

**s** 是Logistic分布的尺度参数。

**X** 是0到1之间的浮点型标量或向量。

## 详情

返回Logistic分布的累计密度函数的逆函数值。

## 例子

```
invLogistic( 2.31, 0.627, [0.5, 0.3, 0.5, 0.7, 0.1]);
// output
[2.31, 1.778744, 2.31, 2.841256, 0.93234]
```

