# sort!

## 语法

`sort!(X, [ascending=true])`

## 参数

**X** 是一个向量。

**ascending** 是一个布尔值，表示按升序排序还是按降序排序。默认值为 true（按升序排序）。

## 详情

返回一个排序后的向量。该函数会改变 *X* 的值。

## 例子

```
x=9 1 5;
sort!(x);
x;
// output
[1 5 9]

x.sort!(0);
x;
// output
[9,5,1]
```

