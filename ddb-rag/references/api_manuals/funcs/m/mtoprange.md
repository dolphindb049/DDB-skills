# mTopRange

## 语法

`mTopRange(X, window, [minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.md)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内，统计每个元素 Xi 左侧相邻且连续小于它的元素个数。NULL 被视为最小值。

若 *X* 是矩阵，在每列内进行上述计算。

## 例子

```
x = [NULL, 3.1, NULL, 3.0, 2.9, 2.8, 3.1, NULL, 3.2]
mTopRange(x, window=3)
// output: [,,0,1,0,0,2,0,2]

mTopRange(x, window=3, minPeriods=1)
// output: [,1,0,1,0,0,2,0,2]

x = [NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, 3.2]
date = [0, 1, 2, 3, 7, 8, 9, 10, 11] + 2020.01.01
X = indexedSeries(date, x)
mTopRange(X, 3d)
```

|  | #0 |
| --- | --- |
| 2020.01.01 |  |
| 2020.01.02 |  |
| 2020.01.03 |  |
| 2020.01.04 |  |
| 2020.01.08 |  |
| 2020.01.09 | 1 |
| 2020.01.10 | 0 |
| 2020.01.11 | 0 |
| 2020.01.12 | 2 |

```
m = matrix(1 2 3 NULL, 1 2 NULL 3, 1 3 NULL NULL, 1 2 3 4)
mTopRange(m, 2)
```

| #0 | #1 | #2 | #3 |
| --- | --- | --- | --- |
|  |  |  |  |
| 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 0 | 1 |  | 1 |

