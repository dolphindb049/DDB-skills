# 基本概念：Agent、Workspace、Skills、Tools、Sandbox

这份文档只讲当前常见 Agent 开发里的基础概念，不讲空泛定义，直接结合 pi-mono 说明。

## 1. Agent 是什么

可以把 Agent 理解成一套“受约束的 LLM 运行设定”：

- 它背后连接的是一个 LLM。
- 它不是裸模型，而是带着固定系统提示词、工具列表、上下文加载规则一起运行。
- 它通常只被允许访问一部分能力，而不是整台机器的全部能力。
- 它的行为边界，来自 prompt、workspace、tools、resource loading 和运行环境共同约束。

所以，Agent 不是“一个会聊天的模型”，而是：

```text
Agent = LLM + System Prompt + Context Loading + Tools + Runtime Constraints
```

举例：在 pi-mono 的 `pi-coding-agent` 里，默认就是一个最小 coding agent。公开文档明确写了默认给模型 4 个工具：

- `read`
- `write`
- `edit`
- `bash`

这 4 个工具就决定了它的基础能力边界。它不是“什么都能做”，而是只能在这 4 个动作上做组合。

## 2. Workspace 是什么

Workspace 是 Agent 工作的项目上下文，不只是一个目录。

它通常包含：

- 当前工作目录
- 项目文件
- 项目级说明文件
- 项目里发现到的 skills、prompts、extensions
- 项目自己的运行约定

在 pi-mono 的公开文档里，`cwd` 决定当前工作目录；`DefaultResourceLoader` 会从当前目录、祖先目录和全局目录里发现资源。也就是说，workspace 既是文件系统范围，也是“上下文发现范围”。

## 3. Tools 是什么

Tool 是给 Agent 的原子能力。

特点：

- 粒度小，通常是一个明确动作
- 输入输出结构稳定
- 适合做单步操作
- 更像函数，不像流程

还是用 pi-mono 举例：

- `read`: 读文件
- `bash`: 执行命令
- `edit`: 做精确文本替换
- `write`: 创建或覆盖文件

pi-mono 也有更多内置工具可选：

- `grep`
- `find`
- `ls`

但默认仍然只启用前 4 个。这说明一个很重要的设计思想：**默认工具越少，模型越不容易乱用能力。**

## 4. Skill 是什么

Skill 不是一个函数，而是一组“按需加载的方法论和资源包”。

它通常包括：

- 什么时候该用它
- 做这件事的步骤
- 配套脚本
- 参考文档
- 常见踩坑

在 pi-mono 的技能机制里，Skill 是渐进式加载的：

1. 启动时先扫描 skill 目录，只把 `name` 和 `description` 放进系统提示词。
2. 当用户任务匹配到某个 skill 时，Agent 再用 `read` 去读取完整的 `SKILL.md`。
3. 如果 `SKILL.md` 里引用了 `scripts/`、`references/`、`assets/`，再按需继续读取或执行。

这就是 progressive disclosure。结论很简单：

- 始终在上下文里的，只应该是“短描述”。
- 真正的长文、脚本、细节，应该延后加载。

## 5. agent.md、AGENTS.md、SKILL.md 分别是什么

不同 Agent 框架名字不完全一样，但语义大致相同。

### 5.1 agent.md / AGENTS.md

它们一般是“总是加载”的项目级说明。

常见用途：

- 项目规则
- 代码风格
- 运行命令
- 人和 Agent 都要遵守的约束
- 当前仓库的工作方法

pi-mono 当前公开文档里，直接支持的是：

- `AGENTS.md`
- `CLAUDE.md`
- `.pi/SYSTEM.md`
- `APPEND_SYSTEM.md`

其中：

- `AGENTS.md` / `CLAUDE.md` 更像项目说明和工作规则
- `SYSTEM.md` 用于替换默认 system prompt
- `APPEND_SYSTEM.md` 用于在默认 prompt 后追加内容

所以如果你习惯说 `agent.md`，可以把它理解成这一类“总是加载的项目总纲文件”。在 pi-mono 语境里，最接近的是 `AGENTS.md`。

### 5.2 SKILL.md

这是按需加载的专项能力说明。

适合写：

- 某个专项任务的步骤
- 这个任务的脚本入口
- 这个任务的输入输出约定
- 这个任务的坑

不适合写：

- 整个项目的全局规范
- 所有 agent 都需要知道的常识

一句话区分：

- `AGENTS.md` 讲“这个项目里总的工作规则”
- `SKILL.md` 讲“某一类任务具体怎么做”

## 6. Sandbox 是什么

Sandbox 是执行环境隔离层。

它的目的不是“更炫”，而是：

- 限制 Agent 的副作用范围
- 限制可以访问的文件、网络、系统能力
- 提供更可控的执行环境
- 在需要时让能力可审计、可回收

pi-mono 公开资料里至少能看到两类 sandbox 思路：

### 6.1 浏览器侧 sandbox

在 `pi-web-ui` 里，JavaScript REPL 是在浏览器 sandbox 环境里执行的；Artifacts 也是在受控环境中运行 HTML/SVG/Markdown。

这类 sandbox 适合：

- 前端代码执行
- 小型数据处理
- 可视化产物生成
- 附件和 artifact 的受控访问

### 6.2 宿主机 / 容器 sandbox

在 `pi-mom` 的文档和代码片段里，可以看到 host / docker 两种运行环境。也就是：

- 直接跑在宿主机上
- 跑在 Docker 里

这类 sandbox 适合：

- shell 命令
- 安装依赖
- 跑脚本
- 长任务执行

结论是：sandbox 不是某个具体产品名，它是“把 Agent 的执行能力装进受控边界里”的总称。

## 7. 现状可以怎么理解

如果只抓住当前最重要的事实，可以记下面这几句：

1. Agent 不是裸 LLM，而是带工具、带上下文加载规则、带运行边界的一套设定。
2. Workspace 不只是目录，而是 Agent 的上下文发现范围。
3. Tools 解决单步动作，Skills 解决专项流程。
4. `AGENTS.md` 这类文件适合始终加载，`SKILL.md` 适合按需加载。
5. Sandbox 的本质是把执行环境隔离起来，降低失控成本。
6. pi-mono 的核心思路是：**核心最小，能力外置，按需装配。**
