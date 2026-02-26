# and

## 语法

`and(X, Y)` 或 `X && Y`

## 参数

**X** 和 **Y** 可以是标量、数据对、向量或矩阵。

## 详情

对 *X* 和 *Y* 内的元素逐个进行逻辑与（logical AND）的运算并返回结果。

## 例子

```
1 && 3;
// output
1

x=1 2 3
x && 0
// output
[0,0,0]

x=1 2 3
y=0 1 0
x && y
// output
[0,1,0]

t=table(1 2 2 3 as id, 4 5 6 5 as value)
t
```

| id | value |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 2 | 6 |
| 3 | 5 |

```
select id, value from t where id=2 and value=5;   // SQL query
```

| id | value |
| --- | --- |
| 2 | 5 |

相关函数：[or](../o/or.md), [not](../n/not.md)

