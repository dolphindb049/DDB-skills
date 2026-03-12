---
name: develop-skills
description: Agent Skill 开发实战指南。从零开始：环境搭建、Skill 与 Tool 的区别、归纳式开发法、FICC 定价案例全拆解、联调与 Agent 编排，到 DolphinX Skills Market 共享倡议。
license: MIT
metadata:
  author: jrzhang
  version: "3.0.0"
---

# 从零开始开发 Agent Skill —— 实战指南

> 一句话：**把你"做过一次"的经验，变成任何人、任何 Agent 都能"一键复现"的能力包。**

本文面向想要开发、共享 Agent Skill 的一线工程师。不讲空话，全程以我们团队实际落地的十几个 Skill 为例，带你从拿到 API Key 开始，一步步走到发布你自己的 Skill，并参与 DolphinX Skills Market 共建。

---

## 目录

0. [快速上手：5 分钟跑通你的第一个 Skill](#0-快速上手5-分钟跑通你的第一个-skill)
1. [什么是 Skill？跟 Tool 到底有什么区别？](#1-什么是-skill跟-tool-到底有什么区别)
2. [Skill 的开发方法论：自上而下的归纳式开发](#2-skill-的开发方法论自上而下的归纳式开发)
3. [我们已有的 Skill 一览——每个都是"被逼出来的"](#3-我们已有的-skill-一览每个都是被逼出来的)
4. [实战案例：FICC 债券定价 —— 从任务到 Agent 的完整开发过程](#4-实战案例ficc-债券定价--从任务到-agent-的完整开发过程)
5. [Skill 的文件结构与渐进式加载](#5-skill-的文件结构与渐进式加载)
6. [测试与迭代](#6-测试与迭代)
7. [DolphinX Skills Market：共享与共建倡议](#7-dolphinx-skills-market共享与共建倡议)
8. [结语](#8-结语)

---

## 0. 快速上手：5 分钟跑通你的第一个 Skill

**别急着看理论，先跑起来。** 下面是最小路径，让你体会到"Skill 到底能干嘛"。

### 0.1 环境准备

你需要：

| 项目 | 说明 |
|------|------|
| VS Code | 安装 GitHub Copilot 扩展（Chat 面板） |
| API Key | 公司统一提供，或自行申请 OpenAI / Claude / 第三方兼容 API |
| 代理配置 | 如果公司网络受限，参考 `codex-vscode-proxy-setup` Skill 配置代理 |
| Python + uv | 部分 Skill 的脚本依赖 Python 环境，推荐用 `uv` 做包管理 |

### 0.2 把 Skills 仓库拉到本地

```bash
git clone <你的skills仓库地址> .github/skills
```

拉完之后，VS Code 的 Copilot Chat 会自动识别 `.github/skills/` 下的所有 Skill（通过 YAML frontmatter 中的 `name` 和 `description`）。

### 0.3 试一下

在 Copilot Chat 里说一句：

> "帮我在 192.168.1.5:8848 部署一个 DolphinDB 单节点"

如果你已经有 `ddb-deployment-skill`，Agent 会自动触发它，按步骤帮你完成部署。你什么都不用记，Skill 帮你记住了所有细节。

**这就是 Skill 的价值：你踩过的坑，别人不用再踩。**

---

## 1. 什么是 Skill？跟 Tool 到底有什么区别？

这是最常见的困惑。一张表说清楚：

| 维度 | Tool（工具） | Skill（技能） |
|------|-------------|--------------|
| **本质** | 一个可调用的函数/API | 一套可复用的方法论 + 步骤 + 经验 |
| **类比** | 自行车、扳手、计算器 | "骑自行车"、"修水管"、"做财务分析" |
| **粒度** | 原子操作：读文件、发请求、执行 SQL | 工作流：多个 Tool 的编排 + 判断 + 经验 |
| **谁来用** | Agent 直接调用 | Agent 阅读后理解，再决定如何调用 Tool |
| **开发方式** | **自下而上（演绎式）**：先定义接口 → 实现函数 → 注册到 MCP | **自上而下（归纳式）**：先完成任务 → 总结经验 → 写成 Skill |
| **举例** | `execute.py`（执行一段 DDB 代码） | `ddb-deployment-skill`（部署 DDB 的完整流程） |
| **数量焦虑** | Tool 多了会让 Agent 困惑（选择成本高） | Skill 多了反而更好（知识越丰富越强） |
| **生命周期** | 相对稳定，接口变化少 | 持续迭代，随着经验积累不断优化 |

**一句话总结：Tool 是"能做什么"，Skill 是"怎么做好"。**

### 开发方式的根本区别

```
Tool 的开发（自下而上 / 演绎式）：
  定义接口签名 → 实现代码 → 写测试 → 注册到 MCP → Agent 可调用

Skill 的开发（自上而下 / 归纳式）：
  带 Agent 做一次完整任务 → 过程中告诉它有哪些可用工具
  → 反复试错直到跑通 → 让 AI 归纳出步骤和经验 → 写成 SKILL.md
```

Skill 更像是"学徒制"：你带着 AI 做一遍，它学会了，然后你们一起把经验写下来，下次谁都能用。

---

## 2. Skill 的开发方法论：自上而下的归纳式开发

### 2.1 核心理念

**不要从代码开始，从任务开始。**

传统的开发习惯是先写函数、先设计接口。但 Skill 的开发恰好相反——你应该：

1. **打开一个对话**，告诉 AI："我要完成 XXX 任务"
2. **告诉它有哪些可用的工具**（MCP、脚本、API）
3. **一起做一遍**，过程中会遇到报错、踩坑、走弯路
4. **做完之后**，让 AI 帮你归纳："刚才我们做了哪些关键步骤？哪些地方容易出错？"
5. **把总结写成 SKILL.md**

### 2.2 一个最简单的例子：服务器部署代理

我经常需要在不同的 Linux 服务器上配置 Mihomo 代理，每次都要：
- 解压二进制包
- 拉取订阅链接
- 生成最小配置
- 设置 on/off/status 命令
- 分发到多台机器

第一次做的时候花了 2 小时，各种路径不对、配置写错。第二次又接手一台新服务器，又花了 1 小时回忆上次怎么搞的。

**第三次我受不了了**，于是打开 Copilot Chat，跟 AI 说："我们一起把刚才的过程整理成一个 Skill 吧。" 它帮我生成了 `mihomo_onoff/SKILL.md` + 一组脚本，之后再部署新服务器，5 分钟搞定。

**这就是 Skill 的起源：反复做同样的事，就该写成 Skill。**

### 2.3 判断"什么该做成 Skill"

问自己三个问题：
1. **我做过两次以上了吗？** → 如果是，值得沉淀
2. **别人也需要做这件事吗？** → 如果是，值得共享
3. **过程中有很多"隐性知识"吗？**（配置顺序、端口冲突、权限问题等）→ 如果是，必须写成 Skill

---

## 3. 我们已有的 Skill 一览——每个都是"被逼出来的"

以下是 `.github/skills/` 目录下已有的 Skill，每一个背后都有一个"重复劳动"的痛苦故事：

| Skill | 一句话说明 | 为什么要做成 Skill |
|-------|----------|-------------------|
| **codex-vscode-proxy-setup** | Windows 下配置 Codex CLI + 第三方 API 代理 | 每个新同事入职都要配一遍，配错了 debug 半天 |
| **mihomo_onoff** | Linux 服务器一键装 Mihomo 代理 + on/off/status | 多台服务器反复部署，每次都忘记配置细节 |
| **ddb-deployment-skill** | DolphinDB 单节点部署与升级 | 共享服务器上多人部署，改错名字就误杀别人进程 |
| **execute-dlang** | DolphinDB 脚本执行器（支持持久化会话） | 是几乎所有 DDB Skill 的底层依赖，统一执行入口 |
| **ddb-data-discovery** | 全库扫描、表结构透视、数据清洗 | 接手陌生集群时的标准动作，每次都要从头摸索 |
| **ddb-data-analysis** | 量化数据分析：聚合、回归、假设检验 | 把散落在各处的分析脚本统一成标准化工作流 |
| **ddb-visualization** | 因子评价结果渲染为单页 HTML 仪表板 | 每次出图都要调 Plotly 参数，做成 Skill 一行命令出报告 |
| **document-translation** | PDF/Word 文档自动化翻译（保留排版） | 翻译外文文献，手动逐段翻太慢，整篇扔给模型会丢格式 |
| **pdf** | PDF 读取、合并、拆分、OCR 等 | 处理研报、合同等 PDF 的通用能力 |
| **pptx** | PPT 创建、读取、编辑 | 自动生成汇报材料 |
| **research-ddb** | 研报复现：PDF → 因子卡片 → DDB 落库 → 评价报告 | 量化研究的核心工作流，串联多个子 Skill |
| **research-analysis** | 研报文本分析 + 因子卡片生成 | 从研报中提取可执行的因子逻辑 |
| **prepare_data_for_pricing** | 债券定价前的数据准备：建库建表、样本导入 | FICC 定价流程的上游依赖 |
| **pricing** | 债券定价与风险分析 | FICC 定价流程的核心计算 |
| **find-skills** | 用 skills.sh 搜索和安装社区 Skill | 不知道有什么 Skill 可用时的入口 |

**你会发现一个规律：越是"运维""部署""数据准备"这类事务性工作，越适合做成 Skill。** 因为它们步骤固定但细节多，人容易忘，但 Agent 记得住。

---

## 4. 实战案例：FICC 债券定价 —— 从任务到 Agent 的完整开发过程

这是我们目前最复杂的 Skill 组合案例，完整展示了从 Tool 到 Skill 再到 Agent 的进化路径。

### 第一步：确定任务与所需函数

**任务**：在 DolphinDB 中实现债券定价全流程——从数据准备到定价计算到可视化输出。

**关键参考**：
- DolphinDB FICC 模块文档：https://docs.dolphindb.cn/zh/modules/ficc/index.html
- 核心函数：`bondDirtyPriceFromYield`、`bondYieldFromDirtyPrice`、`bootstrapSwapCurve` 等

在这一步，你不需要写任何代码。只需要搞清楚两件事：
1. 最终交付物是什么？（定价结果表 + 风险指标 + 可视化报告）
2. 需要调用哪些底层函数？（查文档，列出来）

### 第二步：划分模块（拆成可独立开发的流程块）

整个任务拆成以下模块：

```
┌─────────────────────────────────────────────────────────┐
│                  FICC 债券定价全流程                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐         │
│  │ 1. 数据源  │──▶│ 2. 建库建表│──▶│ 3. 数据导入│         │
│  │ (通联 API) │   │ (Schema)  │   │ (Ingest)  │         │
│  └───────────┘   └───────────┘   └───────────┘         │
│        │                               │                │
│        ▼                               ▼                │
│  ┌───────────────────────────────────────────┐          │
│  │  4. 曲线构建 & 资产建模 & 定价计算          │          │
│  │  (Bootstrap + Pricing Pipeline)            │          │
│  └───────────────────────────────────────────┘          │
│                       │                                 │
│                       ▼                                 │
│  ┌───────────┐   ┌───────────┐                          │
│  │ 5. 风险计算│   │ 6. 可视化  │                          │
│  │ (Greeks)   │   │ (Report)  │                          │
│  └───────────┘   └───────────┘                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 第三步：分头开发多个 Skill

模块划出来之后，就可以并行开发了。每个模块对应一个独立的 Skill：

| 模块 | 对应 Skill | 职责边界 |
|------|-----------|---------|
| 1~3：数据准备 | `prepare_data_for_pricing` | 连通联 API 拉数据、建库建表、把原始数据灌入 DDB |
| 4~5：定价计算 | `pricing` | 基于标准化输入做曲线构建、资产定价、风险指标计算 |
| 底层执行 | `execute-dlang` | 所有 `.dos` 脚本的统一执行入口 |
| 可视化 | `ddb-visualization` | 把定价结果渲染成可交互 HTML 报告 |

**Skill 之间的依赖关系：**

```
prepare_data_for_pricing ──数据写入──▶ dfs://bond_pricing_workflow_v2
        │                                        │
        │  (都依赖)                               │ (读取)
        ▼                                        ▼
   execute-dlang ◀──────────────────────── pricing
                                              │
                                              ▼
                                      ddb-visualization
```

每个 Skill 都有明确的输入输出契约。比如 `prepare_data_for_pricing` 的产出是 `dfs://data_pricing_skill` 库中的标准化表，`pricing` 读取这些表做计算。这个"接口约定"非常重要——后面联调章节会讲为什么。

### 第四步：逐个开发每个 Skill（最耗时、也最有价值）

每个 Skill 的开发都遵循同一个节奏：

```
反复修改代码直到跑通 ──▶ 总结经验写成 SKILL.md
```

以 `prepare_data_for_pricing` 为例，我的实际开发过程：

1. **开一个 Copilot Chat 对话**，说："我要从通联数据 API 拉取债券基本信息和利率曲线数据，写入 DolphinDB"
2. AI 生成了第一版脚本，**跑不通**——通联 API 的字段名变了
3. 我把报错贴回去，AI 修正字段映射，**又跑不通**——DDB 建表的分区方式不对
4. 继续修，这次成功写入了数据，但 **缺少校验**——有空值没处理
5. 加了数据清洗逻辑，终于完整跑通
6. 我对 AI 说："把刚才的过程整理一下，生成 SKILL.md 和配套脚本"

**一个 Skill 的第一次开发通常要 3~5 小时**，大部分时间花在试错。但这些试错产生的经验，就是 Skill 的核心价值——下一个人跑同样的流程，5 分钟搞定。

脚本的组织建议按执行顺序编号：

```
scripts/
├── 10_probe_uqer_api.py            # 验证 API 连通性
├── 20_download_minimal_samples.py   # 下载最小数据集
├── 30_create_pricing_schema.dos     # 建库建表
├── 40_ingest_raw_to_ddb.py          # 数据导入
├── 50_run_case1_irs_pricing.dos     # 案例 1 验证
├── 60_run_case2_curve_bootstrap.dos # 案例 2 验证
└── 70_generate_standard_report.py   # 输出报告
```

### 第五步：联调 Skill（最容易被忽视的关键环节）

当每个 Skill 各自跑通之后，串起来很可能不通。常见问题：

| 问题类型 | 具体表现 | 解决方案 |
|---------|---------|---------|
| 命名不一致 | `prepare_data` 写入 `dfs://data_pricing_skill`，但 `pricing` 读的是 `dfs://bond_pricing_v2` | 统一约定库表名，写在 SKILL.md 的输入输出契约里 |
| 字段不匹配 | 上游输出 `bondCode`，下游期望 `securityId` | 在接口文档中明确字段映射 |
| 环境差异 | Skill A 在 3.00.2 版本开发，Skill B 要求 3.00.4 | 在 SKILL.md 中标注最低版本要求 |
| 执行顺序 | 下游 Skill 在上游还没写完数据时就开始读 | 在 Agent 编排中显式控制步骤依赖 |

**联调的核心原则：让每个 Skill 的通用性尽可能高。**

具体做法：
- 把硬编码的库名、表名、服务器地址提取为可配置参数
- 在 SKILL.md 中写清楚"我的输入是什么格式、我的输出是什么格式"
- 实际跑一遍两个 Skill 串联的全流程，发现不一致就立刻修

### 第六步：编写 Agent（把 Skill 编排成完整任务）

**Agent 是什么？** 我的理解是：

> **Agent = Bootstrap Prompt + Tools + Skills + Hooks 的上下文编排规则。**

具体到 FICC 定价这个场景：

```yaml
# agent.md（Agent 的 Bootstrap Prompt）

## 任务
你是一个 FICC 债券定价 Agent，负责完成从数据准备到定价输出的全流程。

## 边界
- 只做定价分析，不做交易执行
- 不处理实时行情，只做批量定价

## 执行流程
1. 数据准备阶段 → 使用 skill: prepare_data_for_pricing
2. 定价计算阶段 → 使用 skill: pricing
3. 结果可视化   → 使用 skill: ddb-visualization
4. 脚本执行     → 统一通过 skill: execute-dlang

## 约束
- 所有 DDB 脚本必须通过 execute-dlang 执行
- 数据库路径统一使用 dfs://bond_pricing_workflow_v2
- 出错时先检查数据完整性，再检查计算逻辑
```

**Agent 各组成部分的角色：**

| 组件 | 角色 | 以 FICC 定价为例 |
|------|------|----------------|
| **Bootstrap Prompt** (agent.md) | 定义任务范围、边界、执行顺序 | "你是定价 Agent，先准备数据再定价再出报告" |
| **Skills** | 提供每个阶段的方法论和步骤 | `prepare_data_for_pricing`、`pricing` 等 |
| **Tools** | 提供原子操作能力 | 文件读写、终端执行、DDB 连接 |
| **Hooks** | 某些流程必然触发的动作 | 启动 DDB session 时自动加载 FICC 模块；结束时自动释放资源 |

**从 Tool 到 Agent 的完整路径：**

```
Tool（原子能力）
  ↓  封装经验
Skill（可复用方法论）
  ↓  编排组合
Agent（自主完成复杂任务）
```

---

## 5. Skill 的文件结构与渐进式加载

### 5.1 标准目录结构

```text
your-skill/
├── SKILL.md              # 必需：主说明与执行指南（给 Agent 读的）
├── README.md             # 可选：给人读的说明
├── scripts/              # 可选：可执行代码（按编号排序）
├── reference/            # 可选：方法论、接口契约等参考资料
├── templates/            # 可选：模板文件
└── python/               # 可选：Python 辅助脚本
```

### 5.2 渐进式加载（Progressive Loading）

Agent 不会一次读完所有 Skill 的全部内容，而是分层按需加载：

| 层级 | 何时加载 | Token 消耗 | 内容 |
|------|---------|-----------|------|
| **L1: 元数据** | 启动时全部加载 | ~100 tokens / Skill | YAML frontmatter 中的 `name` 和 `description` |
| **L2: 指令** | 触发时加载 | < 5k tokens | SKILL.md 正文（步骤、指南、经验） |
| **L3+: 资源** | 按需加载 | 无上限 | scripts/、reference/ 中的文件，通过执行而非读入上下文 |

这意味着你可以在 `reference/` 里放 50 页的方法论文档也不会拖慢 Agent——它只在需要时才去读。

参考来源：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

### 5.3 SKILL.md 写作要点

1. **开头写清楚"做什么"和"不做什么"** —— 让 Agent 快速判断是否该用这个 Skill
2. **给出最小跑通路径** —— 先让人/Agent 能跑通一个最简单的 case
3. **标注输入输出契约** —— 我需要什么数据？我产出什么数据？格式是什么？
4. **记录踩过的坑** —— 这是 Skill 最宝贵的部分

---

## 6. 测试与迭代

### 6.1 验收标准

**一个人跑通，另一个人用同级模型也能跑通。**

具体测试维度：
1. **触发测试**：用户说"帮我做 XXX"时，Agent 是否自动选中了正确的 Skill？
2. **流程测试**：是否按预期步骤执行？中间出错时能否恢复？
3. **结果测试**：输出是否满足质量和格式标准？
4. **跨环境测试**：换一台服务器、换一个 DDB 版本，还能跑吗？

### 6.2 迭代节奏

| 阶段 | 耗时 | 状态 |
|------|------|------|
| 第一次开发 | 3~5 小时 | 踩坑期，大部分时间在试错 |
| 第二次使用 Skill | 30 分钟 | 明显提速，但会发现遗漏 |
| 第三次 + 迭代修正 | 5~10 分钟 | 趋于稳定 |
| N 次使用后 | 一键执行 | Skill 成熟，进入维护期 |

**类比：第一次骑自行车歪歪扭扭，后面越来越稳，最后你根本不需要想"怎么骑"。**

---

## 7. DolphinX Skills Market：共享与共建倡议

### 7.1 为什么要共享？

我一个人写了十几个 Skill，但公司里有几十个人在做类似的事情。如果每个人把自己踩的坑都写成 Skill 并共享出来，我们就拥有了一个组织级的"经验库"，新人上手的时间可以从"周"缩短到"小时"。

### 7.2 DolphinX Skills Market 倡议

我发起一个 **DolphinX Skills Market** 项目（GitHub 仓库），作为公司层面的 Skill 共享平台。

**核心机制：**

#### 1. 统一提交与 Review

- 所有 Skill 提交到统一的 GitHub 仓库
- 每个 Skill 必须署名（`metadata.author`）
- 提交后需经过至少一位同事 Review 后才进入"推荐列表"

#### 2. 评分与排名

| 评分维度 | 权重 | 说明 |
|---------|------|------|
| **可复现性** | 40% | 另一个人是否能一次跑通？ |
| **文档质量** | 25% | SKILL.md 是否清晰、有踩坑记录？ |
| **通用性** | 20% | 是否对环境、版本有过多假设？ |
| **社区反馈** | 15% | 点赞数、评论数、使用频率 |

#### 3. 定期联调与治理

Skill 多了之后，必然会遇到：
- **重复**：两个人写了功能类似的 Skill → 评审后合并为一个
- **冲突**：Skill A 的输出格式和 Skill B 的输入格式不匹配 → 制定统一的接口契约
- **过时**：DDB 版本升级后某些 API 变了 → 定期巡检，标记过时 Skill

建议每月做一次 Skills Review（可以结合周会的一个固定议题），内容就三件事：
1. 上一周期新提交了哪些 Skill？质量如何？
2. 有哪些 Skill 出现了冲突或重复，需要合并？
3. 有哪些 Skill 已经过时，需要更新或下线？

### 7.3 平台路线图

```
Phase 1（当前）: GitHub 仓库 + SKILL.md + README
  → 最小可用，大家先把 Skill 提上来

Phase 2: 简易局域网网站（DolphinX Skills Market）
  → 浏览所有共享 Skill、按热度排名
  → 热度 = 下载量 + commit 记录 + 点赞评论
  → 搜索功能、分类标签

Phase 3: 自动化集成
  → CI/CD 自动检测 Skill 格式合规性
  → 自动运行验收测试（在标准环境中跑一遍最小用例）
  → 自动生成 Skill 质量报告
```

### 7.4 如何贡献你的第一个 Skill

```
1. Fork skills 仓库
2. 在 .github/skills/ 下创建你的 Skill 目录
3. 至少包含一个 SKILL.md（参考本文档的格式和现有 Skill 的写法）
4. 提交 PR，写清楚：
   - 这个 Skill 解决什么问题
   - 你在什么环境下验证过
   - 有没有已知的局限性
5. 等待至少一位同事 Review 通过后合并
```

---

## 8. 结语

每个人总结 Skill 的方式都不可能完美——我自己写的这些 Skill 也还在不断迭代。但共享会让它们持续进化。

**我对 Skill 长期形态的判断：**

- **短中期**：Skill 是把个人经验变成组织能力的最佳介质。模型还不够强大的时候，Skill 就是它的"外挂记忆"。
- **长期**：随着模型能力增强，一部分基础 Skill 会被模型内化（就像你骑车熟练后不再需要念口诀），但领域专业 Skill（比如 FICC 定价）仍然会是核心资产。

**就像骑自行车：刚学时要记每个动作，熟练后不再显式思考。但"骑车"这个技能，永远住在你身体里。**

欢迎加入 DolphinX Skills Market，一起把"会做一次"变成"所有人都会做"。

---

## 附：参考资料

- Anthropic 官方 Skill 架构文档：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- skills.sh 社区浏览：https://skills.sh/
- 本技能配套参考文件：`references/` 目录
