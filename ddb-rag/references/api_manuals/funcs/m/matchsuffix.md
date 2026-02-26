# matchSuffix

## 语法

`matchSuffix(textCol, suffix)`

## 参数

**textCol** 待查询的列，即 PKEY 存储引擎中设置了文本索引的列。

**suffix** STRING 类型标量，用于指定待查询的后缀。

## 详情

该函数用于 SQL 语句的 WHERE 子句，针对 PKEY 存储引擎中设置文本索引的列进行后缀匹配，返回包含指定后缀的行。

## 例子

```
// 构造数据
stringColumn = ["There are some apples and oranges.","Mike likes apples.","Alice likes oranges.","Mike gives Alice an apple.","Alice gives Mike an orange.","John likes peaches, so he does not give them to anyone.","Mike, can you give me some apples?","Alice, can you give me some oranges?","Mike traded an orange for an apple with Alice."]
t = table([1,1,1,2,2,2,3,3,3] as id1, [1,2,3,1,2,3,1,2,3] as id2, stringColumn as remark)
if(existsDatabase("dfs://textDB")) dropDatabase("dfs://textDB")
db = database(directory="dfs://textDB", partitionType=VALUE, partitionScheme=[1,2,3], engine="PKEY")
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="id1",primaryKey=`id1`id2,indexes={"remark":"textindex(parser=english, full=false, lowercase=true, stem=true)"})
pt.tableInsert(t)

// 匹配包含后缀是 ke 的单词的行
select * from pt where matchSuffix(remark,"ke")
```

| id1 | id2 | remark |
| --- | --- | --- |
| 1 | 2 | Mike likes apples. |
| 1 | 3 | Alice likes oranges. |
| 2 | 1 | Mike gives Alice an apple. |
| 2 | 2 | Alice gives Mike an orange. |
| 2 | 3 | John likes peaches, so he does not give them to anyone. |
| 3 | 1 | Mike, can you give me some apples? |
| 3 | 3 | Mike traded an orange for an apple with Alice. |

