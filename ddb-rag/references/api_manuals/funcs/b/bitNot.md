# bitNot

## 语法

`bitNot(X)`

## 参数

**X** 可以是数值型的标量，向量，矩阵，或数据表。

## 详情

返回按位取反的结果。

## 例子

```
bitNot(3)
// output
-4

av = array(INT[], 0, 10).append!([1 2 3, 4 5])
bitNot(av)
// output
[[-2,-3,-4],[-5,-6]]
```

