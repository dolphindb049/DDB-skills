# tushare-ddb

纯 DolphinDB 服务端 Tushare 数据同步 Skill。不依赖 Python，通过 httpClient 插件直接调用 Tushare API。

## 目录结构

```
tushare-ddb/
  _common.dos          ← 公共层: token、callTS、票池、交易日历
  minute/
    schema.dos         ← 分钟频建库建表
    sync.dos           ← 历史回填 + 实时同步 + 定时任务
```

后续可扩展：`daily/`、`tick/`、`fund/` 等，每个数据源同样 schema.dos + sync.dos 两件套。

## 快速开始

在 DolphinDB **任意 data node** 上依次 source 三个文件：

```dolphindb
// 1. 加载公共层
source "/your/path/_common.dos"

// 2. 建库建表（幂等）
source "/your/path/minute/schema.dos"
ensureMinuteDB()

// 3. 加载同步函数
source "/your/path/minute/sync.dos"
```

## 分钟频 API

### 历史回填

```dolphindb
// 全 A 回填（约 5500 只，需要数小时）
backfill(2026.01.01, 2026.03.11)

// 指定股票
backfill(2026.03.01, 2026.03.11, ["000001.SZ", "600000.SH"])
```

### 实时同步

```dolphindb
// 手动跑一轮
syncOnce()
```

### 定时任务

```dolphindb
// 注册：每日 9:30 启动，60s 一轮循环到 15:01
install()

// 删除
uninstall()
```

### 诊断

```dolphindb
status()                              // 今日概况
coverage(2026.03.11)                  // 某日每股覆盖率
backfillStatus(2026.03.01, 2026.03.11) // 日期范围覆盖
```

## 配置

编辑 `_common.dos` 中的 `tsCfg()` 函数：

| 参数 | 说明 |
|------|------|
| token | Tushare API token |
| apiUrl | API 地址（默认 https://api.tushare.pro） |
| timeout | HTTP 超时毫秒（默认 30000） |

编辑 `minute/schema.dos` 中的 `minuteSchema()` 修改库表名：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| db | dfs://ts_minute | 数据库路径 |
| tb | bar_1m | 表名 |

## DFS 表设计

- 引擎: TSDB
- 分区: COMPO = RANGE(月) × HASH(SYMBOL, 20)
- 排序键: ts_code, trade_time
- 去重: keepDuplicates=LAST
