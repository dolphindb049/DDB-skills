---
name: develop-skills
description: Agent Skill 开发指南。涵盖 workspace 上下文体系（agent.md / skills）、Skill 目录结构规范、实践→归纳开发方法论、以及 Skill 日常维护准则。
license: MIT
metadata:
  author: jrzhang
  version: "4.0.0"
---

# Agent Skill 开发指南

> 把"做过一次"的经验，变成任何 Agent 都能一键复现的能力包。

---

## 1. Workspace 上下文体系

Agent 的知识来源分两层：

### 1.1 始终加载：agent.md / .instructions.md

放在 workspace 根目录（或 `.github/`）的 `agent.md`（或 `copilot-instructions.md`）**每次对话都会全文注入上下文**。适合写：

- 项目级约定（代码风格、分支策略、CI 规则）
- Agent 的角色与边界（"你是 XXX Agent，只做 YYY"）
- 全局环境信息（服务器地址、DDB 版本、公共库路径）

> ⚠️ 因为始终加载，**篇幅必须克制**，建议 < 2k tokens。

### 1.2 渐进式加载：Skills

放在 `.github/skills/<skill-name>/` 下的 Skill 按需分层加载：

| 层级 | 何时加载 | 内容 |
|------|---------|------|
| **L1 元数据** | 启动时全部加载 | YAML frontmatter 里的 `name` + `description`（~100 tokens/skill） |
| **L2 指令** | 用户意图匹配时加载 | SKILL.md 正文（建议 < 5k tokens） |
| **L3 资源** | Agent 主动 read_file 时加载 | `reference/`、`scripts/` 等，按需读取，不占启动上下文 |

这意味着 `reference/` 里可以放很长的文档也不影响性能——Agent 需要时才读。

---

## 2. Skill 目录结构规范

```text
your-skill/
├── SKILL.md           # 必需。主指南，< 5k tokens，给 Agent 读的
├── reference/         # 可选。详细方法论、踩坑记录、接口契约等
│   └── METHODOLOGY.md
├── scripts/           # 可选。可直接执行的代码，按编号排序
│   ├── 01_exploration.dos
│   ├── 02_structure.dos
│   └── ...
├── assets/            # 可选。Skill 需要的静态资源（模板、样本数据等）
└── .env.example       # 可选。敏感信息模板（API Key、Token 等）
```

### 要点

- **SKILL.md** 是唯一必需文件。开头写清楚"做什么 / 不做什么"，给出最小可跑通路径，记录关键踩坑。
- **reference/** 放更细的参考内容。SKILL.md 只写结论和速查，reference 放推导过程和完整案例。
- **scripts/** 放能跑的代码。建议按执行顺序编号（`01_`、`02_`...），Agent 可直接调用。
- **assets/** 放 Skill 运行时需要的存储物（模板文件、样本数据、预训练权重等）。
- **敏感信息独立到 .env**。API Key、Token、密码等**绝不硬编码**在 SKILL.md 或 scripts 中。提供 `.env.example` 作为模板，实际 `.env` 加入 `.gitignore`。

### YAML Frontmatter 规范

```yaml
---
name: your-skill-name          # 必需，kebab-case，和该 skill 的目录名一致
description: 一句话描述         # 必需，控制在 20 字以内
license: MIT
metadata:
  author: your-name
  version: "1.0.0"
  tags: ["tag1", "tag2"]
---
```

---

## 3. 开发方法论：实践 → 归纳

### 3.1 核心原则

1. **用最强的模型开发 Skill**。开发阶段的目标是最快找到正确方案，不要省 token。用 Claude Opus 4.6 / GPT-5.4 等顶级模型跑通全流程，再把经验写成 Skill 给任何模型复用。
2. **从任务开始，不从代码开始**。先完整做一遍，再归纳——这是"实践→归纳"法，不是"设计→实现"法。
3. **踩过的坑就是 Skill 的核心价值**。一个 Skill 如果只有步骤没有坑，那就是一篇没用的文档。

### 3.2 开发流程

```
① 打开对话，描述任务目标
② 告诉 Agent 有哪些可用工具（MCP、脚本、API）
③ 一起做一遍，遇到报错就修，直到跑通
④ 跑通后让 Agent 归纳：关键步骤、踩坑点、最佳实践
⑤ 整理成 SKILL.md + scripts/ + reference/
```

### 3.3 判断"什么该做成 Skill"

- 做过两次以上 → 值得沉淀
- 别人也需要做 → 值得共享
- 过程中有大量隐性知识（配置顺序、权限、兼容性等） → 必须写

---

## 4. Skill 维护准则

**Skill 不是写完就丢的文档，需要定期治理。**

### 4.1 定期精简

- **合并重复**：功能相似的 Skill 合并为一个，消除冗余
- **缩减篇幅**：SKILL.md 如果超过 5k tokens，把细节下沉到 `reference/`
- **删除过时内容**：API 变了、版本升级了，及时更新或标记废弃

### 4.2 质量标准

- **可复现**：另一个人用同级模型能一次跑通
- **自包含**：不隐式依赖"你知道的"上下文，所有前置条件写清楚
- **低耦合**：把硬编码的地址、库名、表名提取为参数或写在 .env 中

### 4.3 反模式

| 反模式 | 正确做法 |
|--------|---------|
| SKILL.md 写成万字长文 | 主文件只放结论和速查，细节放 reference/ |
| Skills 越堆越多从不清理 | 定期合并、缩减、下线过时 Skill |
| 把 API Key 写死在脚本里 | 用 .env + .env.example 管理敏感信息 |
| 不记录踩坑只写流程 | 踩坑记录是 Skill 最有价值的部分 |
| 用弱模型开发 Skill 反复试错 | 开发阶段用最强模型，快速找到方案再归纳 |

---

## 5. 更多参考

- `references/01-basic-concepts.md`：Agent / Workspace / Skills / Tools / Sandbox 基本概念
- `references/02-simple-repeatable-skills.md`：简单重复型 Skill 的开发示例（execute-dlang / DDB 部署 / 代理配置）
- `references/03-long-chain-skills-ficc.md`：长链条 Skill 的拆分与联调方法（FICC 定价案例）
- `references/04-pi-mono-product-case.md`：基于 pi-mono 做 DDB 产品的最小实现路径与第一步交付
- Anthropic 官方 Skill 文档：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- skills.sh 社区：https://skills.sh/
