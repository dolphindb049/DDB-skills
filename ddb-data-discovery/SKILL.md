---
name: ddb-data-discovery
description: DolphinDB 数据发现与预处理专家技能。提供从全库扫描、表结构透视到数据清洗与内存共享的完整工作流脚本。
license: MIT
metadata:
  author: ddb-user
  version: "2.0.0"
  tags: ["etl", "exploration", "cleaning", "metadata"]
---

# DolphinDB 数据发现与预处理 (Data Discovery & Preprocessing)

本技能提供了一套专家级的 DolphinDB 脚本库，旨在帮助用户快速接手陌生的 DolphinDB 集群，完成从**全库资产盘点**到**高质量数据清洗**的全流程。

## 📂 技能结构

```text
ddb-data-discovery/
├── scripts/
│   ├── 01_exploration.dos  # [全库扫描] 自动发现集群内所有数据库路径
│   ├── 02_structure.dos    # [结构透视] 查看表结构、字段类型与分区方案
│   ├── 03_queries.dos      # [数据画像] 采样、统计总数、分布概览
│   ├── 04_cleaning.dos     # [清洗修复] 空值填充(ForwardFill)、异常处理
│   └── 05_sharing.dos      # [数据共享] 发布为共享内存表(IPC)，跨会话复用
└── reference/
    └── METHODOLOGY.md      # 📖 详细使用指南与方法论
```

## 🚀 核心能力

### 1. 资产自动发现 (Auto Discovery)
针对接手新环境痛点，通过底层函数 `getChunksMeta` 扫描全集群数据块，自动推断出所有数据库的 DFS 路径，不再需要手动询问管理员库名。

### 2. 向量化预处理 (Vectorized Cleaning)
利用 DolphinDB 强大的向量引擎，进行毫秒级的空值填充与数据修正。
- **前向填充 (Forward Fill)**: 完美解决金融时间序列中的停牌/无交易导致的空洞。
- **指定填充 (Fill with Value)**: 快速修复缺失的 Volume 或 Status。

### 3. 连接与共享 (Connect & Share)
演示了如何将清洗后的数据发布为 **Shared In-Memory Table**，使其成为流计算源头或供其他分析师即席查询，实现 "Write Once, Read Many"。

## 💡 快速开始

1.  **浏览指南**: 阅读 [reference/METHODOLOGY.md](reference/METHODOLOGY.md) 了解每个脚本的最佳适用场景。
2.  **配置参数**: 打开任意 `.dos` 脚本，修改顶部的 `USER CONFIG` 区域：
    ```dolphin
    // --- 配置参数 (USER CONFIG) ---
    dbPath = "dfs://your_db_path"   // 填入你的数据库
    tableName = "your_table_name"   // 填入你的表名
    ```
3.  **运行脚本**: 使用 `execute-dlang` 技能或 DolphinDB GUI 运行脚本。

## 🔧 常见问题

- **Q: 脚本报错 "Table not found"?**
    - A: 请先运行 `01_exploration.dos` 确认数据库路径是否正确，部分集群即便是标准库也可能有非标准的前缀。
- **Q: 数据量太大内存溢出？**
    - A: 脚本默认包含 `top 1000` 或 `where Date=...` 过滤条件。生产环境中通过 `loadTable` 获取句柄后，务必带上 `where` 条件进行切片处理。
