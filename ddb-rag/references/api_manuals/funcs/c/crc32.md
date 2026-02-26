# crc32

## 语法

`crc32(str, [cksum=0])`

## 参数

**str** 是一个字符串标量、向量或表。

**cksum** 是整型标量或向量。

## 详情

根据 CRC32 算法，对字符串进行哈希，生成 INT 类型数据。

## 例子

```
a=crc32(`aa`cc,1);
a;
// output
[512829590,-1029100744]

typestr(a);
// output
FAST INT VECTOR
```

