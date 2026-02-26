# isDigit

## 语法

`isDigit(X)`

## 参数

**X** 是字符或字符串类型的标量、向量或表。

## 详情

判断 *X* 是否只包含数字。如果 *X* 中的所有字符都是数字，该函数返回 true，反之返回 false。对于空字符串（STRING 类型的
NULL 值），该函数返回 false。

## 例子

```
isDigit("123456");
// output
true

isDigit("1And1");
// output
false

isDigit("10.05");
// output
false

isDigit(string());
// output
false
```

