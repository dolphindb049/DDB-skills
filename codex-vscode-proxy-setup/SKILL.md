````skill
---
name: codex-vscode-proxy-setup
description: 在 Windows + VS Code 场景下，使用第三方 OpenAI 兼容 API（n1n）稳定启动 Codex CLI。覆盖最小安装检查、config.toml 正确写法、环境变量一次配置永久生效、国内/代理地址切换、以及非交互连通性验证。
license: MIT
metadata:
  author: ddb-user
  version: "1.0.0"
---

# Codex CLI（VS Code / Windows / n1n）快速跑通

本技能用于解决这类问题：
- `Missing environment variable: OPENAI_API_KEY`
- 已安装 `codex` 但在 VS Code 里启动失败
- 不确定是工作目录问题还是配置问题

## 🚀 极简可执行流程（推荐）

### 0) 只做一次的前提检查
```powershell
node --version
codex --version
```
如果已能输出版本，**不要重复安装**。

### 1) 配置 `~/.codex/config.toml`
Windows 对应路径：`C:\Users\<你的用户名>\.codex\config.toml`

建议最小配置：
```toml
model = "gpt-5.3-codex"
model_provider = "openai-chat-completions"
model_reasoning_effort = "medium"

[model_providers.openai-chat-completions]
name = "N1N_PROXY"
base_url = "https://api.n1n.ai/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

> 说明：`env_key = "OPENAI_API_KEY"` 表示 Codex 会从系统环境变量读取密钥；如果变量没设置，就会报错。

如不确定可用模型，先执行：
```powershell
$headers = @{ Authorization = "Bearer $env:OPENAI_API_KEY" }
(Invoke-RestMethod -Uri "https://api.n1n.ai/v1/models" -Headers $headers).data.id
```
然后把 `model` 改为你账号有权限的模型。

### 2) 在 Windows 永久设置环境变量（PowerShell）
```powershell
# 替换为你的真实密钥
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-xxxx", "User")

# 默认走代理地址
[Environment]::SetEnvironmentVariable("OPENAI_BASE_URL", "https://api.n1n.ai/v1", "User")
```

设置后请**重开 VS Code**（或至少重开集成终端）。

### 3) 连通性验证（非交互）
```powershell
codex exec --skip-git-repo-check "回复: OK"
```
若能返回正常文本，即可确认可用。

---

## 🌏 地址切换（代理 / 国内）

你有两个可用地址：
- 代理：`https://api.n1n.ai/v1`
- 国内：`https://hk.n1n.ai/v1`

### 方案 A（推荐）：临时覆盖本次运行
```powershell
codex -c 'model_providers.openai-chat-completions.base_url="https://hk.n1n.ai/v1"' exec "回复: OK"
```

### 方案 B：改回默认配置
直接修改 `config.toml` 里的 `base_url` 即可。

---

## 🧩 常见坑位（精简版）

1. **VS Code 里仍报缺少变量**
   - 原因：变量是后来设置的，旧终端没刷新。
   - 处理：重开 VS Code，再执行：
   ```powershell
   echo $env:OPENAI_API_KEY
   ```

2. **以为是工作目录问题**
   - 对这个报错不是。`OPENAI_API_KEY` 缺失与 cwd 无关。
   - 若提示 `Not inside a trusted directory`，先使用 `--skip-git-repo-check` 跑通。

3. **配置写了但仍不生效**
   - 检查是否存在冲突字段（比如在 provider 节里误写了全局 `model` / `model_provider`）。

4. **模型名不匹配**
   - 使用平台实际支持的模型名；本技能示例为 `gpt-5.3-codex`。

---

## ✅ AI Agent 执行策略

当用户说“Codex 在 VS Code 启不来/缺少 OPENAI_API_KEY”时，按以下顺序：
1. 先检查 `codex --version` 与环境变量是否为空。
2. 再修正 `config.toml` 为最小可用配置。
3. 最后用 `codex exec "回复: OK"` 做非交互验证。

````