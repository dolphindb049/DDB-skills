# deleteScheduledJob

## 语法

`deleteScheduledJob(jobId)`

## 参数

**jobId** 是一个表示定时任务 ID 的字符串。

## 详情

删除一个定时任务。如果指定的任务 ID 不存在，则抛出异常。

## 例子

```
deleteScheduledJob(`dailyJob1);
```

