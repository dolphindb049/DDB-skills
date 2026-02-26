# lpad

## 语法

`lpad(str, length, [pattern])`

## 参数

**str** 可以是字符串或字符串向量。它表示目标字符串。

**length** 是一个非负整数，表示填充之后的字符串长度。如果 *length* 小于 *str* 的长度，*lpad*
函数相当于 [left](left.md) (str, length).

**pattern** 是填充字符串。它是一个可选参数。如果 *pattern* 没有指定，则在
*str* 的左边填充空格。

## 详情

在 *str* 的左边填充指定字符串。

## 例子

```
lpad("Hello",2);
// output
He

lpad(`Hello, 10);
// output
Hello

lpad(`Hello, 12, `0);
// output
0000000Hello
```

