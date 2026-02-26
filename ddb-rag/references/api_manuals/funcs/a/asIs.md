# asis

## 语法

`asis(obj)`

## 参数

**obj** 可以是任意数据类型。

## 详情

返回 *obj* 的引用。

## 例子

```
a = 1 2 3
b = asis(a)
a[0] = 0
b
// output
[0, 2, 3]
b[1] = 4
// output
a;
[0, 4, 3]
```

相关函数：[copy](../c/copy.md), [deepCopy](../d/deepCopy.md)

