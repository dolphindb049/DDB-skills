# Tushare 数据导入 DolphinDB

这个 skill 负责把 Tushare 数据规范化导入 DolphinDB。

当前已经补齐一套独立于原有日更批处理的分钟频专用方案，优先用于 A 股 1 分钟行情写入 DolphinDB。

## 当前推荐入口

- `Tushare数据导入/CreateMinuteDBTB.dos`
- `Tushare数据导入/AutoLoadMinuteHistory.py`
- `Tushare数据导入/AutoLoadMinuteRealtime.py`
- `Tushare数据导入/CheckMinuteCompleteness.py`
- `Tushare数据导入/ProbeRtMinCapacity.py`

`Tushare数据导入/dataSource/stock_minute_1m.py` 仍可作为一次性手工导入入口使用，但分钟频的正式运行建议使用上面的三段式流程。

## 实现说明

- 数据源接口：`tushare.pro_bar(..., freq='1min')`
- 实时接口：`pro.rt_min(ts_code='600000.SH,000001.SZ', freq='1MIN')`
- 历史接口：`tushare.pro_bar(..., freq='1min')`
- 落库目标：`dfs://minute_factor/stock_minute_1m`
- 分区方式：`trade_date + ts_code HASH` 的 TSDB 复合分区
- 运行方式：分钟频任务独立于原有 `AutoLoadTushareData.py/AutoLoadTushareData_today.py`
- 历史回补：按股票、按日期窗口抓取分钟线并补齐近一段历史
- 实时增量：每分钟使用 `rt_min` 按小批股票抓取当日分钟线，只追加 DB 中还不存在的尾部数据
- 完整性检查：比较期望分钟槽位与已落库槽位，识别缺口并支持修复

## 推荐流程

1. 先跑近一周历史分钟回补
2. 再启动每分钟增量脚本常驻补齐
3. 定期运行完整性检查，或在实时脚本中开启 `--repair-missing`
4. 在准备切到大股票池前，先运行 `ProbeRtMinCapacity.py` 测出当前账号的 `rt_min` 批量能力

## 建议使用方式

先回补近一周历史分钟：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteHistory.py --symbols 000001.SZ 600000.SH --start-date 20260305 --end-date 20260311 --check-after-load
```

然后按每分钟做增量补齐：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteRealtime.py --symbols 000001.SZ 600000.SH --repair-missing --exit-after-close
```

如果要按全活跃股票池做分批实时轮询：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteRealtime.py --all-active-symbols --api-batch-codes 800 --max-batches-per-loop 5 --repair-missing
```

如果只想执行一轮增量：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/AutoLoadMinuteRealtime.py --symbols 000001.SZ 600000.SH --run-once
```

如果只做完整性检查或修复：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/CheckMinuteCompleteness.py --symbols 000001.SZ 600000.SH --trade-date 20260311 --repair-missing
```

如果要先做 `rt_min` 批量能力探测：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/ProbeRtMinCapacity.py --all-active-symbols --limit-symbols 1200 --batch-sizes 50 100 200 500 800 1000
```

原来的手工单次验证入口仍可保留：

```powershell
python .github/skills/tushare-data-import-ddb/Tushare数据导入/dataSource/stock_minute_1m.py --symbols 000001.SZ 600000.SH --pause 31
```

## 注意事项

- 分钟频任务默认读取 `basic.py` 里的 `minuteTask` 配置
- 不传 `--all-active-symbols` 时，实时任务默认优先读取 `basic.py` 里 `minuteTask.symbols` 的小股票池
- 传入 `--all-active-symbols` 后，实时任务会忽略 `basic.py` 的固定股票池，改为读取当前活跃股票列表
- `rt_min` 虽然支持多股票同时请求，但单次最大返回 1000 行；随着盘中分钟数增长，单次能覆盖的股票数会快速下降，收盘附近通常只能安全覆盖很小的股票批次
- 当前 token 的分钟接口权限非常低时，实时速度会被 Tushare 限频约束，这不是脚本本身的问题
- 如果要做真正的大范围分钟级实时更新，需要更高的 Tushare 分钟权限或更适合实时流的行情源
