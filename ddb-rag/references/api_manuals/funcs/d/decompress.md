# decompress

## 语法

`decompress(X)`

## 参数

**X** 是一个压缩后的向量。

## 详情

对一个压缩后的向量进行解压缩。

## 例子

```
x=1..100000000
y=compress(x, "delta");

y.typestr();
// output: HUGE COMPRESSED VECTOR

z=decompress(y);
z.size();
// output: 100000000
```

相关函数：[compress](../c/compress.md)

