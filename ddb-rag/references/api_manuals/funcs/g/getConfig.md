# getConfig

## 语法

`getConfig([key])`

## 参数

**key** 是一个字符串，表示配置参数名称，为可选参数。

## 详情

若不指定 *key*，返回一个字典，显示系统所有的配置信息。若指定的 *key* 为有效配置参数，返回一个 scalar 或
vector，表示具体的配置信息；若指定的 *key* 不是配置参数，则返回空值。

**相关信息**

* [参数配置](../../db_distr_comp/cfg/para_cfg.html "参数配置")

