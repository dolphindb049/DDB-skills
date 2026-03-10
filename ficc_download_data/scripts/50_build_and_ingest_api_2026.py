#!/home/jrzhang/miniconda3/bin/python3
"""
FICC API 数据下载与入库（可复用版）

设计目标：
1. 严格按 PDF 输出参数定义建表，字段级 comment 与文档一致；
2. 一次执行完成：建库建表 -> 下载数据 -> 入库 -> 导出 -> 行数与注释校验；
3. 通过环境变量参数化年份与连接信息，便于后续 agent 复用调度。

关键环境变量：
- DATAYES_TOKEN: API Token
- DDB_HOST / DDB_PORT / DDB_USER / DDB_PASSWORD: DolphinDB 连接参数
- DDB_DB_PATH: 目标数据库路径（默认 dfs://ficc_api_pdf_2026）
- TARGET_YEAR: 日频行情/估值抓取年份（默认 2026）
- MATURITY_YEAR: 到期债券筛选年份（默认 2026）
- OUT_DIR: 本地导出目录
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import dolphindb as ddb
import pandas as pd
import requests

BASE_URL = "https://api.datayes.com/data/v1"
TOKEN = os.getenv("DATAYES_TOKEN", "4c89993d518c6cb4105870590b923416ecc61d0da7b438f6ace0bb036040a7c4")
DDB_HOST = os.getenv("DDB_HOST", "192.168.100.43")
DDB_PORT = int(os.getenv("DDB_PORT", "7731"))
DDB_USER = os.getenv("DDB_USER", "admin")
DDB_PASSWORD = os.getenv("DDB_PASSWORD", "123456")
DB_PATH = os.getenv("DDB_DB_PATH", "dfs://ficc_api_pdf_2026")
OUT_DIR = Path(os.getenv("OUT_DIR", "/hdd/hdd9/jrzhang/data/ficc_api_2026"))
TARGET_YEAR = int(os.getenv("TARGET_YEAR", "2026"))
MATURITY_YEAR = int(os.getenv("MATURITY_YEAR", "2026"))
MATURITY_YEARS_RAW = os.getenv("MATURITY_YEARS", "").strip()
MONTH_LIMIT = int(os.getenv("MONTH_LIMIT", "0"))
MAX_CANDIDATE_TICKERS = int(os.getenv("MAX_CANDIDATE_TICKERS", "0"))
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "90"))
API_RETRIES = int(os.getenv("API_RETRIES", "6"))
API_MAX_PAGES = int(os.getenv("API_MAX_PAGES", "0"))
SCHEMA_DOS = Path(__file__).resolve().parent / "30_create_pricing_schema.dos"


def parse_maturity_years() -> list[int]:
    if MATURITY_YEARS_RAW:
        years = [int(item.strip()) for item in MATURITY_YEARS_RAW.split(",") if item.strip()]
        uniq_years = sorted(set(years))
        if uniq_years:
            return uniq_years
    return [MATURITY_YEAR]


MATURITY_YEARS = parse_maturity_years()


@dataclass(frozen=True)
class Col:
    """字段定义：名称、DolphinDB 类型、字段中文注释。"""

    name: str
    dtype: str
    comment: str


SCHEMA: dict[str, dict[str, Any]] = {
    "api_getBond": {
        "table_comment": "getBond-债券基本信息输出参数表",
        "endpoint": "/api/bond/getBond.json",
        "columns": [
            Col("secID", "STRING", "证券ID"),
            Col("ticker", "STRING", "交易代码"),
            Col("exchangeCD", "STRING", "通联编制的证券市场编码。例如，XIBE-中国银行间市场；XSHE-深圳证券交易所等。对应getSysCode.codeTypeID=10002。"),
            Col("bondID", "STRING", "债券ID"),
            Col("secFullName", "STRING", "债券全称"),
            Col("secShortName", "STRING", "债券简称"),
            Col("listStatusCD", "STRING", "上市状态。L-上市，S-暂停，DE-终止上市，UN-未上市。对应getSysCode.codeTypeID=10005。"),
            Col("partyID", "LONG", "发行人ID"),
            Col("issuer", "STRING", "发行人"),
            Col("totalSize", "DOUBLE", "累计发行总额(亿元)"),
            Col("remainSize", "DOUBLE", "截至查询当天，债券剩余规模，单位，亿元"),
            Col("currencyCD", "STRING", "货币代码。例如，USD-美元；CAD-加元等。对应getSysCode.codeTypeID=10004。"),
            Col("couponTypeCD", "STRING", "计息方式。例如，FIXED-固定利率；ZERO-贴现等。对应getSysCode.codeTypeID=30001。"),
            Col("cpnFreqCD", "STRING", "付息频率。例如，1PY-每年付息；MAT-到期一次还本付息等。对应getSysCode.codeTypeID=30002。"),
            Col("paymentCD", "STRING", "兑付方式。M-一次还本；I-分期还本；P-资产支持证券。对应getSysCode.codeTypeID=30003。"),
            Col("coupon", "DOUBLE", "票面年利率(%)"),
            Col("par", "DOUBLE", "债券面值(元)"),
            Col("hybridCD", "STRING", "混合方式。例如，R-常规债券；W-分离交易可转债等。对应getSysCode.codeTypeID=30005。"),
            Col("typeID", "STRING", "债券分类ID。例如，02020101-国债；0202010201-央行票据。对应getSysCode.codeTypeID=30018。"),
            Col("typeName", "STRING", "分类名称"),
            Col("publishDate", "DATE", "信息发布日期"),
            Col("listDate", "DATE", "上市日期"),
            Col("delistDate", "DATE", "退市日期"),
            Col("actMaturityDate", "DATE", "实际到期日"),
            Col("firstAccrDate", "DATE", "起息日"),
            Col("maturityDate", "DATE", "到期日"),
            Col("firstRedempDate", "DATE", "首次兑付日"),
            Col("minCoupon", "DOUBLE", "保底利率(%)"),
            Col("frnRefRateCD", "STRING", "浮息债参考利率指标。例如，FD1Y-一年期整存整取定期存款利率；B_2W-B_2W银行间7天回购利率(10日算术平均)等。对应getSysCode.codeTypeID=30006。"),
            Col("frnCurrBmkRate", "DOUBLE", "浮息债首次参考利率(%)"),
            Col("frnMargin", "DOUBLE", "浮息债利差(%)"),
            Col("privPlacemFlag", "SHORT", "非公开定向标志"),
            Col("issueInvNum", "SHORT", "初始定向投资人数量"),
            Col("privInvNum", "SHORT", "定向投资人数量"),
            Col("isOption", "INT", "是否含权，是否含赎回或回售选择权。1-是；0-否。对应getSysCode.codeTypeID=10007。"),
            Col("absIssuerID", "LONG", "发起机构ID"),
            Col("absIssuer", "STRING", "发起机构"),
            Col("absLevelCD", "STRING", "分层级别。例如，A-A级；AAA-AAA级等。对应getSysCode.codeTypeID=30007。"),
            Col("absLevelRatio", "DOUBLE", "规模分层占比(%)"),
            Col("absCouponCap", "STRING", "利率上限说明"),
        ],
    },
    "api_getBondCfNew": {
        "table_comment": "getBondCfNew-债券现金流-新输出参数表",
        "endpoint": "/api/bond/getBondCfNew.json",
        "columns": [
            Col("secID", "STRING", "通联编制的证券编码，格式是“交易代码.证券市场代码”，如000002.XSHE。可传入证券交易代码使用getSecID接口获取到。"),
            Col("ticker", "STRING", "交易代码"),
            Col("bondID", "STRING", "债券ID"),
            Col("exchangeCD", "STRING", "交易市场代码"),
            Col("secShortName", "STRING", "债券简称"),
            Col("cashTypeCD", "STRING", "现金流类型。对应getSysCode.codeTypeID=30014"),
            Col("intePeriod", "INT", "计息周期"),
            Col("perAccrDate", "DATE", "本周期计息起始日"),
            Col("perAccrEndDate", "DATE", "本周期计息截止日"),
            Col("paymentDate", "DATE", "现金流日期"),
            Col("recordDate", "DATE", "债权登记日"),
            Col("exDivDate", "DATE", "除权除息日"),
            Col("interest", "DOUBLE", "每百元面额付息"),
            Col("payment", "DOUBLE", "每百元面额兑付本金"),
            Col("totalSize", "DOUBLE", "债券总额"),
        ],
    },
    "api_getBondTicker": {
        "table_comment": "getBondTicker-债券代码对照表输出参数表",
        "endpoint": "/api/bond/getBondTicker.json",
        "columns": [
            Col("bondID", "STRING", "通联编制的债券编码，同一债券在不同交易市场有同一债券ID"),
            Col("secID", "STRING", "通联编制的证券编码。可传入证券交易代码使用getSecID接口获取到。"),
            Col("ticker", "STRING", "证券在证券市场通用的交易代码。"),
            Col("exchangeCD", "STRING", "证券交易市场代码。例如，XSHG-上海证券交易所；XSHE-深圳证券交易所。可在getSysCode接口输入codeTypeID=10002获取到"),
            Col("secShortName", "STRING", "证券简称"),
            Col("secFullName", "STRING", "证券全称"),
        ],
    },
    "api_getBondType": {
        "table_comment": "getBondType-债券类型输出参数表",
        "endpoint": "/api/bond/getBondType.json",
        "columns": [
            Col("secID", "STRING", "证券内部编码，可通过交易代码和交易市场在getSecID获取到。"),
            Col("ticker", "STRING", "交易代码"),
            Col("exchangeCD", "STRING", "通联编制的证券市场编码。例如，XIBE-中国银行间市场；XSHE-深圳证券交易所等。对应getSysCode.codeTypeID=10002。"),
            Col("bondID", "STRING", "债券ID"),
            Col("bondShortName", "STRING", "债券简称"),
            Col("bondFullName", "STRING", "债券全称"),
            Col("typeID", "STRING", "债券分类ID。例如，02020101-国债；0202010201-央行票据。"),
            Col("typeName", "STRING", "债券分类名称"),
        ],
    },
    "api_getCFETSValuation": {
        "table_comment": "getCFETSValuation-中国外汇交易中心估值输出参数表",
        "endpoint": "/api/bond/getCFETSValuation.json",
        "columns": [
            Col("secID", "STRING", "证券内部ID"),
            Col("ticker", "STRING", "债券代码"),
            Col("secShortName", "STRING", "债券简称"),
            Col("tradeDate", "DATE", "估值日期"),
            Col("bondType", "STRING", "债券类型"),
            Col("grossPx", "DOUBLE", "估值全价"),
            Col("netPx", "DOUBLE", "估值净价"),
            Col("ytm", "DOUBLE", "估值收益率"),
            Col("couponType", "STRING", "息票类型"),
            Col("modifiedDuration", "DOUBLE", "估值修正久期"),
            Col("convexity", "DOUBLE", "估值凸性"),
            Col("baseRate", "DOUBLE", "估值基点价值"),
            Col("spreadDuration", "DOUBLE", "估值利差久期"),
            Col("spreadConvexity", "DOUBLE", "估值利差凸性"),
            Col("spotDuration", "DOUBLE", "估值利率久期"),
            Col("spotConvexity", "DOUBLE", "估值利率凸性"),
        ],
    },
    "api_getMktIBBondd": {
        "table_comment": "getMktIBBondd-银行间现券日行情输出参数表",
        "endpoint": "/api/market/getMktIBBondd.json",
        "columns": [
            Col("secID", "STRING", "通联编制的证券编码，可使用getSecID获取"),
            Col("ticker", "STRING", "通用交易代码"),
            Col("secShortName", "STRING", "债券简称"),
            Col("exchangeCD", "STRING", "通联编制的交易市场编码"),
            Col("tradeDate", "DATE", "交易日期"),
            Col("preClosePrice", "DOUBLE", "前收盘净价"),
            Col("preWAVGPrice", "DOUBLE", "前加权平均净价"),
            Col("openPrice", "DOUBLE", "开盘净价"),
            Col("highestPrice", "DOUBLE", "最高净价"),
            Col("lowestPrice", "DOUBLE", "最低净价"),
            Col("closePrice", "DOUBLE", "收盘净价"),
            Col("wAvgPrice", "DOUBLE", "加权平均净价"),
            Col("chgPct", "DOUBLE", "净价涨跌幅"),
            Col("turnoverVol", "DOUBLE", "成交量"),
            Col("preCloseYield", "DOUBLE", "前收盘收益率"),
            Col("preWAVGYield", "DOUBLE", "前加权平均收益率"),
            Col("openYield", "DOUBLE", "开盘收益率"),
            Col("highestYield", "DOUBLE", "最高收益率"),
            Col("lowestYield", "DOUBLE", "最低收益率"),
            Col("closeYield", "DOUBLE", "收盘收益率"),
            Col("wAvgYield", "DOUBLE", "加权平均收益率"),
            Col("grossClosePrice", "DOUBLE", "收盘价(全价)=收盘价+应计利息"),
            Col("accrInterest", "DOUBLE", "应计利息"),
            Col("YTM", "DOUBLE", "到期收益率"),
        ],
    },
}


def chunked(items: list[str], n: int) -> list[list[str]]:
    """按固定大小切片，用于 API 多值参数分批请求。"""

    return [items[i : i + n] for i in range(0, len(items), n)]


def ymd(d: date) -> str:
    """日期对象转 YYYYMMDD 字符串。"""

    return d.strftime("%Y%m%d")


def month_ranges(year: int) -> list[tuple[str, str]]:
    """构造某年的按月时间窗口，便于拆分日频接口请求。"""

    out: list[tuple[str, str]] = []
    start = date(year, 1, 1)
    for m in range(1, 13):
        month_start = date(year, m, 1)
        if m == 12:
            month_end = date(year, 12, 31)
        else:
            month_end = date(year, m + 1, 1) - timedelta(days=1)
        if month_start >= start:
            out.append((ymd(month_start), ymd(month_end)))
            if MONTH_LIMIT > 0 and len(out) >= MONTH_LIMIT:
                break
    return out


def call_api(endpoint: str, params: dict[str, Any], retries: int | None = None, timeout: int | None = None) -> pd.DataFrame:
    """
    请求 Datayes API，并将返回结果解析为 DataFrame。

    - 自动重试（网络抖动/超时）
    - 将 "No Data Returned" 视为空结果而非异常
    """

    retries = API_RETRIES if retries is None else retries
    timeout = API_TIMEOUT if timeout is None else timeout

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept-Encoding": "gzip, deflate",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None and str(v) != "")
    url = f"{BASE_URL}{endpoint}?field=&{query}"
    last_error: Exception | None = None
    for i in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            payload = resp.json()
            if payload.get("retCode") != 1:
                ret_msg = str(payload.get("retMsg", ""))
                if "No Data Returned" in ret_msg:
                    return pd.DataFrame()
                raise RuntimeError(f"{endpoint} failed: {payload.get('retMsg')}")
            return pd.DataFrame(payload.get("data", []))
        except Exception as error:
            last_error = error
            if i < retries - 1:
                time.sleep(2 + i)
                continue
            raise RuntimeError(f"API failed after retries: endpoint={endpoint}, params={params}, err={last_error}")
    raise RuntimeError("unreachable")


def fetch_paginated(endpoint: str, base_params: dict[str, Any], pagesize: int = 500) -> pd.DataFrame:
    """分页拉取某个接口，直到无数据或失败次数达到阈值。"""

    frames: list[pd.DataFrame] = []
    fail_count = 0
    page_upper = API_MAX_PAGES if API_MAX_PAGES > 0 else 20000
    for page in range(1, page_upper + 1):
        params = dict(base_params)
        params["pagenum"] = page
        params["pagesize"] = pagesize
        try:
            df = call_api(endpoint, params, retries=6, timeout=90)
            fail_count = 0
        except Exception:
            fail_count += 1
            if fail_count >= 3:
                break
            continue
        if df.empty:
            break
        frames.append(df)
        if len(df) < pagesize:
            break
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def create_schema(sess: ddb.session) -> None:
    """执行 DOS 脚本建库建表。"""

    if not SCHEMA_DOS.exists():
        raise FileNotFoundError(f"schema dos not found: {SCHEMA_DOS}")
    dos = SCHEMA_DOS.read_text(encoding="utf-8").replace("__DB_PATH__", DB_PATH)
    sess.run(dos)


def ddb_select_expr(columns: list[Col]) -> str:
    """将列定义映射为 DolphinDB select cast 表达式。"""

    type_map = {
        "STRING": "string",
        "DOUBLE": "double",
        "INT": "int",
        "LONG": "long",
        "SHORT": "short",
        "DATE": "date",
    }
    exprs = []
    for c in columns:
        cast = type_map[c.dtype]
        exprs.append(f"{cast}({c.name}) as {c.name}")
    return ",\n           ".join(exprs)


def align_columns(df: pd.DataFrame, columns: list[Col]) -> pd.DataFrame:
    """将 API 返回对齐到目标 schema：补缺列、截断列、处理 DATE 类型。"""

    out = df.copy()
    for c in columns:
        if c.name not in out.columns:
            out[c.name] = pd.NA
    out = out[[c.name for c in columns]]
    for c in columns:
        if c.dtype == "DATE":
            out[c.name] = pd.to_datetime(out[c.name], errors="coerce")
    return out


def append_table(sess: ddb.session, table_name: str, df: pd.DataFrame) -> int:
    """将 DataFrame 写入指定表，返回写入行数。"""

    cols: list[Col] = SCHEMA[table_name]["columns"]
    aligned = align_columns(df, cols)
    if aligned.empty:
        return 0
    sess.upload({"tmp_api_data": aligned})
    expr = ddb_select_expr(cols)
    sql = f'''
loadTable("{DB_PATH}", "{table_name}").append!(
    select {expr}
    from tmp_api_data
)
'''
    sess.run(sql)
    return len(aligned)


def fetch_monthly_all(endpoint: str, year: int, pagesize: int = 500) -> pd.DataFrame:
    """按月拉取全年数据并去重。"""

    frames: list[pd.DataFrame] = []
    for begin_d, end_d in month_ranges(year):
        df = fetch_paginated(endpoint, {"beginDate": begin_d, "endDate": end_d}, pagesize=pagesize)
        if not df.empty:
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).drop_duplicates()


def get_maturity_bond_universe(candidate_tickers: list[str], maturity_years: list[int]) -> pd.DataFrame:
    """根据候选 ticker 回查 getBond，并筛选指定到期年份集合债券池。"""

    if not candidate_tickers:
        return pd.DataFrame()
    frames: list[pd.DataFrame] = []
    for chunk in chunked(candidate_tickers, 40):
        df = fetch_paginated(
            "/api/bond/getBond.json",
            {"ticker": ",".join(chunk)},
            pagesize=500,
        )
        if not df.empty:
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    all_bond = pd.concat(frames, ignore_index=True).drop_duplicates()
    if "maturityDate" in all_bond.columns and maturity_years:
        mat = pd.to_datetime(all_bond["maturityDate"], errors="coerce")
        all_bond = all_bond[mat.dt.year.isin(set(maturity_years))]
    if "secID" in all_bond.columns:
        all_bond = all_bond.drop_duplicates(subset=["secID"])
    return all_bond.reset_index(drop=True)


def fetch_by_multivalue(endpoint: str, key: str, values: list[str], extra_params: dict[str, Any] | None = None, chunk_size: int = 30) -> pd.DataFrame:
    """通过多值参数批量拉取（如 ticker/secID 列表）。"""

    if extra_params is None:
        extra_params = {}
    frames: list[pd.DataFrame] = []
    uniq = [v for v in pd.Series(values).dropna().astype(str).unique().tolist() if v]
    for chunk in chunked(uniq, chunk_size):
        params = dict(extra_params)
        params[key] = ",".join(chunk)
        df = fetch_paginated(endpoint, params, pagesize=500)
        if not df.empty:
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).drop_duplicates()


def main() -> None:
    """主流程：建库建表 -> 数据抓取 -> 入库 -> 导出 -> 校验与摘要。"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    session = ddb.session()
    ok = session.connect(DDB_HOST, DDB_PORT, DDB_USER, DDB_PASSWORD)
    if not ok:
        raise RuntimeError("connect DolphinDB failed")

    create_schema(session)

    market_year_all = fetch_monthly_all("/api/market/getMktIBBondd.json", TARGET_YEAR, pagesize=500)
    candidate_tickers = []
    if not market_year_all.empty and "ticker" in market_year_all.columns:
        candidate_tickers.extend(market_year_all["ticker"].dropna().astype(str).unique().tolist())
    candidate_tickers = pd.Series(candidate_tickers).dropna().astype(str).drop_duplicates().tolist()
    if MAX_CANDIDATE_TICKERS > 0:
        candidate_tickers = candidate_tickers[:MAX_CANDIDATE_TICKERS]

    bond_df = get_maturity_bond_universe(candidate_tickers, MATURITY_YEARS)
    if bond_df.empty:
        raise RuntimeError(
            f"getBond 未拉到到期年份 {','.join(map(str, MATURITY_YEARS))} 的债券数据，请检查 token 或过滤参数"
        )

    secids = bond_df["secID"].dropna().astype(str).unique().tolist() if "secID" in bond_df.columns else []
    tickers = bond_df["ticker"].dropna().astype(str).unique().tolist() if "ticker" in bond_df.columns else []
    bond_ids = bond_df["bondID"].dropna().astype(str).unique().tolist() if "bondID" in bond_df.columns else []

    bond_ticker_df = fetch_by_multivalue("/api/bond/getBondTicker.json", "bondID", bond_ids, chunk_size=40)
    if bond_ticker_df.empty and secids:
        bond_ticker_df = fetch_by_multivalue("/api/bond/getBondTicker.json", "secID", secids, chunk_size=40)

    bond_type_df = fetch_by_multivalue("/api/bond/getBondType.json", "ticker", tickers, chunk_size=40)

    bond_cf_df = fetch_by_multivalue(
        "/api/bond/getBondCfNew.json",
        "ticker",
        tickers,
        extra_params={"beginDate": f"{TARGET_YEAR}0101", "endDate": f"{TARGET_YEAR}1231"},
        chunk_size=20,
    )

    cfets_df = fetch_by_multivalue(
        "/api/bond/getCFETSValuation.json",
        "secID",
        secids,
        extra_params={"beginDate": f"{TARGET_YEAR}0101", "endDate": f"{TARGET_YEAR}1231"},
        chunk_size=20,
    )
    market_df = market_year_all.copy()

    if not market_df.empty:
        market_df = market_df[market_df["secID"].astype(str).isin(set(secids))]
    if not cfets_df.empty:
        cfets_df = cfets_df[cfets_df["secID"].astype(str).isin(set(secids))]

    inserted = {
        "api_getBond": append_table(session, "api_getBond", bond_df),
        "api_getBondCfNew": append_table(session, "api_getBondCfNew", bond_cf_df),
        "api_getBondTicker": append_table(session, "api_getBondTicker", bond_ticker_df),
        "api_getBondType": append_table(session, "api_getBondType", bond_type_df),
        "api_getCFETSValuation": append_table(session, "api_getCFETSValuation", cfets_df),
        "api_getMktIBBondd": append_table(session, "api_getMktIBBondd", market_df),
    }

    for name, df in [
        ("api_getBond", bond_df),
        ("api_getBondCfNew", bond_cf_df),
        ("api_getBondTicker", bond_ticker_df),
        ("api_getBondType", bond_type_df),
        ("api_getCFETSValuation", cfets_df),
        ("api_getMktIBBondd", market_df),
    ]:
        df.to_csv(OUT_DIR / f"{name}.csv", index=False)

    counts = session.run(
        f'''
select * from (
    select "api_getBond" as tableName, count(*) as rows from loadTable("{DB_PATH}", "api_getBond")
    union all
    select "api_getBondCfNew" as tableName, count(*) as rows from loadTable("{DB_PATH}", "api_getBondCfNew")
    union all
    select "api_getBondTicker" as tableName, count(*) as rows from loadTable("{DB_PATH}", "api_getBondTicker")
    union all
    select "api_getBondType" as tableName, count(*) as rows from loadTable("{DB_PATH}", "api_getBondType")
    union all
    select "api_getCFETSValuation" as tableName, count(*) as rows from loadTable("{DB_PATH}", "api_getCFETSValuation")
    union all
    select "api_getMktIBBondd" as tableName, count(*) as rows from loadTable("{DB_PATH}", "api_getMktIBBondd")
)
'''
    )

    counts.to_csv(OUT_DIR / "table_counts.csv", index=False)

    # 字段 comment 校验：统计每张表缺失字段注释数量（应为 0）
    comment_check = session.run(
        f'''
tabs = `api_getBond`api_getBondCfNew`api_getBondTicker`api_getBondType`api_getCFETSValuation`api_getMktIBBondd
res = table(1:0, `tableName`missingColComments, [STRING, INT])
for(tn in tabs){{
    sch = schema(loadTable("{DB_PATH}", string(tn))).colDefs
    miss = exec count(*) from sch where isNull(comment) or trim(string(comment))=""
    insert into res values(string(tn), int(miss))
}}
res
'''
    )
    comment_check.to_csv(OUT_DIR / "comment_check.csv", index=False)

    print("=== 插入行数（本次批次）===")
    for k, v in inserted.items():
        print(f"{k}: {v}")

    print("=== 库内总行数 ===")
    print(counts)
    print("=== 字段注释缺失校验（应全为0） ===")
    print(comment_check)
    print(f"MATURITY_YEARS={MATURITY_YEARS}")
    print(f"MONTH_LIMIT={MONTH_LIMIT}")
    print(f"MAX_CANDIDATE_TICKERS={MAX_CANDIDATE_TICKERS}")
    print(f"API_TIMEOUT={API_TIMEOUT}")
    print(f"API_RETRIES={API_RETRIES}")
    print(f"API_MAX_PAGES={API_MAX_PAGES}")
    print(f"DB_PATH={DB_PATH}")
    print(f"OUT_DIR={OUT_DIR}")


if __name__ == "__main__":
    main()
