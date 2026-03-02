# The Complete Guide to Building Skill for Claude（中文翻译）

## 第 1 页

面向 Claude 的完整技能提升指南

## 第 2 页

目录
简介
3
基础知识
4
规划与设计
7
测试与迭代
14
分发与共享
18
模式与故障排除
21
资源与参考文献
28
2

## 第 3 页

简介
技能是一组指令——打包成一个简单的文件夹——用于教会 Claude 如何处理特定任务或工作流。技能是定制 Claude 以满足你特定需求的最强大方式之一。与在每次对话中重新解释你的偏好、流程和领域专业知识不同，技能让你一次性教会 Claude，并在每次使用时受益。
当你有可重复的工作流时，技能就很有力量：从规格生成前端设计、以一致的方法进行研究、创建符合你团队风格指南的文档，或编排多步流程。它们与 Claude 的内置能力（如代码执行和文档创建）配合良好。对于那些构建 MCP 集成的人来说，技能增加了另一层强大的能力，帮助将原始工具访问转化为可靠、优化的工作流。
本指南涵盖构建有效技能所需了解的一切——从规划和结构到测试与分发。无论你是在为自己、你的团队，还是为社区构建技能，你都将发现实用的模式和真实世界的示例贯穿始终。

你将学到的内容：
• 技术要求和技能结构的最佳实践
• 独立技能与 MCP 增强工作流的模式
• 我们在不同用例中看到的行之有效的模式
• 如何测试、迭代和分发你的技能

本指南适用对象：
• 希望 Claude 始终遵循特定工作流的开发者
• 希望 Claude 遵循特定工作流的高级用户
• 希望在整个组织中标准化 Claude 的工作方式的团队

本指南的两条路径
构建独立技能？请关注基础、规划与设计，以及类别 1-2。增强 MCP 集成？请参考“技能 + MCP”章节和类别 3。两条路径共享相同的技术要求，但你可以选择与你的用例相关的部分。
本指南的收获：到最后，你将能够在一次性完成地构建一个可运行的技能。预计大约需要 15-30 分钟来使用 skill-creator 构建并测试你的首个可工作技能。
现在开始。

## 第 4 页

第1章
基础知识
4

## 第 5 页

第1章
基础
什么是技能（skill）？
一个技能是一个包含以下内容的文件夹：
•	 SKILL.md（必需）：以 Markdown 编写的说明，包含 YAML frontmatter
•	 scripts/（可选）：可执行代码（Python、Bash 等）
•	 references/（可选）：按需加载的文档
•	 assets/（可选）：用于输出的模板、字体、图标
核心设计原则
逐步披露（Progressive Disclosure）
技能使用三级系统：
•	 第一级（YAML frontmatter）：始终加载到 Claude 的系统提示中。提供足够的信息让 Claude 知道何时应使用每个技能，而无需将全部内容加载到上下文中。
•	 第二级（SKILL.md 正文）：当 Claude 认为该技能与当前任务相关时加载。包含完整的说明和指导。
•	 第三级（链接文件）：打包在技能目录中的附加文件，Claude 可以根据需要选择浏览和发现。
这种逐步披露在保持专门知识的同时最小化了令牌（token）使用。
可组合性（Composability）
Claude 可以同时加载多个技能。你的技能应能与其他技能良好协同，不要假定它是唯一可用的功能。
可移植性（Portability）
技能在 Claude.ai、Claude Code 和 API 中表现一致。只需创建一次技能，它即可在所有平台上工作而无需修改，前提是运行环境支持该技能所需的任何依赖项。
针对 MCP 构建者：技能 + 连接器（Skills + Connectors）
💡 在没有 MCP 的情况下构建独立技能？跳到 Planning and Design ——你随时可以返回此处。
如果你已经有一个可用的 MCP 服务器，那么艰难的部分已经完成。技能是置于其上的知识层——捕捉你已经掌握的工作流和最佳实践，以便 Claude 可以一致地应用它们。
厨房比喻
MCP 提供专业厨房：可以使用工具、原料和设备。
技能提供配方：逐步说明如何创造有价值的成果。
5

## 第 6 页

Together, they enable users to accomplish complex tasks without needing to figure out every step themselves.
他们共同让用户在无需自己逐步摸索的情况下完成复杂任务。

How they work together:
它们如何协同工作：

MCP (Connectivity)
MCP（连接性）

Skills (Knowledge)
技能（知识）

Connects Claude to your service
将 Claude 连接到您的服务（Notion、Asana、Linear 等）

Teaches Claude how to use your service effectively
教会 Claude 如何高效使用您的服务

Provides real-time data access and tool invocation
提供对实时数据的访问和工具调用

Captures workflows and best practices
捕捉工作流和最佳实践

What Claude can do
Claude 能做什么

How Claude should do it
Claude 应该如何做

Why this matters for your MCP users
这对您的 MCP 用户为何重要

Without skills:
没有技能时：

