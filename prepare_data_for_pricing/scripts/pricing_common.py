from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import dolphindb as ddb
import pandas as pd
import requests

BASE_URL = "https://api.datayes.com/data/v1"
DEFAULT_TOKEN = "4c89993d518c6cb4105870590b923416ecc61d0da7b438f6ace0bb036040a7c4"


@dataclass
class PricingConfig:
    token: str
    pricing_date: str
    tickers: list[str]
    ddb_host: str
    ddb_port: int
    ddb_user: str
    ddb_password: str
    db_path: str


def load_config() -> PricingConfig:
    tickers_env = os.getenv("PRICING_TICKERS", "240025,250015,250401")
    tickers = [item.strip() for item in tickers_env.split(",") if item.strip()]
    return PricingConfig(
        token=os.getenv("DATAYES_TOKEN", DEFAULT_TOKEN),
        pricing_date=os.getenv("PRICING_DATE", "20260105"),
        tickers=tickers,
        ddb_host=os.getenv("DDB_HOST", "127.0.0.1"),
        ddb_port=int(os.getenv("DDB_PORT", "8848")),
        ddb_user=os.getenv("DDB_USER", "admin"),
        ddb_password=os.getenv("DDB_PASSWORD", "123456"),
        db_path=os.getenv("DDB_DB_PATH", "dfs://data_pricing_skill"),
    )


class DatayesClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Encoding": "gzip, deflate",
        }

    def get(self, endpoint: str, params: dict[str, Any]) -> pd.DataFrame:
        query = "&".join(f"{key}={value}" for key, value in params.items() if value is not None)
        url = f"{BASE_URL}{endpoint}?field=&{query}"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        payload = response.json()
        if payload.get("retCode") != 1:
            raise RuntimeError(f"{endpoint} failed: {payload.get('retMsg')}")
        return pd.DataFrame(payload.get("data", []))


def ymd_to_iso(date_ymd: str) -> str:
    return datetime.strptime(date_ymd, "%Y%m%d").strftime("%Y-%m-%d")


def ymd_to_dot(date_ymd: str) -> str:
    return datetime.strptime(date_ymd, "%Y%m%d").strftime("%Y.%m.%d")


def tenor_to_curve_date(pricing_date: str, tenor: str) -> str:
    base_date = pd.Timestamp(datetime.strptime(pricing_date, "%Y%m%d"))
    normalized = tenor.upper().strip()
    if normalized.endswith("D"):
        shifted = base_date + pd.DateOffset(days=int(normalized[:-1]))
    elif normalized.endswith("W"):
        shifted = base_date + pd.DateOffset(weeks=int(normalized[:-1]))
    elif normalized.endswith("M"):
        shifted = base_date + pd.DateOffset(months=int(normalized[:-1]))
    elif normalized.endswith("Y"):
        shifted = base_date + pd.DateOffset(years=int(normalized[:-1]))
    else:
        raise ValueError(f"unsupported tenor format: {tenor}")
    return shifted.strftime("%Y.%m.%d")


def connect_ddb(cfg: PricingConfig) -> ddb.session:
    session = ddb.session()
    success = session.connect(cfg.ddb_host, cfg.ddb_port, cfg.ddb_user, cfg.ddb_password)
    if not success:
        raise RuntimeError("failed to connect DolphinDB")
    return session


def write_json_records(path: str, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handler:
        json.dump(rows, handler, ensure_ascii=False, indent=2)


def read_json_records(path: str) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as handler:
        rows = json.load(handler)
    return pd.DataFrame(rows)


def map_frequency(freq_code: str) -> str:
    mapping = {
        "MAT": "Once",
        "1PY": "Annual",
        "2PY": "Semiannual",
        "4PY": "Quarterly",
        "6PY": "BiMonthly",
        "12PY": "Monthly",
    }
    return mapping.get(freq_code, "Annual")


def pick_fixed_bond_rows(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    target = df[df["ticker"].astype(str) == str(ticker)].copy() if "ticker" in df.columns else df.copy()
    target = target[target["couponTypeCD"].eq("FIXED")]
    if target.empty:
        return target
    preferred = target[target["exchangeCD"].isin(["XIBE", "OTC"])]
    if not preferred.empty:
        target = preferred
    target = target.sort_values(["exchangeCD", "maturityDate"]).drop_duplicates(subset=["secID"])
    return target
