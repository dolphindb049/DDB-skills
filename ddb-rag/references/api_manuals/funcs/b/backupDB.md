# backupDB

## 语法

`backupDB(backupDir, dbPath, [keyPath])`

## 参数

**backupDir** 字符串，表示存放备份数据的目录。

**dbPath** 字符串，表示数据库路径。

**keyPath** 字符串标量，指定备份时使用的密钥文件路径。仅 Linux 系统支持该参数。该密钥用于对备份数据进行加密。设置为空即不加密。

## 详情

备份数据库到指定路径。

该函数是 [backup](backup.md) 函数的特例，其等价于调用
`backup(backupDir, dbPath, force=false, parallel=true,
snapshot=true)`。 调用该函数可以简化代码，方便用户一次性备份整个数据库。

## 例子

```
dbName = "dfs://compoDB2"
n=1000
ID=rand("a"+string(1..10), n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10, n)
t=table(ID, date, x)
db1 = database(, VALUE, 2017.08.07..2017.08.11)
db2 = database(, HASH,[INT, 20])
if(existsDatabase(dbName)){
  dropDatabase(dbName)
}
db = database(dbName, COMPO,[ db1,db2])

// 创建2个表
pt1 = db.createPartitionedTable(t, `pt1, `date`x).append!(t)
pt2 = db.createPartitionedTable(t, `pt2, `date`x).append!(t)

backupDB(backupDir, dbName)
```

相关函数：[backup](backup.md), [backupTable](backupTable.md), [restore](../r/restore.md), [restoreDB](../r/restoreDB.md), [restoreTable](../r/restoreTable.md), [migrate](../m/migrate.md)

