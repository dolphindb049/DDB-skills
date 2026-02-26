# isUpper

## 语法

`isUpper(X)`

## 参数

**X** 是字符或字符串类型的标量或向量。

## 详情

判断字符串中的字母是否全部为大写。对于空字符串，该函数返回 false。

## 例子

```
isUpper("THIS IS STRING EXAMPLE....WOW!!!");
// output
true

isUpper("THIS is string example....wow!!!");
// output
false

isUpper("123456ABC");
// output
true

isUpper("123");
// output
false

isUpper(["  ",string()]);
// output
[false,false]
```

相关函数：[isLower](isLower.md), [isTitle](isTitle.md)

