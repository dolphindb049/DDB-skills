# isAlNum

## 语法

`isAlNum(X)`

## 参数

**X** 是字符或字符串类型的标量或向量。

## 详情

判断 *X* 是否只包含字母或数字。如果 *X*
中的所有字符都是字母和数字，该函数返回true，反之返回false。对于空字符串（STRING类型的NULL值），该函数返回false。

## 例子

```
isAlNum("123456");
// output
true

isAlNum("1And1");
// output
true

isAlNum("10.05");
// output
false

isAlNum(string());
// output
false
```

