# distinct

## 语法

`distinct(X)`

## 参数

**X** 是一个向量或数组向量类型。

## 详情

只返回向量 *X*
中不相同的元素，如果有两个或以上的相同元素，将只返回一个。结果中返回的顺序不保证和原来的向量相同。

## 例子

```
distinct 4 5 5 2 3;
// output
[3,2,5,4]

a = array(INT[], 0, 10).append!([1 2 3,  4 5, 6 7 8, 9 10])
distinct(a)
// output
[10,9,8,7,6,5,4,3,2,1]

t=table(3 1 2 2 3 as x);
select distinct x from t;
```

| distinct\_x |
| --- |
| 2 |
| 1 |
| 3 |

```
select sort(distinct(x)) as x from t;
```

| x |
| --- |
| 1 |
| 2 |
| 3 |

函数 `distinct` 返回一个向量，而函数 [`set`](../s/set.md) 返回一个集合。

```
x=set(4 5 5 2 3);
x;
// output
set(3,2,5,4)
x.intersection(set(2 5));
// output
set(2,5)
```

在内存表或分布式表中，`distinct` 函数可以和
`group by` 配合使用，每个分组的结果为一个数组向量。

```
dbName = "dfs://testdb"
if(existsDatabase(dbName)){
   dropDatabase(dbName)
}

db=database("dfs://testdb", VALUE, 2012.01.11..2012.01.29)

n=100
t=table(take(2012.01.11..2012.01.29, n) as date, symbol(take("A"+string(21..60), n)) as sym, take(100, n) as val)

pt=db.createPartitionedTable(t, `pt, `date).append!(t)
result=select distinct(date) from pt group by sym
select sym, distinct_date from result where sym=`A21
```

| sym | distinct\_date |
| --- | --- |
| A21 | [2012.01.15,2012.01.13,2012.01.11] |

