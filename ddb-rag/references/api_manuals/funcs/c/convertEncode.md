# convertEncode

## 语法

`convertEncode(str, srcEncode, destEncode)`

## 参数

**str** 是一个字符串标量或向量。

**srcEncode** 是一个字符串，表示 *str* 原来的编码名称。

**destEncode** 是一个字符串，表示 *str* 的目标编码名称。

## 详情

转换字符串编码。DolphinDB 对编码名称的大小写敏感，所有编码名称必须用小写表示。

Window 版本目前仅支持 gbk 和 utf-8 两种编码的相互转换。Linux 版本支持任意两种编码之间的转换。

## 例子

```
convertEncode("高性能分布式时序数据库","utf-8","gbk");
// output
高性能分布式时序数据库

convertEncode(["hello","DolphinDB"],"gbk","utf-8");
// output
["hello","DolphinDB"]
```

相关函数：[fromUTF8](../f/fromUTF8.md), [toUTF8](../t/toUTF8.md)

