# getClusterDFSDatabases

## 语法

`getClusterDFSDatabases()`

## 参数

无

## 详情

该函数由管理员执行时，返回当前集群中所有分布式数据库；

由其他用户执行时，返回该用户在集群中拥有以下权限的分布式数据库：DB\_OWNER, DB\_MANAGE, DB\_READ, DB\_INSERT, DB\_UPDATE,
DB\_DELETE, DBOBJ\_CREATE, DBOBJ\_DELETE。

## 例子

```
getClusterDFSDatabases()

// output
["dfs://demohash","dfs://myDataYesDB","dfs://testDB"]
```

