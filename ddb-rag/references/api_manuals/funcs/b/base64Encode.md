# base64Encode

## 语法

`base64Encode(X)`

## 参数

**X** 字符串标量或向量。

## 详情

将 *X* 转换为 Base64 编码格式。

返回值：字符串标量或向量。

## 例子

```
base64Encode(`hello)
// output
aGVsbG8=

base64Encode(`hello`world)
// output
["aGVsbG8=","d29ybGQ="]

base64Encode("")
// output
""
```

相关函数：[base64Decode](base64Decode.md)

