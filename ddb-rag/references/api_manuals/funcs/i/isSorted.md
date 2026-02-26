# isSorted

## 语法

`isSorted(X, [ascending=true])`

## 参数

**X** 是一个向量。

**ascending** 是布尔值，表示 *X* 按升序排序（true）或降序排序（false）。默认值为 true。

## 详情

检查 *X* 是否排序。

## 例子

```
x=NULL 1 2 3
isSorted(x);
// output
true

t=table(9 7 5 3 as x, 1 5 2 4 as y)
t.x.isSorted(false);
// output
true

t.y.isSorted();
// output
false
```

