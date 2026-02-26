# endsWith

## 语法

`endsWith(X, str)`

## 参数

**X** 是搜索的目标字符串。它可以是标量或向量。

**str** 是被搜索的目标字符串。它必须是标量。

## 详情

检查 *X* 是否以 *str* 结尾。如果是，返回 true； 否则返回 false。

## 例子

```
endsWith('ABCDEF!', "F!");
// output
true

endsWith('ABCDEF!', "E!");
// output
false
```