•  用户连接您的 MCP，但不知道下一步该做什么
•  支持工单，询问“如何通过您的集成实现 X”
•  每次对话都从头开始
•  结果不一致，因为用户每次提示不同
•  当真正的问题是工作流指导时，用户会责怪您的连接器

With skills:
有技能时：

•  预构建的工作流在需要时自动激活
•  一致、可靠的工具使用
•  在每次交互中嵌入最佳实践
•  降低您的集成的学习曲线

6

## 第 7 页

第2章
规划与设计
7

## 第 8 页

Chapter 2
规划与设计
Start with use cases
在编写任何代码之前，识别 2-3 个你的技能应能够实现的具体用例。
Good use case definition:
良好的用例定义：
Use Case: Project Sprint Planning
用例：项目冲刺规划
Trigger: User says "help me plan this sprint" or "create
sprint tasks"
触发：用户说“帮助我规划这个冲刺”或“创建冲刺任务”
Steps:
步骤：
1. Fetch current project status from Linear (via MCP)
1. 从 Linear（通过 MCP）获取当前项目状态
2. Analyze team velocity and capacity
2. 分析团队节奏与产能
3. Suggest task prioritization
3. 建议任务优先级
4. Create tasks in Linear with proper labels and estimates
4. 在 Linear 中创建带有适当标签和估算的任务
Result: Fully planned sprint with tasks created
结果：完成计划的冲刺，已创建任务
Ask yourself:
自问：
•	 What does a user want to accomplish?
•	 用户想要完成什么？
•	 What multi-step workflows does this require?
•	 这需要哪些多步骤的工作流？
•	 Which tools are needed (built-in or MCP?)
•	 需要哪些工具（内建还是 MCP？）
•	 What domain knowledge or best practices should be embedded?
•	 应该嵌入哪些领域知识或最佳实践？

Common skill use case categories
常见技能用例类别
At Anthropic, we’ve observed three common use cases:
在 Anthropic，我们观察到三种常见用例：
Category 1: Document & Asset Creation
类别 1：文档与资产创建
Used for: Creating consistent, high-quality output including documents,
用于：创建一致的、高质量的输出，包括文档、
presentations, apps, designs, code, etc.
演示、应用、设计、代码等。
Real example: frontend-design skill (also see skills for docx, pptx, xlsx, and
ppt)
实际示例：前端设计技能（另见 docx、pptx、xlsx 和
ppt)
"Create distinctive, production-grade frontend interfaces with high design
quality. Use when building web components, pages, artifacts, posters, or
applications."
“创建具有高设计质量的独特前端界面。用于构建网页组件、页面、制品、海报或应用时。”
Key techniques:
关键技术：
•	 Embedded style guides and brand standards
•	 嵌入式风格指南和品牌标准
•	 Template structures for consistent output
•	 用于一致输出的模板结构
•	 Quality checklists before finalizing
•	 在最终定稿前的质量检查清单
•	 No external tools required - uses Claude's built-in capabilities
•	 无需外部工具 — 使用 Claude 的内置能力
8

## 第 9 页

类别 2：工作流自动化
用途：多步骤流程，受益于一致的方法学，包括跨多个 MCP 服务器的协调。
真实示例：skill-creator 技能
“用于创建新技能的交互式指南。引导用户完成用例定义、frontmatter 生成、指令编写和验证。”
关键技术：
• 具有验证门的分步工作流
• 常见结构模板
• 内置的审查与改进建议
• 迭代式改进循环
类别 3：MCP 增强
用途：用于改进 MCP 服务器提供的工具访问的工作流指导。
真实示例：sentry-code-review 技能（来自 Sentry）
“通过其 MCP 服务器使用 Sentry 的错误监控数据，自动分析并修复 GitHub Pull Request 中检测到的错误。”
关键技术：
• 在序列中协调多个 MCP 调用
• 融入领域专业知识
• 提供用户本应自行指定的上下文信息
• 针对常见 MCP 问题的错误处理
定义成功标准
你将如何知道你的技能在工作？
这些是愿景目标——大致的基准，而非精确阈值。目标是严格，但也接受存在一定主观评估的成分。我们正在积极开发更稳健的测量指南和工具。
定量指标：
• 技能在相关查询中的触发率达到 90%
– 如何衡量：运行 10-20 个应该触发你的技能的测试查询。记录它自动加载的次数与需要显式调用的次数。
• 在 X 次工具调用中完成工作流
– 如何衡量：比较同一任务在启用技能与未启用技能时的差异。统计工具调用次数和总 token 消耗。
• 每个工作流中的 API 调用不应有失败
– 如何衡量：在测试运行期间监控 MCP 服务器日志。跟踪重试率和错误代码。
定性指标：
• 用户无需再向 Claude 请求下一步
– 如何评估：在测试过程中，记录需要重定向或澄清的频率。请 Beta 用户提供反馈。
• 工作流在无需用户修正的情况下完成
– 如何评估：对同一请求重复执行 3-5 次。比较输出在结构一致性和质量方面的一致性。
• 跨会话的一致性结果
– 如何评估：新用户能否在首次尝试时以最少的引导完成任务？
9

