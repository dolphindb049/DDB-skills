# strlenu

## 语法

`strlenu(X)`

## 参数

**X** 是一个字符串标量或向量。

## 详情

用于获取 Unicode 编码的目标字符串的长度。

## 例子

```
strlenu("高性能分布式时序数据库")
// output
11

strlenu(["高性能分布式时序数据库","DolphinDB"])
// output
[11,9]
```

