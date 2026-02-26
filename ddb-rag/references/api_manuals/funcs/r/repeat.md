# repeat

## 语法

`repeat(X, n)`

## 参数

**X** 是一个字符串或字符串向量。

**n** 是一个非负整数，表示重复的次数。

## 详情

返回 *X* 重复 *n* 次后的字符串。

## 例子

```
repeat(`FB, 3);
// output
FBFBFB
repeat(`AB`CD,2);
// output
["ABAB","CDCD"]
```