## 第 10 页

技术要求
文件结构
your-skill-name/
├── SKILL.md              # 必填 - 主技能文件
├── scripts/              # 可选 - 可执行代码
│   ├── process_data.py # 示例
│   └── validate.sh # 示例
├── references/           # 可选 - 文档
│   ├── api-guide.md # 示例
│   └── examples/ # 示例
└── assets/              # 可选 - 模板等
└── report-template.md # 示例
关键规则
SKILL.md 命名：
•	 必须严格为 SKILL.md（区分大小写）
•	 不接受任何变体（SKILL.MD、skill.md 等）
技能文件夹命名：
•	 使用 kebab-case: notion-project-setup ✅
•	 不允许有空格: Notion Project Setup ❌
•	 不允许下划线: notion_project_setup ❌
•	 不允许大写字母: NotionProjectSetup ❌
不包含 README.md：
•	 不要在你的技能文件夹内包含 README.md
•	 所有文档放在 SKILL.md 或 references/ 中
•	 注：通过 GitHub 分发时，你仍然需要一个仓库级别的 README 供人类用户使用 — 参见 分发与共享。
YAML 前置元数据：最重要的部分
YAML 前置元数据是 Claude 决定是否加载你的技能的依据。务必设置正确。
最小必需格式
---
name: your-skill-name
description: What it does. Use when user asks to [specific
phrases].
---
这就是你开始所需的全部。
字段要求
name（必填）：
•	 仅限 kebab-case
•	 不含空格或大写字母
•	 应与文件夹名称匹配
description（必填）：
•	 必须同时包含以下两项：
– 技能的作用
– 何时使用它（触发条件）
•	 少于 1024 字符
•	 不包含 XML 标签（< 或 >）
•	 包含用户可能说出的具体任务
•	 如相关，提及文件类型
10

## 第 11 页

license (optional):
• 如将技能开源时使用
• 常见：MIT、Apache-2.0
compatibility (optional)
• 1-500 字符
• 表示环境要求：例如目标产品、所需系统、包、网络访问需求等。
metadata (optional):
• 任何自定义键值对
• 建议：author、version、mcp-server
• 示例：
```yaml
metadata:
author: ProjectHub
version: 1.0.0 mcp-server: projecthub
```
Security restrictions
Forbidden in frontmatter:
• XML 角括号（< >）
• 名称中包含 "claude" 或 "anthropic" 的技能（保留）
原因：Frontmatter 出现在 Claude 的系统提示中。恶意内容可能
注入指令。
Writing effective skills
The description field
根据 Anthropic 的工程博客：“这段元数据...提供了足够的信息，让 Claude 知道在何时应使用每个技能，而无需把所有信息加载到上下文中。” 这是渐进式披露的第一层。
结构：
[What it does] + [When to use it] + [Key capabilities]
优秀描述示例：
# Good - specific and actionable
description: Analyzes Figma design files and generates
developer handoff documentation. Use when user uploads .fig
files, asks for "design specs", "component documentation", or
"design-to-code handoff".
# Good - includes trigger phrases
description: Manages Linear project workflows including sprint
planning, task creation, and status tracking. Use when user
mentions "sprint", "Linear tasks", "project planning", or asks
to "create tickets".
# Good - clear value proposition
description: End-to-end customer onboarding workflow for
PayFlow. Handles account creation, payment setup, and
subscription management. Use when user says "onboard new
customer", "set up subscription", or "create PayFlow account".
11

## 第 12 页

错误描述示例：
# 太模糊
description: 帮助完成项目。
# 缺少触发条件
description: 创建复杂的多页文档系统。
# 过于技术化，缺少用户触发条件
description: 实现带有分层关系的 Project 实体模型。

撰写主要指令
在前置信息（frontmatter）之后，用 Markdown 编写实际指令。

推荐结构：
将此模板适用于你的技能。用你的具体内容替换方括号中的部分。
---
name: your-skill
description: [...]
---
# 你的技能名称
## 指令
### 步骤 1: [第一个主要步骤]
清晰说明将发生的事情。
示例：
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
预期输出：[描述成功的样子]
(根据需要添加更多步骤)
示例
示例 1: [常见情景]
用户说: "设置一个新的营销活动"
操作：
1.  通过 MCP 获取现有活动
2.  根据提供的参数创建新活动
结果：活动已创建，附带确认链接
(根据需要添加更多示例)
故障排除
错误: [常见错误信息]
原因: [为何会发生]
解决方案: [如何修复]
(根据需要添加更多错误案例)
12

## 第 13 页

