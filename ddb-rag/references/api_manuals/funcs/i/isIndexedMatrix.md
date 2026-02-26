# isIndexedMatrix

## 语法

`isIndexedMatrix(X)`

## 参数

**X** 是一个矩阵。

## 详情

判断 *X* 是否为有索引的矩阵。

## 例子

```
m=matrix(1..10, 11..20)
m.rename!(2020.01.01..2020.01.10, `A`B);

isIndexedMatrix(m);
// output
false

m.setIndexedMatrix!()
isIndexedMatrix(m);
// output
true
```

