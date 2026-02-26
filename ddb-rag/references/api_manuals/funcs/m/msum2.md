# msum2

## 语法

`msum2(X, window, [minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.md)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内计算 *X* 元素的平方和。请注意，该函数的返回值是 DOUBLE 类型。

## 例子

```
X = 2 1 3 7 6 5 4
Y = 2 1 3 NULL 6 5 4

msum2(X, 3)
// output
[,,14,59,94,110,77]

msum2(Y, 3)
// output
[,,14,10,45,61,77]

msum2(Y, 3, minPeriods=1)
// output
[4,5,14,10,45,61,77]

m = matrix(1 NULL 4 NULL 8 6 , 9 NULL NULL 10 NULL 2)
m.rename!(date(2021.08.16)+1..6, `col1`col2)
m.setIndexedMatrix!()
msum2(m, 3d)  // 等价于 msum2(m, 3)
```

| label | col1 | col2 |
| --- | --- | --- |
| 2021.08.17 | 1 | 81 |
| 2021.08.18 | 1 | 81 |
| 2021.08.19 | 17 | 81 |
| 2021.08.20 | 16 | 100 |
| 2021.08.21 | 80 | 100 |
| 2021.08.22 | 100 | 104 |

相关函数：[sum2](../s/sum2.md)