指令的最佳实践
具体且可执行
✅  好的：
运行 `python scripts/validate.py --input {filename}` 以检查数据格式。
如果验证失败，常见问题包括：
- 缺少必填字段（请将它们添加到 CSV 中）
- 日期格式无效（使用 YYYY-MM-DD）
❌  错误：
在继续之前验证数据。
包含错误处理机制
## 常见问题
### MCP 连接失败
如果你看到 "Connection refused"：
1. 验证 MCP 服务器是否正在运行：检查 设置 > 扩展
2. 确认 API 密钥有效
3. 尝试重新连接：设置 > 扩展 > [你的服务] > 重新连接
清晰引用打包的资源
在编写查询之前，请查阅 `references/api-patterns.md` 以获取：
- 速率限制相关指引
- 分页模式
- 错误代码及处理
使用分步披露信息
让 SKILL.md 专注于核心指令。将详细文档移动到 `references/` 并链接到它。 (有关三层系统如何工作，请参阅 Core Design Principles。)
13

## 第 14 页

第3章
测试与迭代
14

## 第 15 页

第3章
测试与迭代

技能可以根据你的需求在不同程度的严格性下进行测试：
• 手动测试在 Claude.ai - 直接运行查询并观察行为。快速迭代，无需设置。
• 在 Claude Code 上进行脚本化测试 - 自动化测试用例，以在变更之间实现可重复的验证。
• 通过 skills API 进行编程化测试 - 构建在定义的测试集上系统性运行的评估套件。
选择与您的质量要求和技能的可见性相匹配的方法。由小团队内部使用的技能与部署给成千上万企业用户的技能有着不同的测试需求。
专业提示：在扩展之前先在单个任务上迭代
我们发现，最有效的技能创建者在单个具有挑战性的任务上迭代直到 Claude 成功，然后将获胜的方法提取到一个技能中。这利用 Claude 的上下文学习，并比广泛测试提供更快的信号。一旦你有了可工作的基础，扩展到多个测试用例以实现覆盖。

推荐的测试方法
基于早期经验，有效的技能测试通常覆盖三个方面：
1. 触发测试
目标：确保你的技能在正确的时间加载。
测试用例：
• ✅  在明显任务上触发
• ✅  对改述请求触发
• ❌  不会对不相关的主题触发
示例测试套件：
应触发：
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"
- "Initialize a ProjectHub project for Q4 planning"
应不触发：
- "What's the weather in San Francisco?"
- "Help me write Python code"
- "Create a spreadsheet" (unless ProjectHub skill handles sheets)
15

## 第 16 页

2. Functional tests
目标: 验证技能产生正确输出。
测试用例:
•	 生成有效输出
•	 API 调用成功
•	 错误处理可用
•	 覆盖边界情况
示例:
测试: 创建包含 5 个任务的项目
给定: 项目名称 "Q4 Planning"，5 条任务描述
当: 技能执行工作流
则:
- 已在 ProjectHub 中创建项目
- 已创建 5 个具有正确属性的任务
- 所有任务链接到该项目
- 无 API 错误

3. Performance comparison
性能对比
目标：证明该技能相较于基线能够提高结果。
使用 Define Success Criteria 中的指标。下面给出一个对比的示意。
基线对比:
没有技能:
- 用户每次提供指令
- 15 条往返消息
- 3 次需要重试的 API 调用失败
- 消耗 12,000 令牌
有技能:
- 自动化工作流执行
- 仅需 2 个澄清性问题
- 0 次 API 调用失败
- 消耗 6,000 令牌
使用 skill-creator 技能
skill-creator 技能 - 可通过 Claude.ai 的插件目录或
下载用于 Claude Code 的版本 - 能帮助你构建并迭代技能。如果你有 MCP 服务器并且了解你最关心的 2–3 个工作流，你可以在一次性完成的时间内构建并测试一个
功能性技能 - 往往只需 15–30 分钟。
创建技能:
•	 通过自然语言描述生成技能
•	 生成带有 frontmatter 的正确格式的 SKILL.md
•	 建议触发短语和结构
评审技能:
•	 标记常见问题（描述含糊、缺失触发、结构性问题）
•	 识别潜在的过度触发/不足触发风险
•	 基于技能的既定目的提出测试用例
迭代改进:
•	 在使用技能并遇到边界情况或失败后，将那些示例带回 skill-creator
•	 例如：“使用本次对话中识别的问题与解决方案来改进技能如何处理 [具体边界情况]”
16

## 第 17 页

使用方法：
"Use the skill-creator skill to help me build a skill for
[your use case]"
注意：skill-creator 可以帮助你设计和完善技能，但不执行自动化测试套件或产生定量评估结果。
基于反馈的迭代
技能是动态文档。计划基于以下内容进行迭代：
触发不足信号：
•	 技能在应加载时未加载
•	 用户手动启用它
•	 关于何时使用它的支持性问题
解决方案：在描述中增加更多细节和微妙之处——这可能包括针对技术术语的关键词
过度触发信号：
•	 技能在无关查询上加载
•	 用户禁用它
•	 对用途的困惑
解决方案：增加负触发器，更加具体
执行问题：
•	 结果不一致
•	 API 调用失败
•	 需要用户纠错
解决方案：改进说明，增加错误处理
17

