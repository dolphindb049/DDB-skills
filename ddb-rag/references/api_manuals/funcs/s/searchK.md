# searchK

## 语法

`searchK(X, k)`

## 参数

**X** 是一个向量。

## 详情

返回第 *k* 小的元素，忽略 NULL 值。

## 例子

```
searchK(1 7 3 5 3 9 6 1 NULL, 1);
```

输出返回：1

```
searchK(1 7 3 5 3 9 6 1 NULL, 2);
```

输出返回：1

```
searchK(1 7 3 5 3 9 6 1 NULL, 3);
```

输出返回：3

