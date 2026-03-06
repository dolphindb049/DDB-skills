---
name: swordfish-smoke-test
description: 在本地 Swordfish 项目目录中执行可复现的构建与冒烟验证（baseDemo + streamEngineDemo），并快速定位常见启动失败原因（license、运行目录、依赖库、资产文件缺失）。
---

# Swordfish Smoke Test

用于验证本地 Swordfish（如 `swordfish-300.4`）是否可成功启动并跑通核心示例。

## 何时使用

- 用户希望确认 Swordfish 是否“能启动 + 能跑代码”
- 需要快速区分是构建问题还是运行环境问题
- 需要形成可复用验收流程

## 前置条件

- 项目根目录含 `CMakeLists.txt`、`asset/`、`demo/`
- 已有可用商业 license 文件（`asset/dolphindb.lic`）
- 系统可用 `cmake`、`make`、`g++`

## 快速执行

在项目根目录执行：

```bash
bash /home/jrzhang/.codex/skills/swordfish-smoke-test/scripts/smoke_test.sh /abs/path/to/swordfish-300.4
```

## 手动流程（脚本等价）

1. 构建
```bash
cd <project>/build
cmake ..
make -j8
```

2. 检查运行资产是否在 `build/bin`：
- `dolphindb.dos`
- `dolphindb.lic`
- `dolphindb.cfg`
- `dict/`

3. 运行基础验证：
```bash
cd <project>/build/bin
./baseDemo
```
成功信号：
- 输出 `Inintialize DolphinDB runtime ...`
- 最后输出 `Finalize DolphinDB runtime ...`
- 进程退出码为 0

4. 运行流引擎验证：
```bash
cd <project>/build/bin
./streamEngineDemo
```
成功信号：
- 出现 `create oltp table`
- 出现多次 `exec count(*) from objByName(\`result)` 且计数递增
- 出现 `clean environment`
- 进程退出码为 0

## 常见失败与处理

- License 校验失败（CPU 核数或授权不匹配）：
  - 检查 `build/bin/dolphindb.log` 中 license 报错
  - 替换为匹配机器和版本的商业 license

- 运行目录错误：
  - 必须从 `build/bin` 运行 demo，或确保运行目录存在 `dolphindb.dos/.lic/.cfg/dict`

- 动态库缺失：
  - 优先确认项目 `lib/` 下依赖齐全
  - 必要时补充系统依赖（如 OpenBLAS、zlib）

- Demo 二进制不存在：
  - 先执行 `cmake .. && make -j8`

## 输出建议

执行后给出：
- 构建是否成功
- `baseDemo` 是否通过
- `streamEngineDemo` 是否通过
- 若失败：失败阶段 + 首条关键报错 + 建议修复动作
