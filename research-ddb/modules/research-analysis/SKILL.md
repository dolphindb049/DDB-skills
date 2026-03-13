---
name: research-analysis
description: research-ddb 内部子模块：研报文本解析、多因子卡片生成、DolphinDB 代码落地。
license: MIT
metadata:
  scope: internal-module
  parent: .github/skills/research-ddb
---

# Research Analysis (Submodule)

这是 `research-ddb` 的内部子模块。

职责：

1. 从研报文本 + 因子规格生成多因子卡片。
2. 为每个因子输出 DolphinDB `.dos` 代码文件。
3. 输出统一目录索引 `factor_catalog.json`。

输出结构：

```text
<outdir>/
├── factor_cards/
│   ├── <factor_1>.md
│   └── <factor_2>.md
├── ddb_scripts/
│   ├── <factor_1>.dos
│   └── <factor_2>.dos
└── factor_catalog.json
```
