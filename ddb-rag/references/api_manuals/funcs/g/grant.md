# grant

## 语法

`grant(userId|groupId, accessType, [objs])`

## 参数

**userId** | **groupId** 是表示用户名或组名的字符串。

**accessType** 权限类型/内存限制。

**objs** 标量或向量，表示权限类型的应用对象/约束规则。也可以指定为 \*，表示全局。当 *accessType* 指定为 COMPUTE\_GROUP\_EXEC 时，*objs*
必须为对应的计算组名。

注：

* 管理共享内存表、流数据表或流计算引擎的权限时，*objs* 必须为 "tableName@nodeAlias"
  或"nodeAlias:tableName"。
* 管理 IMOLTP 引擎库表权限时，*objs* 必须为 "oltp://database/table@nodeAlias" 或
  "oltp://database@nodeAlias"。

*accessType* 和 *objs* 的取值请参照 [用户权限管理](../../tutorials/ACL_and_Security.md) 权限类型表。

## 详情

`grant` 函数执行以下操作：

* 授予某个用户或某个用户组权限。当 *accessType* = DB\_OWNER 时，还支持约束某个用户只能创建指定前缀的数据库。
* 约束某个用户查询返回结果的内存上限（指定 *accessType* =
  QUERY\_RESULT\_MEM\_LIMIT）和发送的批量子查询占用的内存上限（指定 *accessType* =
  TASK\_GROUP\_MEM\_LIMIT）。其功能等效于 [setMemLimitOfQueryResult](../s/setMemLimitOfQueryResult.md) 函数和 [setMemLimitOfTaskGroupResult](../s/setMemLimitOfTaskGroupResult.md) 函数，区别在于 `grant`
  只对指定用户生效（暂不支持用户组），`setMemLimitOfQueryResult` 函数和
  `setMemLimitOfTaskGroupResult` 函数对所有用户生效。

管理员可以通过该命令赋予用户所有权限（*accessType*），但普通用户在拥有相关的 OWNER
权限后，只能通过该命令赋予以下权限：TABLE\_READ, TABLE\_WRITE, TABLE\_INSERT, TABLE\_UPDATE, TABLE\_DELETE,
DB\_READ, DB\_WRITE, DB\_INSERT, DB\_UPDATE, DB\_DELETE, DBOBJ\_DELETE, DBOBJ\_CREATE 和
VIEW\_EXEC。

注： 该函数可在控制节点、数据节点和计算节点运行。

## 例子

授予组 "research" 的所有成员读取所有数据库表的权限：

```
grant(`research, TABLE_READ, "*")
```

授予组 "research" 的所有成员读写表 dfs://db1/t1 的权限：

```
grant(`research, TABLE_WRITE, "dfs://db1/t1")
```

授予组 "research" 的所有成员在数据库 dfs://db1 和
dfs://db2 创建表的权限：

```
grant("research", DBOBJ_CREATE, ["dfs://db1","dfs://db2"])
```

授予用户 "AlexSmith" 删除数据库的权限：

```
grant("AlexSmith", DB_MANAGE)
```

授予用户"AlexSmith"执行脚本的权限：

```
grant("AlexSmith", SCRIPT_EXEC)
```

授予用户 "AlexSmith" 测试脚本的权限：

```
grant("AlexSmith", TEST_EXEC)
```

授予用户”AlexSmith”命名空间 test1下函数 f1 的执行权限：

```
grant("AlexSmith", VIEW_EXEC, "test1::f1")
```

授予用户”AlexSmith”命名空间 test2 下所有函数的执行权限：

```
grant("AlexSmith", VIEW_EXEC, "test2::*")
```

命名空间必须是模块级别。例如有一个模块 *test.dos*，所在路径为
moduleDir/mod1/test.dos，为用户授权执行模块中所有函数时，应通过以下脚本实现：

```
grant("AlexSmith", VIEW_EXEC, "mod1::test::*")
```

不支持写成：

```
grant("AlexSmith", VIEW_EXEC, "mod1::*")
```

如果授权了某个命名空间，后来命名空间中的函数视图被通过 `dropFunctionView`
删除，一旦命名空间中的最后一个函数视图被删除，对该命名空间的授权也将自动回收。同理，授权时如果发现该命名空间下没有函数视图，会抛出异常。

对于没有命名空间的函数视图，被认为是全局的。以下两种方式等价：

```
grant("AlexSmith", VIEW_EXEC, "::f")
grant("AlexSmith", VIEW_EXEC, f)
```

约束用户查询所占用的内存：

指定 *accessType* 为 QUERY\_RESULT\_MEM\_LIMIT，此时 *objs*
表示限制的内存大小，单位为 GB。下述脚本限制用户 "AlexSmith" 查询时，查询结果所占用的内存大小不能超过 4 GB。

```
grant("AlexSmith", QUERY_RESULT_MEM_LIMIT, 4)
```

约束用户只能创建指定前缀的数据库：

假设管理员要求限制用户 "AlexSmith" 只能创建并管理以 ddb 作为库名前缀的数据库，可以通过以下脚本实现：

```
grant("AlexSmith", DB_OWNER, "dfs://ddb*")
```

当指定 `grant` 函数的 *accessType* 为 DB\_OWNER 时，可以指定
*objs* 为一个规则，目前仅支持约束用户可以创建的库名前缀，便于不同用户管理不同范围的数据库。

当需要指定多个规则时，可以为 objs 传入一个向量，如下脚本所示：

```
grant("AlexSmith", DB_OWNER, ["dfs://ddb_prefix1*","dfs://ddb_prefix2*"])
```

授权时，如果当前已有全局授权，则对某一前缀规则的授权将无效。如果前缀规则之间存在包含关系，则这些规则不会相互覆盖。

当用户创建或管理数据库时，如有全局禁止，则禁止执行，否则，用户的权限为所有前缀规则的并集，即如果库名符合已授权的任一前缀规则，则允许执行。已授权的前缀规则可以通过函数
`getUserAccess` 查看。

注： 特定的前缀约束规则，只能通过 `grant` 指定、通过
`revoke` 移除，但不能通过 `deny` 禁止。当 *accessType* 为
DB\_OWNER 时，`deny` 只能对全局生效，且会覆盖之前已有的前缀约束规则。

