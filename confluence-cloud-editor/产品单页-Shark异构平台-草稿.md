# 【Shark】产品单页（草稿）

- 信息来源: `assets/内部培训-Shark 异构平台-20250730.pptx`

---

**产品名称：** Shark 异构平台

**产品 slogan：** 面向高性能计算与业务建模的一体化异构计算平台

**视觉主图：** ![alt text](image.png)

### 产品概述
**一句话定义：**

*一个面向 DolphinDB 业务场景的异构计算平台，通过 GPU 并行计算与可扩展计算框架，统一支持因子挖掘、通用并行计算和复杂定价加速。*

**核心定位：**
Shark 位于 DolphinDB 高性能数据处理能力之上，向上提供可直接落地的异构计算能力层。它重点解决三类问题: 
1. 因子挖掘训练慢、表达式搜索成本高。
2. 复杂业务逻辑难以高效迁移到 GPU。
3. 蒙特卡洛等高计算量定价与风险计算难以满足实时性要求。

**目标用户：**
- 量化研究员和因子研究员（高频/多频因子挖掘）
- 金融工程与量化开发团队（复杂定价与风险计算）
- 平台与架构团队（统一 GPU 计算能力接入）

---

### 优势与价值
*简要解释: 产品有什么能力能给客户带来什么。*

**关键特性**
- 支持 `@gpu` 注解，将用户函数自动编译为计算图并调度到 GPU 执行。
- 支持 Shark GPLearn 全流程: `createGPLearnEngine`、`gpFit`、`gpPredict`、`setGpFitnessFunc`、`addGpFunction`。
- 支持 group 维度与降频挖掘能力（`groupCol`、`dimReduceCol`），可覆盖高频/低频混合研究。
- 覆盖计算密集型场景: 因子挖掘、蒙特卡洛路径模拟、复杂结构化产品定价与 Greeks 计算。

**核心优势**
- 与 DolphinDB 脚本语法和数据结构保持一致，已有脚本可低改造迁移到 GPU。
- 与 DolphinDB 数据存储计算链路一体化，减少数据搬运与跨系统改写成本。
- 基于平台内建函数库和可扩展算子机制，金融场景表达能力更强。

**客户价值**
- 显著缩短计算密集任务耗时，缓解训练和定价的性能瓶颈。
- 提升研究迭代速度与实时报价/风控响应速度。
- 在保留原有研发资产的前提下，降低异构改造的人力和时间成本。

1. **`@gpu` 自定义函数能力**

支持将业务逻辑以 `@gpu` 形式封装为并行计算单元，便于在 Shark Graph 中复用。

在保持业务可定制性的同时，减少底层 GPU 编程负担，降低异构改造门槛。

可更快将策略逻辑和定价逻辑迁移到高性能执行路径，缩短研发与上线周期。

2. **Shark GPLearn 因子挖掘引擎**

内置遗传编程流程，支持 `GPExecutor` 在 GPU 上执行表达式；支持 `functionSet`、种群规模、迭代代数、交叉/变异概率、自定义适应度函数等完整参数体系。

相较 Python `gplearn` 在中大规模样本下有显著训练性能优势，可直接融入 DolphinDB 训练流程。

更快完成候选因子搜索与筛选，提高研究效率并缩短因子从构思到验证的周期。

文档依据补充:
- 官方 `createGPLearnEngine` 提供 `groupCol`、`dimReduceCol`、`deviceId`、`functionSet` 等核心参数，可覆盖分组与降频挖掘。
- `setGpFitnessFunc` 支持字符串适应度或自定义函数，适合按业务目标定制评价指标。
- `gpFit` 输出公式及 fitness（可选公式相关性），便于因子筛选和可解释性分析。

3. **蒙卡路径加速与复杂定价加速**

覆盖结构化产品等高计算负载场景，支持大规模路径模拟与并行定价计算，并可用于实时风险指标计算。

在已展示案例中，原系统与 Shark 对比出现数量级提速（典型 `>100X`），并显著改善实时响应能力。

提升报价与风险响应速度，支持更细粒度、更高频的盘中计算与风控决策。

文档依据补充:
- 在 `Shark Graph` / `蒙特卡洛模拟定价` 教程示例中，`@gpu` 可将定价脚本迁移到 GPU 执行。
- 雪球期权蒙卡示例显示在大迭代规模下，GPU 相对 CPU 并发执行有显著优势（文档内给出多档并发与迭代次数对比表）。

---

### 典型应用场景
*如果有客户案例可写客户背景，否则描述场景。*

可参考内部页面（精要）:
- [Shark 页面（Confluence）](https://dolphindb1.atlassian.net/wiki/spaces/pm/pages/1495433228/Shark)

页面内容涵盖 Shark 的定位、能力边界和典型业务落地，可用于对齐外部单页中的术语与场景口径。

1. **高频因子挖掘场景**

研究团队需要在较短时间内完成大量候选表达式训练与筛选。

传统 CPU 方案训练耗时长，参数迭代慢，影响研究节奏。

通过 Shark GPLearn + GPU 执行表达式，结合自定义适应度函数进行批量训练。

缩短训练周期，提升可迭代次数和候选因子覆盖度。

可落地接口:
- `createGPLearnEngine(trainData, targetData, groupCol=..., dimReduceCol=..., functionSet=...)`
- `setGpFitnessFunc(engine, myFitness, funcArgs=...)`
- `engine.gpFit(programNum)` / `engine.gpPredict(...)`

2. **结构化产品定价与风险计算场景**

定价团队需要对复杂产品进行路径模拟、定价与 Greeks 计算。

原系统计算耗时较长，难以满足实时报价和盘中风控需要。

通过 Shark Graph 与 `@gpu` 自定义函数将关键计算链路并行化。

在案例中实现数量级性能提升（典型 `>100X`），提升实时报价与风控时效。

可落地方式:
- 保留现有 DolphinDB 函数逻辑，在满足语法子集前提下为核心函数增加 `@gpu` 注解。
- 将蒙卡路径生成、敲入敲出判断、折现收益与 Greeks 相关计算放入同一 GPU 执行链路。

---

### 参考链接
- [官方教程：Shark GPLearn 快速上手](https://docs.dolphindb.cn/zh/tutorials/gplearn.html)
- [官方教程：Shark GPLearn 应用说明](https://docs.dolphindb.cn/zh/tutorials/shark_gplearn_application.html)

---

### 底部统一标识
[ DolphinDB LOGO ] 或二维码

**官网：** http://dolphindb.cn

**邮箱：** sales@dolphindb.com

**电话：** 0571-82852925

**地址：** 浙江 杭州

**版本：** 2026-03-10 
