# addAccessControl

## 语法

`addAccessControl(table)`

## 参数

**table** 共享表或者流数据引擎对象。

## 详情

用户可使用此命令，限制其他用户访问该用户创建的共享表或者流数据引擎。进行此项操作后，其他用户只有被管理员赋予访问权限后，才可访问该用户创建的共享表或者流数据引擎。

注：

1. 只能由创建 *table* 的用户或者管理员执行该命令。
2. 如果管理员已经为其他用户 grant/deny/revoke
   该表的权限，则该表自动添加权限限制，其他未经授权的用户无法再访问该表，建表用户无需调用
   `addAccessControl` 对表进行访问管理。

## 例子

创建一组用户，进行权限管理。

```
login(`admin, `123456)
createUser(`u1, "111111");
createUser(`u2, "222222");
createUser(`u3, "333333");
```

流数据引擎：

```
// 用户 u1 创建流数据引擎 agg1
login(`u1, "111111")
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
output1 = table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])
agg1 = createTimeSeriesEngine(name="agg1", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50, useWindowStartTime=false)
subscribeTable(tableName="trades", actionName="agg1", offset=0, handler=append!{agg1}, msgAsTable=true);
// 给 agg1 增加访问控制
addAccessControl(agg1)

// 用户 u2 访问
login(`u2, "222222")

// 注入数据
insert into trades values(2018.10.08T01:01:01.785,`A,10) # OK!
insert into agg1 values(2018.10.08T01:01:01.785,`A,10) # ERROR: No access to table [agg1]

// 注销引擎
dropStreamEngine("agg1") # No access to drop stream engine agg1
```

共享内存表：

```
login(`u1, "111111")
t = table(take(`a`b`c`, 10) as sym, 1..10 as val)
share t as st;
addAccessControl(`st)

login(`u3, "333333")
select * from st # ERROR: No access to shared table [st]
insert into st values(`a, 4) # ERROR: No access to shared table [st]
```

