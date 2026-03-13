# pi-mono 产品化改造案例：面向 DolphinDB 的最小实现路径

这份文档不是泛泛介绍 pi-mono，而是回答一个具体问题：

> 如果要基于 pi-mono 做一个面向 DolphinDB 的产品，最小改造路径是什么？

目标功能是三块：

1. 一个内置的 DDB 脚本执行工具
2. 一个按目标 DDB 与 workspace 发放 token、再用 token 启动会话的外部服务
3. 一个 TypeScript 前端界面：左上数据库表，左下 workspace 文件树，右上预览区，右下 terminal/简易对话

结论先说：**最小方案应该尽量复用 `pi-agent-core` 与 `pi-web-ui`，不要一上来重做整套 coding agent。**

## 1. pi-mono 里已经有什么可以复用

基于公开文档，pi-mono 当前至少可以拆成下面几层：

### 1.1 `pi-ai`

作用：统一多 LLM Provider 接入。

对本项目的意义：

- 不需要自己重写模型调用层
- 后续切换模型供应商的成本低

### 1.2 `pi-agent-core`

作用：Agent 状态管理、消息循环、工具调用。

对本项目的意义：

- 可以直接拿来承载对话和 tool call
- 不需要自己从零写 agent loop

### 1.3 `pi-coding-agent`

作用：终端里的 coding harness。

对本项目的意义：

- 可以学习它的资源加载思路
- 可以参考它的 tools、skills、AGENTS.md 加载规则
- 但不建议把整个 TUI 直接搬进你的产品

原因很简单：你的目标不是做一个终端 coding agent 克隆，而是做一个面向 DDB 的垂直产品。

### 1.4 `pi-web-ui`

作用：可复用的 web 端 chat UI 组件。

这是最值得直接复用的一层。公开文档已经给出很多现成能力：

- `AgentInterface` / `ChatPanel`
- `ArtifactsPanel`
- `AppStorage`
- `IndexedDBStorageBackend`
- API key / settings / sessions 存储
- attachment 与 artifact 处理
- 自定义 toolsFactory

这意味着：**你的前端不需要从 0 开始写 chat、会话存储和基础 agent 面板。**

## 2. 你的目标功能，对应 pi-mono 的最小承接点

### 2.1 内置 DDB 脚本执行工具

这部分本质上是一个自定义 tool。

在 pi-mono 体系里，最自然的落点是：

- 若做 CLI 版：`pi-coding-agent` 的 custom tool / extension
- 若做产品版：`pi-agent-core` 上挂一个 TypeScript 自定义工具

它不应该一开始就做成一个庞大的 Skill，而应该先做成一个**稳定可调用的工具**。

理由：

- 它是原子能力，不是完整工作流
- 后面其他 Skill 都会依赖它
- 工具一旦稳定，Skill 编写会快很多

### 2.2 token 发放与会话启动服务

这部分 pi-mono 没有现成业务能力，需要你自己补一个轻量后端。

它的职责建议只做三件事：

1. 接收目标 DDB 与 workspace 信息
2. 校验权限并签发短期 token
3. 用 token 换取一个会话配置，再启动或恢复对应会话

关键点：

- 这不是 LLM provider key 管理的替代品
- 这是你产品自己的业务授权层
- 要尽量保持薄，不要变成一个大而全的中台

### 2.3 四块前端界面

最小实现不要直接魔改 `ChatPanel`，而是自己搭 2x2 布局，把 `AgentInterface` 作为右下角主面板之一。

建议：

- 左上：数据库对象树
- 左下：workspace 文件树
- 右上：预览区
- 右下：`AgentInterface` 或 terminal/chat tabs

为什么不用 `ChatPanel` 直接硬改：

- `ChatPanel` 偏整体式封装
- 你的布局明显不是单一聊天页
- `AgentInterface` 更适合作为可嵌入组件

## 3. 什么可以直接复用，什么不要复用

### 3.1 可以直接复用

- `pi-agent-core` 的 agent loop
- `pi-web-ui` 的 `AgentInterface`
- `pi-web-ui` 的存储层
- `pi-web-ui` 的附件/预览/Artifacts 能力
- `pi-coding-agent` 的 skills 与 context loading 思路
- `pi-coding-agent` 的 custom tool 设计方式

### 3.2 不要直接搬

- 终端 TUI 整套界面
- 过多默认工具
- 与你产品目标无关的交互特性
- 一上来就做复杂 extension 体系

原则就是：**少就是多。只搬真正缩短路径的部分。**

## 4. 最小实现方案

围绕你的目标，我建议 MVP 只做下面这些：

### 4.1 后端

一个很薄的 TypeScript 服务：

