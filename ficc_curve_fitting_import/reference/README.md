# SHCH 曲线原始入库参考

## 目标

将 `.github/skills/ficc_curve_fitting_import/curve/*.csv` 全量导入 DolphinDB，保留全部原始字段并补齐注释元数据。

## 主流程

1. `scripts/30_create_curve_raw_schema.dos`
   - 创建 `curve_shch_yield_raw`、`curve_file_manifest`、`curve_table_comment_meta`
2. `scripts/50_build_and_ingest_curve_raw_2026.py`
   - 执行 schema 脚本
   - 按 `gb18030` 读取 CSV
   - 对齐字段并入库
   - 导出验收结果

## 输出

- `curve_shch_yield_raw`: 曲线原始全量数据
- `curve_file_manifest`: 文件级导入清单
- `curve_table_comment_meta`: 表注释映射
- `OUT_DIR/table_counts.csv`
- `OUT_DIR/comment_check.csv`
