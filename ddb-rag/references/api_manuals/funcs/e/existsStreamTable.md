# existsStreamTable

## 语法

`existsStreamTable(tableName)`

## 参数

**tableName** 字符串，表示流数据表名称。可以是普通流表、共享流表、持久化流表或高可用流表。

## 详情

查询指定的流数据表是否存在。

返回值：true 表示该流数据表存在；false 表示该数据表不存在。

## 例子

```
id=`XOM`GS`AAPL
x=102.1 33.4 73.6
rt=streamTable(id, x);
existsStreamTable(`rt)
```

返回：true

```
existsStreamTable(`srt)
```

返回：false

```
share rt as srt
existsStreamTable(`srt)
```

返回：true