## 第 18 页

第四章
分发与共享
18

## 第 19 页

第4章
分发与共享
技能让你的 MCP 集成更加完整。随着用户比较连接器，具备技能的方案提供更快的实现价值的路径，让你在仅使用 MCP 的替代方案中占据优势。

当前分发模型（January 2026）
个人用户获取技能的方式：
1.  下载技能文件夹
2.  将文件夹压缩为 ZIP（如需要）
3.  通过 Settings > Capabilities > Skills 将其上传到 Claude.ai
4.  或放置在 Claude Code 技能目录中

组织级技能：
•  管理员可以在整个工作区部署技能（于 2025 年 12 月 18 日上线）
•  自动更新
•  集中化管理

开放标准
我们已将 Agent Skills 作为开放标准发布。与 MCP 类似，我们相信技能应在工具和平台之间具有可移植性——同一个技能无论你是使用 Claude 还是其他 AI 平台都应能工作。也就是说，某些技能被设计为充分利用特定平台的能力；作者可以在技能的兼容性字段中注明这一点。我们一直在与生态系统成员就这一标准进行合作，并对早期采用感到兴奋。

通过 API 使用技能
对于编程用例——例如构建应用、代理或利用技能的自动化工作流——API 提供对技能管理与执行的直接控制。

关键能力：
•  `/v1/skills` 端点用于列出和管理技能
•  通过 `container.skills` 参数将技能添加到 Messages API 请求中
•  通过 Claude Console 进行版本控制和管理
•  与 Claude Agent SDK 一起用于构建自定义代理

何时通过 API vs. Claude.ai 使用技能：
使用场景 | 最佳呈现界面
直接与技能交互的终端用户 | Claude.ai / Claude Code
在开发阶段进行手动测试与迭代 | Claude.ai / Claude Code
独立的、临时工作流 | Claude.ai / Claude Code
应用程序以编程方式使用技能 | API
在规模化生产部署 | API
自动化管道和代理系统 | API

19

## 第 20 页

注：API 中的技能需要 Code Execution Tool 测试版，该工具提供技能运行所需的安全环境。

如需实现细节，请参阅：
• Skills API Quickstart
• Create Custom skills
• Skills in the Agent SDK

Recommended approach today
目前的推荐做法
Start by hosting your skill on GitHub with a public repo, clear README (for human visitors — this is separate from your skill folder, which should not contain a README.md), and example usage with screenshots. Then add a section to your MCP documentation that links to the skill, explains why using both together is valuable, and provides a quick-start guide.
从在 GitHub 上托管你的技能开始，使用公开仓库、清晰的 README（供人类访问——这与你的技能文件夹分离，技能文件夹中不应包含 README.md），以及带有截图的示例用法。然后在你的 MCP 文档中添加一个链接到该技能的章节，解释同时使用两者为何有价值，并提供快速入门指南。

1. Host on GitHub
1. 在 GitHub 上托管
– Public repo for open-source skills
– Clear README with installation instructions
– Example usage and screenshots
– 开源技能的公开仓库
– 包含安装说明的清晰 README
– 示例用法和截图

2. Document in Your MCP Repo
2. 在你的 MCP 仓库中编写文档
– Link to skills from MCP documentation
– Explain the value of using both together
– Provide quick-start guide
– 在 MCP 文档中链接到技能
– 解释两者搭配使用的价值
– 提供快速入门指南

3. Create an Installation Guide
3. 创建安装指南
## Installing the [Your Service] skill
## 安装 [Your Service] 技能
1. Download the skill:
1. 下载技能：
- Clone repo: `git clone https://github.com/yourcompany/ skills`
- Or download ZIP from Releases
- 克隆仓库：`git clone https://github.com/yourcompany/ skills`
- 或从 Releases 下载 ZIP

2. Install in Claude:
2. 在 Claude 中安装：
- Open Claude.ai > Settings > skills
- Click "Upload skill"
- Select the skill folder (zipped)
- 打开 Claude.ai > 设置 > 技能
- 点击“上传技能”
- 选择技能文件夹（压缩包）

3. Enable the skill:
3. 启用技能：
- Toggle on the [Your Service] skill
- Ensure your MCP server is connected
- 打开 [Your Service] 技能的开关
- 确保你的 MCP 服务器已连接

4. Test:
4. 测试：
- Ask Claude: "Set up a new project in [Your Service]"
- 向 Claude 提问：“在 [Your Service] 中设置一个新项目”

Positioning your skill
定位你的技能
How you describe your skill determines whether users understand its value and actually try it. When writing about your skill—in your README, documentation, or marketing - keep these principles in mind.
你如何描述你的技能将决定用户是否理解其价值并实际去尝试。在写作关于你的技能的内容时——在你的 README、文档或市场推广中——请牢记以下原则。

