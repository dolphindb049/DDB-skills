---
name: ddb-rag
description: 一个 DolphinDB RAG 系统，用于搜索文档和教程。
license: MIT
metadata:
  author: ddb-user
  version: "1.0.0"
---

# DolphinDB RAG 知识库

本技能包提供了用于 DolphinDB 文档和教程的搜索服务 (RAG)。

## 🏗️ 结构概览

```text
ddb-rag/
├── references/             # 🧠 知识库 (RAG 的输入)
│   ├── tutorials/          # [方法论] 步骤指南、模式与技巧。
│   └── api_manuals/        # [事实] 声明式的 API 定义、函数规范。
├── scripts/                # 🛠️ 工具
│   ├── rag/                # [工具] GPU 加速的搜索服务
└── SKILL.md                # 🧭 本文档
```

## 🛠️ RAG 服务 (搜索)

**使用场景**: "我不知道怎么做 X" 或 "函数 Y 的参数是什么？"

**命令**:
*   **更新索引** (在编辑 references 后运行):
    ```bash
    uv run scripts/rag/ingest.py
    ```
*   **启动服务器** (用于持久化 Agent 使用):
    ```bash
    uv run scripts/rag/mcp_server.py
    ```
*   **快速搜索** (命令行):
    ```bash
    uv run scripts/rag/cli_search.py "查询内容的上下文"
    ```
