# getEnableNullSafeJoin

## 语法

getEnableNullSafeJoin()

## 参数

无

## 详情

返回在线修改后的 *enableNullSafeJoin* 的配置值。配置详情请参考文档 [DolphinDB-功能配置](../../db_distr_comp/cfg/function_configuration.md)。

**返回值** BOOL 类型标量

## 例子

```
// 设置 enableNullSafeJoin 为 true
setDynamicConfig("enableNullSafeJoin", true)
// 查看修改后的配置值
getEnableNullSafeJoin()
// output: true
```