Focus on outcomes, not features:
聚焦于结果，而非功能：
✅  Good:
"The ProjectHub skill enables teams to set up complete project workspaces in seconds — including pages, databases, and templates — instead of spending 30 minutes on manual setup."
✅  好：
“ProjectHub 技能让团队在几秒钟内创建完整的项目工作区——包括页面、数据库和模板——而无需花费 30 分钟进行手动设置。”

❌  Bad:
"The ProjectHub skill is a folder containing YAML frontmatter and Markdown instructions that calls our MCP server tools."
❌  不好：
“ProjectHub 技能是一个包含 YAML frontmatter 和 Markdown 指令的文件夹，用于调用我们的 MCP 服务器工具。”

Highlight the MCP + skills story:
突出 MCP + 技能 的故事：
"Our MCP server gives Claude access to your Linear projects. Our skills teach Claude your team's sprint planning workflow. Together, they enable AI-powered project management."
“我们的 MCP 服务器让 Claude 访问你的 Linear 项目。我们的技能教 Claude 你们团队的冲刺计划工作流。它们共同实现 AI 驱动的项目管理。”

20

## 第 21 页

第5章
模式与
故障排除
21

## 第 22 页

第5章
模式与故障排除
这些模式源自早期采用者和内部团队所创建的技能。它们代表我们所见的常见做法，而不是规定性的模板。

选择你的方法：问题优先 vs. 工具优先
把它想象成家得宝。你可能带着一个问题走进来——“我需要修理一个厨房橱柜”——员工会把你指向合适的工具。或者你可能挑选一个新的钻头，问如何把它用于你的具体工作。
技能的运作方式也类似：
• 问题优先： "I need to set up a project workspace" → 你的技能按正确的顺序编排合适的 MCP 调用。用户描述结果；技能处理工具。
• 工具优先： "I have Notion MCP connected" → 你的技能教会 Claude 最优工作流和最佳实践。用户有访问权限；技能提供专业知识。

大多数技能偏向一个方向。了解哪种框架更适合你的用例，有助于你在下面选择正确的模式。

模式 1：顺序工作流编排
适用场景：你的用户需要按特定顺序的多步骤流程。

示例结构：
## 工作流：新客户入职
### 步骤 1：创建账户
调用 MCP 工具：`create_customer`
参数：name、email、company
### 步骤 2：设置支付
调用 MCP 工具：`setup_payment_method`
等待：payment method verification
### 步骤 3：创建订阅
调用 MCP 工具：`create_subscription`
参数：plan_id、customer_id（来自步骤 1）
### 步骤 4：发送欢迎邮件
调用 MCP 工具：`send_email`
模板：welcome_email_template

关键技巧：
• 明确的步骤排序
• 步骤之间的依赖关系
• 各阶段的验证
• 失败时的回滚说明

22

## 第 23 页

模式 2：多 MCP 协作
适用场景：工作流跨越多个服务。
示例：从设计到开发的交接
### 阶段 1：设计导出（Figma MCP）
1. 从 Figma 导出设计资产
2. 生成设计规格
3. 创建资产清单
### 阶段 2：资产存储（Drive MCP）
1. 在 Drive 中创建项目文件夹
2. 上传所有资产
3. 生成可分享的链接
### 阶段 3：任务创建（Linear MCP）
1. 创建开发任务
2. 将资产链接附加到任务
3. 指派给工程团队
### 阶段 4：通知（Slack MCP）
1. 将交接摘要发布到 #engineering
2. 包含资产链接和任务引用
关键技术：
• 清晰的阶段分离
• MCP 之间的数据传递
• 在进入下一个阶段前进行验证
• 集中式错误处理

模式 3：迭代式改进
适用场景：输出质量通过迭代得到提升。
示例：报告生成
## 迭代式报告创建
### 初始草稿
1. 通过 MCP 获取数据
2. 生成第一份草稿报告
3. 保存到临时文件
### 质量检查
1. 运行验证脚本：`scripts/check_report.py`
2. 识别问题：
- 缺失的章节
- 格式不一致
- 数据验证错误
### 精炼循环
1. 解决每个识别出的问题
2. 重新生成受影响的部分
3. 重新验证
4. 重复直到达到质量阈值
### 最终化
1. 应用最终格式
2. 生成摘要
3. 保存最终版本
关键技术：
• 明确的质量标准
• 迭代改进
• 验证脚本
• 了解何时停止迭代
23

## 第 24 页

模式4：情境感知的工具选择
Use when: Same outcome, different tools depending on context.
适用场景：相同结果，但工具因上下文而异。

Example: File storage
示例：文件存储

## Smart File Storage
## 智能文件存储

### Decision Tree
### 决策树

1. Check file type and size
1. 检查文件类型和大小

2. Determine best storage location:
2. 确定最佳存储位置：

- Large files (>10MB): Use cloud storage MCP
- 大文件（>10MB）：使用云存储 MCP

- Collaborative docs: Use Notion/Docs MCP
- 协作文档：使用 Notion/Docs MCP

- Code files: Use GitHub MCP
- 代码文件：使用 GitHub MCP

- Temporary files: Use local storage
- 临时文件：使用本地存储

