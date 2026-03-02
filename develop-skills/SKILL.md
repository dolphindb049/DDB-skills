---
name: develop-skills
description: Agent Skill（Meta-Skill）开发指南。涵盖技能定义、渐进式加载、规划设计、测试迭代、分发共享、模式排错与企业落地实践。
license: MIT
metadata:
  author: jrzhang
  version: "2.0.0"
---

# The Complete Guide to Building Skills for DolphinDB

> 目标：把“会做一次”变成“可复用、可迁移、可规模化”的团队能力。

## 目录

1. 简介（Introduction）
2. 基础（Fundamentals）
3. 规划与设计（Planning and Design）
4. 测试与迭代（Testing and Iteration）
5. 分发与共享（Distribution and Sharing）
6. 模式与故障排除（Patterns and Troubleshooting）
7. 资源与结语（Resources and References）

---

## 1) 简介（Introduction）

### 1.1 什么是 Skill（用骑自行车解释）
- 自行车是 Tool（可类比 MCP / 工具能力）
- 把手、脚踏是通用交互接口（可类比 MCP 的统一协议）
- “骑自行车上班”是具体 Task
- “我（使用者）”是 Agent
- **Skill** 是“骑车”这套可复用、可迁移的方法论与步骤

一句话归纳：
**Skill 是一个可复用的、灵活的使用工具或完成任务的方法。**

边界澄清：
- 不能说“骑车上班”是 Skill（那是单次 Task）
- 不能说“自行车”是 Skill（那是 Tool）
- 不能说“我会骑车”是 Skill（那是 Agent 的能力状态）

### 1.2 为什么要做 Skill
- 避免每次任务都从 0 提示
- 把个人经验转换为组织资产
- 让 Agent 在不同场景下稳定复现结果
- 给工具层（MCP）增加“可执行工作流”的上层知识

---

## 2) 基础（Fundamentals）

### 2.1 Skill 文件结构

```text
your-skill/
├── SKILL.md              # 必需，主说明与执行指南
├── scripts/              # 可选，可执行代码
├── references/           # 可选，按需查阅资料
└── assets/               # 可选，模板、图标、字体等
```

### 2.2 渐进式加载（Progressive Loading）

| Level | When Loaded | Token Cost | Content |
| --- | --- | --- | --- |
| Level 1: Metadata | Always (at startup) | ~100 tokens per Skill | name and description from YAML frontmatter |
| Level 2: Instructions | When Skill is triggered | Under 5k tokens | SKILL.md body with instructions and guidance |
| Level 3+: Resources | As needed | Effectively unlimited | Bundled files executed via bash without loading contents into context |

参考来源：
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

### 2.3 为什么 Skill 不会像 Tool 一样“越多越乱”
1. **向上抽象**：细粒度 Skill 可持续合并为高阶 Skill（像“把稳车把 + 蹬脚踏”抽象成“骑车”）
2. **模型内化**：高频可复用工作流会逐步被更强模型学习吸收，外挂 Skill 可周期性精简

---

## 3) 规划与设计（Planning and Design）

### 3.1 从用例而不是从代码开始
先定义 2-3 个明确用例：
- Trigger：用户会怎么说
- Steps：必须经过哪些步骤
- Tooling：需要哪些内建能力 / MCP
- Success：何为“完成且可交付”

### 3.2 最简单、最有效的开发法
**执行任务 + 复盘沉淀**

以“服务器部署代理”为例：
1. 先让 Agent 执行复杂任务（可能会失败多次）
2. 记录关键报错、修复动作、最终成功路径
3. 让 AI 自动归纳为 Skill 文件夹（`SKILL.md + scripts + references`）
4. 在新环境复跑验证可迁移性

判断“经验是否高质量”：
- 不遗漏关键条件（权限、端口、依赖、鉴权）
- 不堆砌冗余噪声（无关日志、无意义过程）

---

## 4) 测试与迭代（Testing and Iteration）

### 4.1 验收标准（公司层面）
**一个人跑通，另一个人用同级模型也能跑通。**

建议测试维度：
1. 触发测试：是否在正确场景自动触发 Skill
2. 流程测试：是否按预期步骤执行且稳定收敛
3. 结果测试：输出是否满足质量和格式标准

### 4.2 迭代节奏
- 第一轮常常 3-4 小时（踩坑期）
- 第二轮导入 Skill 后明显提速
- 多轮迭代后达到“速度+准确”可接受阈值

类比：第一次骑车歪歪扭扭，后面越来越稳。

---

## 5) 分发与共享（Distribution and Sharing）

### 5.1 文档即 Skill（Doc as Skill）
旧范式：函数接口文档（给人读）
新范式：Skill 文档（给 Agent 可执行）

当文档以 Skill 组织后：
- 开发流程可被直接复用
- 文档不再只是“说明书”，而是“执行入口”
- 测试可围绕 Skill 用例自动化

### 5.2 在 DolphinX 的落地建议
- 以 Skill 为最小复用单元组织知识
- 以“跨模型可复现”作为上线门槛
- 在团队中持续共建与评审 Skill 资产库

---

## 6) 模式与故障排除（Patterns and Troubleshooting）

### 6.1 高价值模式（建议优先沉淀）
1. 顺序工作流编排（多步骤、可追踪）
2. 多工具协同（多个 MCP / 数据源联动）
3. 迭代式优化（先可用，再提质量）
4. 情境感知工具选择（按输入特征切换策略）
5. 领域特定智能（把行业 know-how 固化）

### 6.2 FICC 定价 Skill 示意（卖方视角）
目标：把“拉数据→曲线拟合→调用定价→结果验证”固化成一键可复用流程。

标准链路：
1. 获取市场数据（利率、汇率、波动率、合约条款）
2. 构建/拟合收益率曲线（含日计数、复利方式、插值外推）
3. 调用定价函数（债券、期权、互换等）
4. 输出并与基准系统核对（P&L / Greeks / 敏感性）

沉淀收益：
- 第一次慢（3-4h）
- 沉淀后快（分钟级）
- 跨人、跨环境可复现

---

## 7) 资源与结语（Resources and References）

### 7.1 参考资料
- 官方架构说明（Progressive Loading）：
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- 本目录参考：`references/`

### 7.2 结语
每个人总结 Skill 的方式都不可能完美，但共享会让它持续进化。

我对长期形态的判断：
- 短中期：Skill 是组织能力沉淀与复用的最佳介质
- 长期：随着模型内化增强，部分基础 Skill 会自然退场

就像骑车：刚学时要记动作，熟练后不再显式思考动作。

---

## 附：本 Skill 的建议配套文件

- `references/The-Complete-Guide-to-Building-Skill-for-Claude.zh.md`（PDF 全量翻译稿）
- `references/Skill-Development-Guide-v2.pptx`（会议演示）
- `references/online-meeting-brief.md`（在线分发文档）
- `scripts/ficc_pricing_example.dos`（FICC 示例脚本）
