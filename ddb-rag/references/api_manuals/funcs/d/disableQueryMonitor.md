# disableQueryMonitor

## 语法

`disableQueryMonitor()`

## 参数

无

## 详情

关闭监控查询任务状态的功能。

由于监控查询任务状态具有一定的内存开销，内存资源紧张时，可以关闭该功能。注意：调用该命令后，用户将无法调用 [getQueryStatus](../g/getQueryStatus.md) 函数获取查询任务的状态。

相关函数： [enableQueryMonitor](../e/enableQueryMonitor.md)

