# 累计窗口系列（cum 系列）

累积窗口，即窗口的起始边界固定，结束边界逐步向右移动的窗口。针对累计窗口计算场景，DolphinDB 提供了 cum 系列函数。

## cum 系列函数介绍

cum 系列函数对应的高阶函数 [accumulate](../ho_funcs/accumulate.md)：

```
accumulate(func, X, [init])
```

注：

如果指定了 *init*，第一个窗口的结果为 *init* + *X* [0]。

内置的 cum 系列函数的通用参数模板如下：

```
cumfunc(X)
cumfunc(X, Y)
```

## 参数

**X** (**Y**) 是一个标量、向量、矩阵、表或由等长向量组成的元组。cum 系列函数如下：

单目：

* [cummax](../c/cummax.md)
* [cummin](../c/cummin.md)
* [cummed](../c/cummed.md)
* [cumfirstNot](../c/cumfirstNot.md)
* [cumlastNot](../c/cumlastNot.md)
* [cumrank](../c/cumrank.md)
* [cumcount](../c/cumcount.md)
* [cumpercentile](../c/cumpercentile.md)
* [cumstd](../c/cumstd.md)
* [cumstdp](../c/cumstdp.md)
* [cumvar](../c/cumvar.md)
* [cumvarp](../c/cumvarp.md)
* [cumsum](../c/cumsum.md)
* [cumsum2](../c/cumsum2.md)
* [cumsum3](../c/cumsum3.md)
* [cumsum4](../c/cumsum4.md)
* [cumavg](../c/cumavg.md)
* [cumprod](../c/cumprod.md)
* [cumnunique](../c/cumnunique.md)
* [cumPositiveStreak](../c/cumPositiveStreak.md)

双目：

* [cumbeta](../c/cumbeta.md)
* [cumwsum](../c/cumwsum.md)
* [cumwavg](../c/cumwavg.md)
* [cumcovar](../c/cumcovar.md)
* [cumcorr](../c/cumcorr.md)

## 窗口确定规则

cum
系列函数可以视为一个累计的窗口计算，对数据中的每一个元素，都会进行一次累计计算，因此返回一个和元数据等长的向量（相同维度的矩阵）。

其计算规则如下图：

![](../../images/cum_1.png)

上图的对应代码，这里以 [cumsum](../c/cumsum.md) 为例：

```
X = 1 1 2 3 4 5 NULL 8 9 1 3
cumsum(X)

//output: [1, 2, 4, 7, 11, 16, 16, 24, 33, 34, 37]
```

