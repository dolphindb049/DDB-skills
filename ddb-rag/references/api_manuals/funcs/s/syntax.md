# syntax

## 语法

`syntax(X)`

## 参数

**X** 是 DolphinDB 函数或命令。

## 详情

返回 *X* 表示的函数或命令的语法。

## 例子

```
syntax(createPartitionedTable);
// output
createPartitionedTable(dbHandle, table, tableName, [partitionColumns], [compressMethods])
```

