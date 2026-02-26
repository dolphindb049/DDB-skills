# 可视化与绘图 (Visualization Skill)

本 Skill 不再从一开始就写死具体的查询逻辑，而是提供一个**通用的执行架构**。Agent 应当学会利用这个架构，根据用户的自然语言需求，动态生成 `.dos` 查询脚本，并调用 Python 工具进行可视化。

## 核心工作流 (Workflow)

Agent 在执行可视化任务时，应遵循以下步骤：

1.  **编写查询 (Authoring)**：
    *   根据用户需求，编写 DolphinDB SQL 脚本 (`.dos`)。
    *   **关键约束**：脚本必须将最终需要绘图的 Table 赋值给变量 `result`。无需包含 `saveText`。
    *   将脚本保存到临时路径，例如 `.github/skills/ddb-visualization/scripts/temp_query.dos`。

2.  **调用工具 (Execution)**：
    *   使用 `visualizer.py` 通用脚本。
    *   传入参数：脚本路径、输出 CSV 路径、输出图片路径、X/Y 轴字段名。

3.  **展示结果 (Presentation)**：
    *   向用户反馈图片生成路径。

## 工具参数说明 (Tool Usage)

脚本路径：`scripts/visualizer.py`

```bash
python scripts/visualizer.py \
  --script  <dos_script_path> \  # 你的查询脚本
  --out-csv <csv_output_path> \  # 中间数据保存位置
  --out-img <image_output_path> \# 最终图片保存位置
  --x       <x_column_name> \    # X轴字段 (如 trade_date)
  --y       <y_column_name> \    # Y轴字段 (如 close)
  --group   <group_column_name> \# [可选] 分组字段 (如 ts_code)
  --title   "图表标题"
```

## 示例 (Example)

如果用户问：“画一下平安银行 2024 年的收盘价”，Agent 应操作如下：

1.  **创建文件** `temp_pingan.dos`:
    ```dolphindb
    pt = loadTable("dfs://stock_daily", "stock_daily_prev")
    result = select trade_date, close from pt 
             where ts_code="000001.SZ", trade_date between 2024.01.01 : 2024.12.31
             order by trade_date
    result // 必须显式返回 result
    ```

2.  **执行命令**:
    ```bash
    python .github/skills/ddb-visualization/scripts/visualizer.py \
      --script temp_pingan.dos \
      --out-csv pingan.csv \
      --out-img pingan.png \
      --x trade_date \
      --y close \
      --title "平安银行2024收盘价"
    ```

## 避坑指南
*   **变量名约束**：务必确认 dos 脚本中计算结果赋值给了 `result` 变量。
*   **日期处理**：Python 绘图时会自动检测 `date`/`time` 命名的列并转换为时间轴。确保 SQL 中 select 出来的列名包含这些关键字，或者在 X 轴参数中指定。
