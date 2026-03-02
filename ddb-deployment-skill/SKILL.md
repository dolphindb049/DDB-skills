---
name: ddb-deployment-skill
description: DolphinDB 单节点部署与排障技能，强调可执行文件重命名、localSite 精确配置、startSingle/stopSingle 安全改造。
license: MIT
metadata:
  author: ddb-user
  version: "1.2.0"
---

# DolphinDB 单节点部署与升级 Skill（中文）

本 Skill 用于**共享服务器**场景，目标是：
- 不误杀他人的 DolphinDB 进程。
- 每个实例有独立可执行文件名，便于后续升级替换。
- 配置与启动脚本严格一致，避免 “配置改了但脚本没改” 的问题。

## 核心规范（必须遵守）

1. 压缩包命名建议使用：`版本号+用途`，例如：`3004_FICC.zip`。
2. 解压后进入实际程序目录（可能是 `server/`，也可能是 `server/server/`），**优先修改 `dolphindb.cfg`**。
3. `localSite` 必须按用户要求填写（IP、端口、别名都不能错）。
4. 再把可执行文件 `dolphindb` 重命名为实例名（如：`dolphindb_3004_FICC`）。
5. 重命名后立即 `chmod +x` 新文件名。
6. 必须同步修改 `startSingle` 与 `stopSingle`，改为使用新名称，避免影响其他实例。

---

## Phase 1：变量约定与目录准备

```bash
# 你可以按需修改以下变量
export DDB_VERSION="3.00.4"
export DDB_TAG="3004_FICC"            # 版本号+用途（建议）
export DDB_PORT=8848
export LOCAL_IP="192.168.1.5"         # 必须按用户真实要求填写
export INSTALL_DIR="/hdd/hdd9/jrzhang/deploy_test/$DDB_TAG"

# 生成名称
export ZIP_NAME="${DDB_TAG}.zip"
export BIN_NAME="dolphindb_${DDB_TAG}"

echo "部署目录: $INSTALL_DIR"
echo "压缩包名: $ZIP_NAME"
echo "可执行名: $BIN_NAME"
```

---

## Phase 2：下载与解压

```bash
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

wget "https://www.dolphindb.cn/downloads/DolphinDB_Linux64_V${DDB_VERSION}.zip" -O "$ZIP_NAME"
unzip -q -o "$ZIP_NAME" -d server

# 自动识别目录：有的包是 server/，有的是 server/server/
if [ -f server/server/dolphindb.cfg ]; then
  cd server/server
elif [ -f server/dolphindb.cfg ]; then
  cd server
else
  echo "未找到 dolphindb.cfg，请检查解压目录结构"
  exit 1
fi
```

---

## Phase 3：先改配置（关键顺序）

> 先配置 `dolphindb.cfg`，再改二进制名。

```bash
[ -f dolphindb.cfg ] && cp dolphindb.cfg "dolphindb.cfg.bak.$(date +%Y%m%d%H%M%S)"

cat > dolphindb.cfg <<EOF
mode=single
localSite=${LOCAL_IP}:${DDB_PORT}:local${DDB_PORT}
maxMemSize=4
maxConnections=512
workerNum=4
console=0
EOF

# 强校验：localSite 必须唯一且与用户要求一致
grep -n '^localSite=' dolphindb.cfg
```

上面这行：

```bash
[ -f dolphindb.cfg ] && cp dolphindb.cfg "dolphindb.cfg.bak.$(date +%Y%m%d%H%M%S)"
```

含义是：
- `[ -f dolphindb.cfg ]`：先判断配置文件是否存在。
- `&&`：只有“存在”时才执行后半句。
- `cp ... dolphindb.cfg.bak.时间戳`：做一份带时间戳的备份，防止写错后无法回滚。

---

## Phase 4：重命名二进制并赋权

```bash
# 保留原始备份，避免回滚困难
cp -n dolphindb "dolphindb.origin"
mv -f dolphindb "$BIN_NAME"
chmod +x "$BIN_NAME"

ls -l "$BIN_NAME"
```

---

## Phase 5：改造 startSingle / stopSingle（避免打扰别人）

### 1) `startSingle`

将默认内容替换为：

```bash
#!/bin/sh
nohup ./${BIN_NAME} -console 0 -mode single > single.nohup 2>&1 &
```

可执行命令：

```bash
cat > startSingle <<EOF
#!/bin/sh
nohup ./${BIN_NAME} -console 0 -mode single > single.nohup 2>&1 &
EOF
chmod +x startSingle
```

### 2) `stopSingle`

将默认匹配 `dolphindb` 的逻辑，替换为匹配新名称：

```bash
#!/bin/sh
ps -ef|grep -e "${BIN_NAME}" |grep -e "single"|grep -v grep|awk '{print "kill -15 "$2}'|sh
```

可执行命令：

```bash
cat > stopSingle <<EOF
#!/bin/sh
ps -ef|grep -e "${BIN_NAME}" |grep -e "single"|grep -v grep|awk '{print "kill -15 "\$2}'|sh
EOF
chmod +x stopSingle
```

---

## Phase 6：启动与验证

```bash
./startSingle
sleep 2

# 端口监听验证
ss -tulnp | grep "${DDB_PORT}"

# 日志验证
head -n 30 dolphindb.log
```

---

## 升级注意事项（重点）

后续升级本质上是“替换一个二进制并保持脚本一致”：

1. 下载新版本并解压到临时目录。
2. 停止当前实例：`./stopSingle`。
3. 用新版本 `dolphindb` 覆盖当前实例名二进制：`$BIN_NAME`。
4. `chmod +x $BIN_NAME`。
5. `./startSingle` 重启并检查日志与监听端口。

> 如果升级后换了实例命名规则，必须同步更新 `startSingle/stopSingle` 的匹配字符串。

---

## 推荐脚本

本 Skill 已提供以下脚本：
- `scripts/deploy.sh`：一键部署（按本规范改名并改脚本）。
- `scripts/patch_single_scripts.sh`：仅修复/改造现有目录的 `dolphindb.cfg`、二进制名称、`startSingle`、`stopSingle`。

如果你要我执行部署，直接给我：`版本号`、`用途标签`、`IP`、`端口`、`安装目录`。