### Execute Storage
### 执行存储

Based on decision:
根据决策：

- Call appropriate MCP tool
- 调用相应的 MCP 工具

- Apply service-specific metadata
- 应用服务特定元数据

- Generate access link
- 生成访问链接

### Provide Context to User
### 向用户提供上下文

Explain why that storage was chosen
解释为何选择该存储

Key techniques:
关键技术：

•	 Clear decision criteria
•	 清晰的决策条件

•	 Fallback options
•	 回退选项

•	 Transparency about choices
•	 对选择的透明度

Pattern 5: Domain-specific intelligence
模式5：领域特定智能

Use when: Your skill adds specialized knowledge beyond tool access.
适用场景：你的专业知识超出对工具的获取能力。

Example: Financial compliance
示例：金融合规

## Payment Processing with Compliance
## 带合规的支付处理

### Before Processing (Compliance Check)
### 处理前（合规检查）

1. Fetch transaction details via MCP
1. 通过 MCP 获取交易详情

2. Apply compliance rules:
2. 应用合规规则：

- Check sanctions lists
- 检查制裁名单

- Verify jurisdiction allowances
- 验证辖区准入

- Assess risk level
- 评估风险等级

3. Document compliance decision
3. 记录合规决策

### Processing
### 处理

IF compliance passed:
如果合规通过：

- Call payment processing MCP tool
- 调用支付处理 MCP 工具

- Apply appropriate fraud checks
- 应用相应的欺诈检测

- Process transaction
- 处理交易

ELSE:
否则：

- Flag for review
- 标记以供复审

- Create compliance case
- 创建合规案例

### Audit Trail
### 审计轨迹

- Log all compliance checks
- 记录所有合规检查

- Record processing decisions
- 记录处理决策

- Generate audit report
- 生成审计报告

Key techniques:
关键技术：

•	 Domain expertise embedded in logic
•	 将领域专长嵌入到逻辑中

•	 Compliance before action
•	 先合规再行动

•	 Comprehensive documentation
•	 完整的文档

•	 Clear governance
•	 清晰的治理

24

## 第 25 页

故障排除
技能无法上传
错误：“在上传的文件夹中未找到 SKILL.md”
原因：文件名未严格命名为 SKILL.md
解决方案：
• 将其重命名为 SKILL.md（区分大小写）
• 验证：ls -la 应显示 SKILL.md
错误：“Invalid frontmatter”
原因：YAML 格式问题
常见错误：
# Wrong - missing delimiters
name: my-skill
description: Does things
# Wrong - unclosed quotes
name: my-skill
description: "Does things
# Correct
---
name: my-skill
description: Does things
---

错误：“Invalid skill name”
原因：名称中有空格或大写字母
# Wrong
name: My Cool Skill
# Correct
name: my-cool-skill
技能不会触发
症状：技能从不自动加载
修复：
修改你的描述字段。参阅 The Description Field 以获取良好/不良示例。
快速清单：
• 它是否过于笼统？（“有助于项目”之类的描述不会起作用）
• 是否包含用户实际会说的触发短语？
• 是否在必要时提及相关的文件类型？
调试方法：
向 Claude 询问：“何时会使用 [skill name] 技能？” Claude 将把描述原文引用回来。根据缺失的部分进行调整。
技能触发过于频繁
症状：技能对无关查询也会触发加载
解决方案：
1. 添加负触发条件
description: Advanced data analysis for CSV files. Use for
statistical modeling, regression, clustering. Do NOT use for
simple data exploration (use data-viz skill instead).
25

## 第 26 页

2. 更具体
# Too broad
description: 处理文档
# More specific
description: 处理用于合同审查的 PDF 法律文档
3. 明确范围
description: PayFlow 的电子商务支付处理。仅用于在线支付工作流，而非一般财务查询。
MCP 连接问题
症状: 技能加载但 MCP 调用失败
清单:
1. 验证 MCP 服务器是否已连接
– Claude.ai: 设置 > 扩展 > [您的服务]
– 应显示 “已连接” 状态
2. 验证身份验证
– API 密钥有效且未过期
– 已授予正确的权限/作用域
– OAuth 令牌已刷新
3. 独立测试 MCP
– 让 Claude 直接调用 MCP（不通过技能）
– “使用 [Service] MCP 来获取我的项目”
– 如果这失败，问题在 MCP 而非技能
4. 验证工具名称
– 技能引用的 MCP 工具名称正确
– 查看 MCP 服务器文档
– 工具名称区分大小写
Instructions not followed
症状: 技能加载但 Claude 未遵循指示
常见原因:
1. 指示过于冗长
– 保持指示简洁
– 使用项目符号和编号列表
– 将详细参考移到单独的文件
2. 指示被埋没
– 将关键指示放在顶部
– 使用 ## Important 或 ## Critical 标题
– 如有需要，重复要点
3. 模糊的语言
# Bad
确保正确验证事物
# Good
CRITICAL: 在调用 create_project 之前，请验证：
- 项目名称不能为空
- 至少分配一个团队成员
- 开始日期不在过去
高级技巧：对于关键验证，考虑打包一个脚本，按编程方式执行检查，而不是依赖语言指令。代码是确定性的；语言解释不是。请参阅 Office 技能中的该模式示例。
4. 模型“懒惰”
添加明确的鼓励：
## 性能说明
- 认真彻底地完成
- 质量比速度更重要
- 不要跳过验证步骤
注：将此添加到用户提示中比在 SKILL.md 中更有效
26

