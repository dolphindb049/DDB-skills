---
name: mihomo_onoff
description: 轻量可移植的 Mihomo 开关技能，支持在 Linux 服务器一键安装、最小配置生成、on/off/status 管理与跨机分发。
license: MIT
metadata:
  author: jrzhang
  version: "1.1.0"
  tags: ["mihomo", "clash-meta", "proxy", "linux", "ops"]
---

# Mihomo On/Off (Portable)

本技能用于在 Linux 环境快速落地 `mihomo`，并通过统一命令完成生命周期管理：

- `mihomo on`
- `mihomo off`
- `mihomo status`

目标是优先保证“首次可用”，避免复杂规则导致启动失败。

## 📂 技能结构

```text
mihomo_onoff/
├── SKILL.md
├── README.md
├── skill.yaml
├── scripts/
│   ├── mihomo                 # on/off/status 统一入口
│   ├── install_local.sh       # 本机安装（解压 core + 拉取订阅 + 生成最小配置）
│   ├── generate_min_config.sh # 从订阅生成最小可用 config-min.yaml
│   └── distribute_wrapper.sh  # 将 wrapper 分发到多台机器
└── templates/
    └── config-min-note.txt
```

## 🚀 快速开始

### 1) 本机安装

```bash
cd .github/skills/mihomo_onoff/scripts
./install_local.sh \
  --binary-gz /path/to/mihomo-linux-amd64-v*.gz \
  --subscription-url "http://your-subscription-url"
```

### 2) 启停验证

```bash
export PATH="$HOME/.local/bin:$PATH"
mihomo on
mihomo status
curl -x http://127.0.0.1:7890 -s https://api.ip.sb/ip && echo
mihomo off
```

## ⚙️ 默认路径与环境变量

- `MIHOMO_BASE_DIR`（默认 `$HOME/clash`）
- `MIHOMO_CORE_BIN`（默认 `$HOME/.local/bin/mihomo-core`）
- `MIHOMO_CONF_FILE`（默认 `$HOME/clash/config-min.yaml`）
- `MIHOMO_LOG_FILE`（默认 `$HOME/clash/mihomo.log`）
- `MIHOMO_PID_FILE`（默认 `$HOME/clash/mihomo.pid`）

## 🧩 设计原则（最小配置优先）

生成配置时采用“最小规则”策略：

- 保留订阅中的 `proxies/proxy-groups`
- 强制 `mode: global`
- 规则仅保留 `MATCH,🚀 节点选择`

这样可以显著降低 `GEOIP/MMDB` 下载超时导致的冷启动失败。

## 🛠️ 跨服务器分发 wrapper

```bash
cd .github/skills/mihomo_onoff/scripts
./distribute_wrapper.sh ~/.local/bin/mihomo user1@host1 user2@host2
```

> 说明：该步骤仅分发 wrapper。远端仍需具备 `~/.local/bin/mihomo-core` 与配置文件。

## 🔧 常见问题

- 启动失败且日志含 MMDB/GEOIP 超时：继续使用最小配置，不要首轮引入复杂规则。
- `status` 异常：先执行 `mihomo off` 再 `mihomo on`，并检查日志文件。
- `mihomo` 命令找不到：将 `export PATH="$HOME/.local/bin:$PATH"` 写入 shell rc。