- `POST /session/token`
  - 输入：目标 DDB、workspace、用户身份
  - 输出：短期 token
- `POST /session/start`
  - 输入：token
  - 输出：session id、可用工具、当前 workspace 元数据
- `POST /tools/ddb/execute`
  - 输入：session id、连接信息、脚本/代码片段
  - 输出：执行结果、表格摘要、错误信息

### 4.2 Agent 侧

先只挂 1 个核心工具：

- `ddb_execute`

暂时不要同时上：

- 文件写回工具
- 自动建模工具
- 自动部署工具
- 多代理编排

因为这些都会放大复杂度。

### 4.3 前端

第一版只做 4 个基础面板：

- 数据库树
- 文件树
- 预览区
- 对话区

其中：

- 对话区复用 `AgentInterface`
- 预览区先支持表格、Markdown、文本、图片
- terminal 先不做真 shell，可先做“执行日志面板”

这样能明显降低前期复杂度。

## 5. 第一步应该做什么

第一步不要碰 token broker，也不要先做完整 UI。

**第一步只做：内置 DDB 执行工具。**

原因：

1. 它是后续所有 Skill 和 UI 的基础原子能力
2. 它最容易形成闭环
3. 它最容易测试
4. 它最容易复用你现有的 `execute-dlang` 经验

### 5.1 第一步的最小范围

只支持下面两种调用：

- 执行 `.dos` 文件
- 执行简短代码片段

先不要做：

- 长会话恢复
- 大结果分页
- 多数据源切换
- 复杂权限模型
- 富交互表格渲染

### 5.2 第一步的最小接口

```ts
interface DdbExecuteParams {
  title: string;
  host: string;
  port: number;
  user?: string;
  password?: string;
  scriptPath?: string;
  code?: string;
}

interface DdbExecuteResult {
  ok: boolean;
  stdout: string;
  stderr?: string;
  summary?: string;
}
```

约束：

- `scriptPath` 和 `code` 二选一
- 优先支持 `.dos`
- 短表达式才允许 `code`
- 敏感信息走环境变量或后端注入，不写死在前端

### 5.3 第一步的复用来源

可以直接复用的现有经验：

- `execute-dlang` 里关于 `.dos` 优于 `-c` 的实践
- PowerShell 引号陷阱总结
- server 模式与直连模式的取舍经验
- 输出为空时要求脚本显式返回结果

也就是说，第一步不是重新发明一个 DDB 执行器，而是先把现有能力用 TypeScript tool 的形式产品化。

## 6. 第一步怎么测试

这个阶段只做最小闭环测试，不求花哨。

### 6.1 功能测试

至少覆盖：

1. `code = "1+1"` 能返回成功
2. 一个最小 `.dos` 文件能执行成功
3. 缺少 host/port 时返回可读错误
4. 同时传 `code` 和 `scriptPath` 时被拒绝
5. 执行报错时，stderr 能回到前端

### 6.2 回归测试

重点看：

- 路径解析
- 超时处理
- 连接失败提示
- 非 ASCII 返回内容是否正常

### 6.3 文档要求

第一步做完后，必须同步补文档：

- 这个 tool 的用途
- 参数定义
- 最小示例
- 错误处理约定
- 为什么先只支持这两个入口

这不是附属工作，而是为了让后续新的 agent 能快速理解和继续开发。

## 7. 为什么不先做 token broker 和完整 UI

因为那会同时引入三类复杂度：

- 业务授权复杂度
- 前后端会话协同复杂度
- 界面状态管理复杂度

如果底层 DDB 执行能力还没稳定，这三块只会放大混乱。

所以正确顺序是：

```text
先做 ddb_execute 工具
→ 再做 token broker
→ 再把四块 UI 接起来
→ 再逐步补 Skill 和更复杂工作流
```

## 8. 当前交付边界

基于你这次要求，当前最合理的“第一步交付”是：

- 把 pi-mono 相关公开资料转写成中文、面向 Agent 的说明
- 明确复用边界
- 确定最小产品方案
- 把第一步锁定为 `ddb_execute` 工具
- 给出明确接口、测试点、文档要求

如果后面要进入真正代码实现，下一轮就应该做一件事：

**在实际的 pi-mono 或新产品仓库里落一个最小 TypeScript `ddb_execute` tool，并把测试跑通。**

## 9. 结论

面向你的这个产品目标，真正高效的路径不是“大而全地搬 pi-mono”，而是：

- 复用 `pi-agent-core`
- 复用 `pi-web-ui`
- 吸收 `pi-coding-agent` 的资源加载思想
- 先落一个最小的 DDB 执行工具
- 每做完一步，就测试、写文档、再继续下一步

这就是“少就是多，慢就是快”的工程化做法。
