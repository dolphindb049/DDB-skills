# ksTest

## 语法

`ksTest(X, Y)`

## 参数

**X** 是一个数值向量。

**Y** 是一个数值向量。

## 详情

对 *X* 和 *Y* 进行 Kolmogorov-Smirnov
检验，检验它们是否符合同一个分布。返回的结果是一个字典，包含以下 key：

* ksValue：Kolmogorov-Smirnov 统计量
* pValue：p 值
* D：D 统计量
* method：字符串 "Two-sample Kolmogorov-Smirnov test"

## 例子

```
x = norm(0.0, 1.0, 50)
y = norm(0.0, 1.0, 20)
ksTest(x, y);

// output
ksValue->0.739301
pValue->0.645199
D->0.19
method->Two-sample Kolmogorov-Smirnov test
```

