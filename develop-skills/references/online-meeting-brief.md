# Skill 开发分享会资料（在线版）

作者：jrzhang  
主题：The Complete Guide to Building Skills for DolphinDB

## 一句话定义
Skill 是一个可复用、可迁移、可执行的任务方法论封装（不是单次任务，不是工具本体，也不是 Agent 本身）。

## 章节导览
1. 简介（骑自行车类比，厘清 Agent/Tool/Task/Skill）
2. 基础（Skill 文件结构 + 渐进式加载）
3. 规划与设计（先定义用例，再写脚本）
4. 测试与迭代（跨环境复现是验收线）
5. 分发与共享（Doc as Skill）
6. 模式与排错（顺序编排、多工具协作、领域智能）
7. FICC 案例（从慢到快的复用闭环）

## 会后资料
- 主指南：../SKILL.md
- 中文翻译参考：./The-Complete-Guide-to-Building-Skill-for-Claude.zh.md
- 演示文稿：./Skill-Development-Guide-v2.pptx
- 示例脚本：../scripts/ficc_pricing_example.dos

## 组织落地建议
- 统一验收标准：一个人跑通，另一个人同级模型也能跑通
- 统一资产结构：每个 Skill 至少包含 `SKILL.md + scripts/ + references/`
- 统一演进机制：任务复盘驱动 Skill 升级，季度清理低价值 Skill

## 结语
Skill 不是终点，而是模型完全内化行业能力前的高效过渡层。
