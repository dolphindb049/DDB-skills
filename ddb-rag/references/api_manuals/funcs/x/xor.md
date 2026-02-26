# xor

## 语法

`xor(X, Y)`

## 参数

**X** 和 **Y** 可以是标量、数据对、向量、矩阵或表。

## 详情

按元素逐个返回 *X* 逻辑异或 (`XOR`)*Y* 的结果。

## 例子

```
1 xor 0
// output
1

x = 5 6 7
x xor 0
// output
[1,1,1]

x = 1 2 3
y = 2 1 3
x xor y
// output
[0,0,0]

true xor false
// output
1
```

相关函数：[or](../o/or.md), [not](../n/not.md)

