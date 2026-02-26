# DolphinDB 数据发现与预处理 (Data Discovery & Preprocessing)

本技能提供了一套完整且经过验证的脚本库，用于在 DolphinDB 中快速探索未知数据、理解表结构、清洗脏数据，并为后续分析构建高质量的数据基础。

## 🎯 核心价值
- **快速上手**: 无需查阅繁杂文档，直接运行脚本即可获得集群概览。
- **安全探索**: 所有脚本均采用只读或临时表操作，不会破坏原有生产数据。
- **最佳实践**: 集成了 DolphinDB 官方推荐的向量化清洗与元数据查询方法。

## 📂 脚本清单

| 脚本文件 | 功能描述 | 关键技术点 |
| :--- | :--- | :--- |
| `scripts/01_exploration.dos` | **全库扫描**: 自动发现在线数据库与表 | `getChunksMeta`, `dfsPath` |
| `scripts/02_structure.dos` | **结构透视**: 查看表字段类型与分区方案 | `schema`, `partitionSchema` |
| `scripts/03_queries.dos` | **数据画像**: 采样、统计总数、分布概览 | `top N`, `sql`, `Distribution` |
| `scripts/04_cleaning.dos` | **清洗修复**: 空值填充与异常处理 | `ffill`, `nullFill`, `update` |
| `scripts/05_sharing.dos` | **数据共享**: 内存表发布与跨会话访问 | `share`, `IPC`, `MemoryTable` |

## 🛠️ 使用指南

### 1. 配置连接信息
在使用前，请确保你知道目标集群的地址，所有脚本开头都有 `USER CONFIG` 区域，例如：

```dolphin
// --- 配置参数 (USER CONFIG) ---
dbPath = "dfs://futures"        // 替换为你的数据库路径
tableName = "ticks"             // 替换为你的表名
```

### 2. 渐进式探索流程
建议按照脚本序号依次执行：

1.  运行 `01_exploration.dos` 找到你感兴趣的数据库路径（如 `dfs://stock`）。
2.  修改 `02_structure.dos` 中的 `dbPath`，查看该库有哪些表及字段。
3.  使用 `03_queries.dos` 确认数据量级（count）和大致内容（top 10）。
4.  如果发现 NULL 值较多，参考 `04_cleaning.dos` 进行清洗。
5.  清洗后的干净数据若需进一步分析，参考 `05_sharing.dos` 发布为共享内存表。

## 📚 参考文档
- [DolphinDB SQL 参考手册](https://docs.dolphindb.cn/zh/sql/index.html)
- [数据导入教程](https://docs.dolphindb.cn/zh/tutorials/import_data.html)
