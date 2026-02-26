# denseRank

## 语法

`denseRank(X, [ascending=true],[ignoreNA=true], [percent=false])`

## 参数

**X** 是一个向量或矩阵。

**ascending** 是一个布尔值，表示是否按升序排序。默认值是 true。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值，默认值为 true。true 表示忽略 NULL 值，false 表示 NULL
作为最小值参与排名。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名，默认值为 false。

## 详情

若 *X* 是向量：

* 基于 *ascending* 指定的排序顺序，返回 *X* 中每个元素连续的排名。
* 如果 *ignoreNA* = true，则 NULL 值不参与排序，结果中 NULL 值的排名为空。

若 *X* 是矩阵，在每列内进行上述计算，返回一个与 *X* 维度相同的矩阵。

注： `denseRanke` 和 [rank](../r/rank.md)
的区别在于，多个元素相等时，前者采用密集排名方式，而后者采用跳跃排名方式。

## 例子

```
x=1 5 5 6 8 8 9
print denseRank(x)
// output
[0,1,1,2,3,3,4]

y=time(4 1 1 2)
print denseRank(y, ascending=false)
// output
[0,2,2,1]
m = matrix(1 2 2 NULL, 0 0 0 1, 0 0 NULL 2)
denseRank(m, ignoreNA=false)
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 0 | 1 |
| 2 | 0 | 0 |
| 0 | 1 | 2 |

```
t=table(`A`A`B`C`B`B`A`C`C as id,[4,1,NULL,1,2,4,5,0,-1] as val)
select id,val, denseRank(val) from t context by id
```

| id | val | denseRank\_val |
| --- | --- | --- |
| A | 4 | 1 |
| A | 1 | 0 |
| A | 5 | 2 |
| B |  |  |
| B | 2 | 0 |
| B | 4 | 1 |
| C | 1 | 2 |
| C | 0 | 1 |
| C | -1 | 0 |

相关函数：[rowDenseRank](../r/rowDenseRank.md)