## 第 27 页

上下文容量过大问题
症状：技能似乎变慢或响应变差
原因：
• 技能内容过大
• 同时启用的技能数量过多
• 所有内容一次性加载，而非渐进式披露
解决方案：
1. 优化 SKILL.md 的大小
– 将详细文档移至 references/
– 链接到参考文献而非内联
– 将 SKILL.md 保持在 5,000 字以内
2. 减少启用的技能
– 评估是否有超过 20-50 个技能同时启用
– 建议有选择地启用
– 考虑为相关能力提供技能“包”
27

## 第 28 页

第六章
资源与
参考文献
28

## 第 29 页

第6章
资源与参考资料
如果你正在构建你的第一项技能，请先从最佳实践指南开始，然后在需要时参考 API 文档。
官方文档
Anthropic 资源：
• 最佳实践指南
• 技能文档
• API 参考
• MCP 文档
博客文章：
• 介绍代理技能
• 工程博客：为现实世界装备代理
• 技能解释
• 如何为 Claude 创建技能
• 为 Claude Code 构建技能
• 通过技能改进前端设计
示例技能
公共技能仓库：
• GitHub: anthropics/skills
• 包含你可以自定义的 Anthropic 创建的技能
工具与实用程序
skill-creator 技能：
• 内置于 Claude.ai，并可用于 Claude Code
• 能从描述生成技能
• 评审并提供建议
• 使用："Help me build a skill using skill-creator"
验证：
• skill-creator 可以评估你的技能
• 问题："审查此技能并提出改进建议"
获取支持
技术问题：
• 常见问题：在 Claude 开发者 Discord 的社区论坛
错误报告：
• GitHub Issues: anthropics/skills/issues
• 包含：技能名称、错误信息、复现步骤
29

## 第 30 页

参考 A：快速检查清单
使用此检查清单在上传前后验证您的技能。如果您想更快速地开始，请使用 skill-creator 技能来生成第一份草稿，然后逐条执行本清单，以确保没有遗漏。

开始前
- 已识别 2-3 个具体用例
- 已识别的工具（内置或 MCP）
- 已审阅本指南及示例技能
- 已规划文件夹结构

开发过程中
- 文件夹名采用 kebab-case
- SKILL.md 文件存在（拼写完全正确）
- YAML frontmatter 使用 --- 分隔符
- name 字段：kebab-case、无空格、无大写字母
- description 包含 WHAT 与 WHEN
- 任意处均无 XML 标签（< >）
- 指令清晰且可操作
- 包含错误处理
- 提供示例
- 引用清晰链接

上传前
- 已测试对明显任务的触发
- 已测试对改写请求的触发
- 已验证对无关主题不触发
- 功能测试通过
- 工具集成可用（如适用）
- 已压缩为 .zip 文件

上传后
- 在实际对话中测试
- 监控触发不足/过度触发
- 收集用户反馈
- 迭代描述和说明
- 在元数据中更新版本
30

## 第 31 页

参考 B：YAML
frontmatter
必填字段
---
name: skill-name-in-kebab-case
description: 它的作用及使用时机。请包含具体
触发短语。
---

所有可选字段
name: skill-name
description: [需要描述]
license: MIT # 可选：开源许可证
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch" # 可选：
限制工具访问
metadata: # 可选：自定义字段
author: 公司名称
version: 1.0.0
mcp-server: server-name
category: 生产力
tags: [项目管理, 自动化]
documentation: https://example.com/docs
support: support@example.com
安全说明
允许：
•  任意标准 YAML 类型（字符串、数字、布尔值、列表、对象）
•  自定义元数据字段
•  长描述（最多 1024 个字符）
禁止：
•  XML 角括号（< >）- 安全限制
•  YAML 中的代码执行（使用安全的 YAML 解析）
•  名称以 "claude" 或 "anthropic" 前缀的技能（保留）
31

## 第 32 页

参考 C：完整技能
示例
对于完整、可投入生产的技能，展示本指南中的模式：
• 文档技能 - PDF、DOCX、PPTX、XLSX 创建
• 示例技能 - 各种工作流模式
• 合作伙伴技能目录 - 查看来自不同合作伙伴的技能，例如 Asana、Atlassian、Canva、Figma、Sentry、Zapier 等
这些仓库保持最新，并包含本指南未覆盖的额外示例。将它们克隆下来，根据你的用例进行修改，并将它们用作模板。
32

## 第 33 页

claude.ai
