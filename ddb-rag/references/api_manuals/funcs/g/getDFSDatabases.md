# getDFSDatabases

## 语法

`getDFSDatabases()`

## 参数

无

## 详情

返回当前节点上的分布式数据库。

2.00.9 版本起，

* 当该函数由管理员或拥有 DB\_MANAGE 权限的用户执行时，返回当前节点上所有分布式数据库；
* 否则，仅返回该用户有 DB\_OWNER 权限的数据库。

## 例子

```
getDFSDatabases()
```

