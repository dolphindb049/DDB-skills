# disableActivePartition

## 语法

`disableActivePartition(dbHandle)`

## 参数

**dbHandle** 是历史数据库的句柄。

## 详情

断开与历史数据库的连接。

## 例子

```
histdb = database("C:\DolphinDBDemo\example\data\dbspace\historical-A\Trades2ndDomain")
activeNodeAlias = getNodeAlias()
activeDate = today()
enableActivePartition(histdb, activeDate, activeNodeAlias);

disableActivePartition(histdb);
```

