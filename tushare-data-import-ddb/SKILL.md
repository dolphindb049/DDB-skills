# Tushare 数据导入 DolphinDB

这个 skill 负责把 Tushare 数据规范化导入 DolphinDB。

当前已经整理为一个最小可运行的分钟频方案，优先用于 A 股 1 分钟行情全池实时写入 DolphinDB。

## 当前推荐入口

- `Tushare数据导入/CreateMinuteDBTB.dos`
- `Tushare数据导入/AutoLoadMinuteRealtime.py`
- `Tushare数据导入/dataSource/stock_minute_1m_lib.py`

## 实现说明

- 实时接口：`pro.rt_min(ts_code='600000.SH,000001.SZ', freq='1MIN')`
- 落库目标：`dfs://minute_factor/stock_minute_1m`
- 分区方式：`trade_date + ts_code HASH` 的 TSDB 复合分区
- 运行方式：分钟频任务独立于原有 `AutoLoadTushareData.py/AutoLoadTushareData_today.py`
- 更新策略：每分钟按股票批次请求 `rt_min`，只追加 DB 中还没有的最新分钟记录
- 默认模式：读取全活跃 A 股列表，并按 `1000` 只股票一批轮询

## 建议使用方式

按全活跃股票池每分钟更新：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteRealtime.py
```

如果要明确指定全池轮询参数：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteRealtime.py --all-active-symbols --api-batch-codes 1000
```

如果只跑一轮：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteRealtime.py --run-once
```

如果收盘后想手动补跑一轮：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteRealtime.py --run-once --ignore-session-window
```

## 注意事项

- 分钟频任务默认读取 `basic.py` 里的 `minuteTask` 配置
- 当前实测 `rt_min` 在盘中返回的是每个股票一条当前分钟记录，不是开盘以来全分钟历史
- 当前账号实测 `50/100/200/500/800/1000` 股票批次都能返回成功，单批耗时约 `0.1s ~ 0.16s`
- 默认 `1000` 股票一批时，大约 `5` 批即可覆盖 `5000` 只股票的全池轮询
