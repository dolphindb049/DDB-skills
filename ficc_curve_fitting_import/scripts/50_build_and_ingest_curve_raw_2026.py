#!/home/jrzhang/miniconda3/bin/python3
"""
SHCH 曲线原始数据入库主流程。

流程：
1) 执行 30_create_curve_raw_schema.dos 建库建表；
2) 批量读取 curve/*.csv（gb18030），字段对齐后写入原始表；
3) 记录文件级导入清单；
4) 导出表行数与注释完整性检查结果。
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import dolphindb as ddb
import pandas as pd

DDB_HOST = os.getenv("DDB_HOST", "192.168.100.43")
DDB_PORT = int(os.getenv("DDB_PORT", "7731"))
DDB_USER = os.getenv("DDB_USER", "admin")
DDB_PASSWORD = os.getenv("DDB_PASSWORD", "123456")
DB_PATH = os.getenv("DDB_DB_PATH", "dfs://ficc_curve_raw_2026")
CURVE_DIR = Path(os.getenv("CURVE_DIR", str(Path(__file__).resolve().parents[1] / "curve")))
OUT_DIR = Path(os.getenv("OUT_DIR", "/hdd/hdd9/jrzhang/data/ficc_curve_raw_2026"))
CSV_ENCODING = os.getenv("CSV_ENCODING", "gb18030")
SCHEMA_DOS = Path(__file__).resolve().parent / "30_create_curve_raw_schema.dos"


@dataclass(frozen=True)
class Col:
    name: str
    dtype: str
    comment: str


SCHEMA: dict[str, dict[str, Any]] = {
    "curve_shch_yield_raw": {
        "table_comment": "SHCH曲线原始数据（CSV全量入库）",
        "columns": [
            Col("curveName", "STRING", "曲线名称"),
            Col("curveType", "STRING", "曲线类型（即期/到期/远期的即期/远期的到期）"),
            Col("referenceDate", "DATE", "曲线日期"),
            Col("standardTermYear", "DOUBLE", "标准期限（年）"),
            Col("yieldPct", "DOUBLE", "收益率（%）"),
            Col("nYear", "DOUBLE", "N（年）"),
            Col("kYear", "DOUBLE", "K（年）"),
            Col("tenorLabel", "STRING", "期限描述（如 3M/1Y/10Y）"),
            Col("sourceFile", "STRING", "来源文件名"),
            Col("importBatch", "STRING", "导入批次号"),
            Col("importTime", "TIMESTAMP", "导入时间"),
        ],
    },
    "curve_file_manifest": {
        "table_comment": "SHCH曲线文件导入清单",
        "columns": [
            Col("sourceFile", "STRING", "来源文件名"),
            Col("rowCount", "LONG", "文件行数"),
            Col("minDate", "DATE", "最小日期"),
            Col("maxDate", "DATE", "最大日期"),
            Col("importBatch", "STRING", "导入批次号"),
            Col("importTime", "TIMESTAMP", "导入时间"),
        ],
    },
}

CN_RENAME = {
    "曲线名称": "curveName",
    "曲线类型": "curveType",
    "日期": "referenceDate",
    "标准期限(年)": "standardTermYear",
    "收益率(%)": "yieldPct",
    "N(年)": "nYear",
    "K(年)": "kYear",
    "期限描述": "tenorLabel",
}


def create_schema(sess: ddb.session) -> None:
    if not SCHEMA_DOS.exists():
        raise FileNotFoundError(f"schema dos not found: {SCHEMA_DOS}")
    dos = SCHEMA_DOS.read_text(encoding="utf-8").replace("__DB_PATH__", DB_PATH)
    sess.run(dos)


def ddb_select_expr(columns: list[Col]) -> str:
    type_map = {
        "STRING": "string",
        "DOUBLE": "double",
        "LONG": "long",
        "DATE": "date",
        "TIMESTAMP": "timestamp",
    }
    exprs = []
    for c in columns:
        cast = type_map[c.dtype]
        exprs.append(f"{cast}({c.name}) as {c.name}")
    return ",\n           ".join(exprs)


def align_columns(df: pd.DataFrame, columns: list[Col]) -> pd.DataFrame:
    out = df.copy()
    for c in columns:
        if c.name not in out.columns:
            out[c.name] = pd.NA
    out = out[[c.name for c in columns]]
    for c in columns:
        if c.dtype in {"DATE", "TIMESTAMP"}:
            out[c.name] = pd.to_datetime(out[c.name], errors="coerce")
    return out


def append_table(sess: ddb.session, table_name: str, df: pd.DataFrame) -> int:
    cols: list[Col] = SCHEMA[table_name]["columns"]
    aligned = align_columns(df, cols)
    if aligned.empty:
        return 0
    sess.upload({"tmp_curve_data": aligned})
    expr = ddb_select_expr(cols)
    sql = f'''
loadTable("{DB_PATH}", "{table_name}").append!(
    select {expr}
    from tmp_curve_data
)
'''
    sess.run(sql)
    return len(aligned)


def load_single_csv(path: Path, import_batch: str, import_time: datetime) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(path, encoding=CSV_ENCODING)
    raw = raw.rename(columns=CN_RENAME)
    for cn, en in CN_RENAME.items():
        if en not in raw.columns:
            raw[en] = pd.NA
    data = raw[[*CN_RENAME.values()]].copy()
    data["sourceFile"] = path.name
    data["importBatch"] = import_batch
    data["importTime"] = import_time

    data["referenceDate"] = pd.to_datetime(data["referenceDate"], errors="coerce")
    for col in ["standardTermYear", "yieldPct", "nYear", "kYear"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    manifest = pd.DataFrame(
        {
            "sourceFile": [path.name],
            "rowCount": [len(data)],
            "minDate": [data["referenceDate"].min()],
            "maxDate": [data["referenceDate"].max()],
            "importBatch": [import_batch],
            "importTime": [import_time],
        }
    )
    return data, manifest


def export_validation(sess: ddb.session, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    counts = sess.run(
        f'''
table(
    ["curve_shch_yield_raw", "curve_file_manifest"] as tableName,
    [
        long((exec count(*) from loadTable("{DB_PATH}", "curve_shch_yield_raw"))[0]),
        long((exec count(*) from loadTable("{DB_PATH}", "curve_file_manifest"))[0])
    ] as rowCount
)
'''
    )
    pd.DataFrame(counts).to_csv(out_dir / "table_counts.csv", index=False, encoding="utf-8-sig")

    comment_check = sess.run(
        f'''
curveRawDef = schema(loadTable("{DB_PATH}", "curve_shch_yield_raw")).colDefs
manifestDef = schema(loadTable("{DB_PATH}", "curve_file_manifest")).colDefs

table(
    ["curve_shch_yield_raw", "curve_file_manifest"] as tableName,
    [
        long((exec sum(iif(isNull(comment) or trim(string(comment))=="", 1, 0)) from curveRawDef)[0]),
        long((exec sum(iif(isNull(comment) or trim(string(comment))=="", 1, 0)) from manifestDef)[0])
    ] as missingColComments
)
'''
    )
    pd.DataFrame(comment_check).to_csv(out_dir / "comment_check.csv", index=False, encoding="utf-8-sig")


def main() -> None:
    sess = ddb.session()
    sess.connect(DDB_HOST, DDB_PORT, DDB_USER, DDB_PASSWORD)

    create_schema(sess)

    files = sorted(CURVE_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No csv files found under {CURVE_DIR}")

    import_batch = datetime.now().strftime("%Y%m%d_%H%M%S")
    import_time = datetime.now()

    total_rows = 0
    for path in files:
        data_df, manifest_df = load_single_csv(path, import_batch, import_time)
        total_rows += append_table(sess, "curve_shch_yield_raw", data_df)
        append_table(sess, "curve_file_manifest", manifest_df)

    export_validation(sess, OUT_DIR)
    print(f"[OK] Imported {total_rows} rows from {len(files)} files into {DB_PATH}")
    print(f"[OK] Validation exported to: {OUT_DIR}")


if __name__ == "__main__":
    main()
