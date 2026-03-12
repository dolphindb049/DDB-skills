#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import datetime as dt
import logging
import sys
import time
from pathlib import Path

import dolphindb as ddb
import pandas as pd
import tushare as ts

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import basic


DB_PATH = "dfs://minute_factor"
TABLE_NAME = "stock_minute_1m"
DDL_FILE = ROOT_DIR / "CreateMinuteDBTB.dos"
DEFAULT_FIELDS = [
    "ts_code",
    "trade_date",
    "trade_time",
    "open",
    "high",
    "low",
    "close",
    "vol",
    "amount",
    "pre_close",
    "change",
    "pct_chg",
    "update_time",
]
MORNING_START = dt.time(9, 30)
MORNING_END = dt.time(11, 30)
AFTERNOON_START = dt.time(13, 1)
AFTERNOON_END = dt.time(15, 0)
FULL_DAY_BAR_COUNT = 241


def configure_logger(name: str, log_dir: Path, file_name: str) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_dir / file_name, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def create_session(host: str, port: int, username: str, password: str) -> ddb.session:
    return ddb.session(host, port, username, password)


def ensure_schema(session: ddb.session, logger: logging.Logger) -> None:
    ddl_script = DDL_FILE.read_text(encoding="utf-8")
    session.run(ddl_script)
    session.run("createStockMinute1m()")
    logger.info("Ensured %s/%s exists", DB_PATH, TABLE_NAME)


def build_appender(session: ddb.session) -> ddb.TableAppender:
    return ddb.TableAppender(dbPath=DB_PATH, tableName=TABLE_NAME, ddbSession=session)


def get_active_symbols(token: str, limit_symbols: int = 0) -> list[str]:
    ts.set_token(token)
    pro = ts.pro_api()
    data = pro.stock_basic(exchange="", list_status="L", fields="ts_code")
    symbols = data["ts_code"].dropna().astype(str).tolist()
    if limit_symbols > 0:
        return symbols[:limit_symbols]
    return symbols


def resolve_symbols(token: str, explicit_symbols: list[str] | None = None, limit_symbols: int = 0) -> list[str]:
    if explicit_symbols:
        return list(dict.fromkeys(explicit_symbols))

    configured_symbols = basic.minuteTask.get("symbols", [])
    if configured_symbols:
        symbols = list(dict.fromkeys(configured_symbols))
        if limit_symbols > 0:
            return symbols[:limit_symbols]
        return symbols

    return get_active_symbols(token, limit_symbols=limit_symbols)


def parse_yyyymmdd(value: str) -> dt.date:
    return dt.datetime.strptime(value, "%Y%m%d").date()


def format_yyyymmdd(value: dt.date) -> str:
    return value.strftime("%Y%m%d")


def date_iter(start_date: dt.date, end_date: dt.date) -> list[dt.date]:
    step_count = (end_date - start_date).days
    return [start_date + dt.timedelta(days=offset) for offset in range(step_count + 1)]


def minute_task_defaults() -> dict:
    return basic.minuteTask.copy()


def chunked_symbols(symbols: list[str], chunk_size: int) -> list[list[str]]:
    if chunk_size <= 0:
        chunk_size = len(symbols) or 1
    return [symbols[index:index + chunk_size] for index in range(0, len(symbols), chunk_size)]


def expected_trade_times(trade_date: dt.date, as_of: dt.datetime | None = None) -> list[pd.Timestamp]:
    morning = pd.date_range(
        f"{trade_date.isoformat()} {MORNING_START.strftime('%H:%M:%S')}",
        f"{trade_date.isoformat()} {MORNING_END.strftime('%H:%M:%S')}",
        freq="1min",
    )
    afternoon = pd.date_range(
        f"{trade_date.isoformat()} {AFTERNOON_START.strftime('%H:%M:%S')}",
        f"{trade_date.isoformat()} {AFTERNOON_END.strftime('%H:%M:%S')}",
        freq="1min",
    )
    full_slots = list(morning) + list(afternoon)

    if as_of is None:
        return full_slots

    if as_of.date() < trade_date:
        return []
    if as_of.date() > trade_date:
        return full_slots

    cutoff = pd.Timestamp(as_of.replace(second=0, microsecond=0))
    return [slot for slot in full_slots if slot <= cutoff]


def in_trading_session(now: dt.datetime) -> bool:
    current_time = now.time()
    morning_open = MORNING_START <= current_time <= MORNING_END
    afternoon_open = AFTERNOON_START <= current_time <= AFTERNOON_END
    return morning_open or afternoon_open


def current_trade_end(trade_date: dt.date, now: dt.datetime | None = None) -> dt.datetime:
    reference = now or dt.datetime.now()
    day_close = dt.datetime.combine(trade_date, AFTERNOON_END)
    if reference.date() > trade_date:
        return day_close
    if reference.date() < trade_date:
        return dt.datetime.combine(trade_date, MORNING_START)
    return min(reference.replace(second=0, microsecond=0), day_close)


def normalize_minute_data(
    frame: pd.DataFrame | None,
    trade_date: dt.date | None = None,
    min_trade_time: pd.Timestamp | None = None,
) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame(columns=DEFAULT_FIELDS)

    data = frame.copy()
    data["ts_code"] = data["ts_code"].astype(str)
    data["trade_time"] = pd.to_datetime(data["trade_time"])
    data["trade_date"] = pd.to_datetime(data["trade_date"], format="%Y%m%d", errors="coerce")

    if trade_date is None:
        latest_trade_date = data["trade_date"].max()
        data = data.loc[data["trade_date"] == latest_trade_date].copy()
    else:
        target_date = pd.Timestamp(trade_date)
        data = data.loc[data["trade_date"] == target_date].copy()

    if min_trade_time is not None:
        data = data.loc[data["trade_time"] > pd.Timestamp(min_trade_time)].copy()

    data["update_time"] = pd.Timestamp.now().floor("s")
    data = data[DEFAULT_FIELDS]
    data = data.sort_values(["ts_code", "trade_time"]).drop_duplicates(["ts_code", "trade_time"], keep="last")
    data = data.reset_index(drop=True)
    return data


def normalize_rt_min_data(frame: pd.DataFrame | None, trade_date: dt.date | None = None) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame(columns=DEFAULT_FIELDS)

    data = frame.copy()
    if "time" in data.columns and "trade_time" not in data.columns:
        data = data.rename(columns={"time": "trade_time"})

    data["ts_code"] = data["ts_code"].astype(str)
    data["trade_time"] = pd.to_datetime(data["trade_time"])
    data["trade_date"] = data["trade_time"].dt.floor("D")

    if trade_date is not None:
        target_date = pd.Timestamp(trade_date)
        data = data.loc[data["trade_date"] == target_date].copy()

    for numeric_column in ["open", "high", "low", "close", "vol", "amount"]:
        if numeric_column in data.columns:
            data[numeric_column] = pd.to_numeric(data[numeric_column], errors="coerce")

    data = data.sort_values(["ts_code", "trade_time"]).reset_index(drop=True)
    data["pre_close"] = data.groupby("ts_code")["close"].shift(1)
    data["change"] = data["close"] - data["pre_close"]
    data["pct_chg"] = (data["change"] / data["pre_close"] * 100).where(data["pre_close"].ne(0))
    data["update_time"] = pd.Timestamp.now().floor("s")
    data = data[DEFAULT_FIELDS]
    data = data.drop_duplicates(["ts_code", "trade_time"], keep="last").reset_index(drop=True)
    return data


def fetch_realtime_batch_frame(
    ts_codes: list[str],
    freq: str,
    logger: logging.Logger,
    max_retries: int,
    pause: float,
    retry_wait: float,
    trade_date: dt.date | None = None,
) -> pd.DataFrame:
    if not ts_codes:
        return pd.DataFrame(columns=DEFAULT_FIELDS)

    query_codes = ",".join(ts_codes)
    query_freq = freq.upper()
    pro = ts.pro_api()
    for attempt in range(1, max_retries + 1):
        try:
            frame = pro.rt_min(ts_code=query_codes, freq=query_freq)
            data = normalize_rt_min_data(frame, trade_date=trade_date)
            if data.empty:
                logger.info("No realtime minute data returned for batch %s", query_codes)
            else:
                logger.info("Fetched %d realtime rows for batch %s", len(data), query_codes)
            return data
        except Exception as exc:
            wait_seconds = max(retry_wait, pause * attempt)
            logger.warning(
                "Attempt %d/%d failed for realtime batch %s: %s. Waiting %.1f seconds before retry.",
                attempt,
                max_retries,
                query_codes,
                exc,
                wait_seconds,
            )
            if attempt == max_retries:
                raise
            time.sleep(wait_seconds)
    return pd.DataFrame(columns=DEFAULT_FIELDS)


def fetch_trade_day_frame(
    ts_code: str,
    trade_date: dt.date,
    freq: str,
    logger: logging.Logger,
    max_retries: int,
    pause: float,
    retry_wait: float,
    end_time: dt.datetime | None = None,
) -> pd.DataFrame:
    start_time = dt.datetime.combine(trade_date, MORNING_START)
    final_end_time = end_time or dt.datetime.combine(trade_date, AFTERNOON_END)
    if final_end_time <= start_time:
        return pd.DataFrame(columns=DEFAULT_FIELDS)

    for attempt in range(1, max_retries + 1):
        try:
            frame = ts.pro_bar(
                ts_code=ts_code,
                freq=freq,
                asset="E",
                start_date=start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end_date=final_end_time.strftime("%Y-%m-%d %H:%M:%S"),
            )
            data = normalize_minute_data(frame, trade_date=trade_date)
            if data.empty:
                logger.info("No minute data returned for %s on %s", ts_code, trade_date)
            else:
                logger.info("Fetched %d rows for %s on %s", len(data), ts_code, trade_date)
            return data
        except Exception as exc:
            wait_seconds = max(retry_wait, pause * attempt)
            logger.warning(
                "Attempt %d/%d failed for %s on %s: %s. Waiting %.1f seconds before retry.",
                attempt,
                max_retries,
                ts_code,
                trade_date,
                exc,
                wait_seconds,
            )
            if attempt == max_retries:
                raise
            time.sleep(wait_seconds)
    return pd.DataFrame(columns=DEFAULT_FIELDS)


def filter_existing_rows(frame: pd.DataFrame, existing_times: set[pd.Timestamp] | None) -> pd.DataFrame:
    if frame.empty or not existing_times:
        return frame
    return frame.loc[~frame["trade_time"].isin(existing_times)].reset_index(drop=True)


def append_frames(appender: ddb.TableAppender, frames: list[pd.DataFrame], logger: logging.Logger) -> int:
    valid_frames = [frame for frame in frames if not frame.empty]
    if not valid_frames:
        return 0
    merged = pd.concat(valid_frames, ignore_index=True)
    appender.append(merged)
    logger.info("Appended %d rows into %s/%s", len(merged), DB_PATH, TABLE_NAME)
    return len(merged)


def _dolphindb_trade_date(trade_date: dt.date) -> str:
    return trade_date.strftime("%Y.%m.%d")


def _dolphindb_symbol_list(symbols: list[str]) -> str:
    return "[" + ",".join(f"'{symbol}'" for symbol in symbols) + "]"


def get_existing_watermarks(session: ddb.session, symbols: list[str], trade_date: dt.date) -> dict[str, pd.Timestamp]:
    if not symbols:
        return {}

    script = (
        f"select ts_code, max(trade_time) as max_trade_time "
        f"from loadTable('{DB_PATH}', '{TABLE_NAME}') "
        f"where trade_date={_dolphindb_trade_date(trade_date)} and ts_code in {_dolphindb_symbol_list(symbols)} "
        f"group by ts_code"
    )
    result = session.run(script)
    if not isinstance(result, pd.DataFrame) or result.empty:
        return {}
    return {
        row["ts_code"]: pd.Timestamp(row["max_trade_time"])
        for _, row in result.iterrows()
        if pd.notna(row["max_trade_time"])
    }


def get_existing_trade_times(session: ddb.session, symbols: list[str], trade_date: dt.date) -> dict[str, set[pd.Timestamp]]:
    existing = {symbol: set() for symbol in symbols}
    if not symbols:
        return existing

    script = (
        f"select ts_code, trade_time "
        f"from loadTable('{DB_PATH}', '{TABLE_NAME}') "
        f"where trade_date={_dolphindb_trade_date(trade_date)} and ts_code in {_dolphindb_symbol_list(symbols)}"
    )
    result = session.run(script)
    if not isinstance(result, pd.DataFrame) or result.empty:
        return existing

    result["trade_time"] = pd.to_datetime(result["trade_time"])
    for ts_code, group in result.groupby("ts_code"):
        existing[str(ts_code)] = set(group["trade_time"].tolist())
    return existing


def summarize_completeness(
    session: ddb.session,
    symbols: list[str],
    trade_date: dt.date,
    as_of: dt.datetime | None = None,
) -> tuple[pd.DataFrame, dict[str, list[pd.Timestamp]]]:
    expected_slots = expected_trade_times(trade_date, as_of=as_of)
    expected_set = set(expected_slots)
    existing_map = get_existing_trade_times(session, symbols, trade_date)

    summary_rows = []
    missing_map: dict[str, list[pd.Timestamp]] = {}
    for symbol in symbols:
        existing_times = existing_map.get(symbol, set())
        missing_slots = sorted(expected_set - existing_times)
        missing_map[symbol] = missing_slots
        summary_rows.append(
            {
                "ts_code": symbol,
                "trade_date": trade_date.isoformat(),
                "expected_count": len(expected_slots),
                "actual_count": len(existing_times),
                "missing_count": len(missing_slots),
                "is_complete": len(missing_slots) == 0,
            }
        )

    return pd.DataFrame(summary_rows), missing_map


def repair_missing_slots(
    session: ddb.session,
    appender: ddb.TableAppender,
    symbols: list[str],
    trade_date: dt.date,
    freq: str,
    logger: logging.Logger,
    max_retries: int,
    pause: float,
    retry_wait: float,
    as_of: dt.datetime | None = None,
) -> tuple[int, pd.DataFrame, pd.DataFrame]:
    before_summary, missing_map = summarize_completeness(session, symbols, trade_date, as_of=as_of)
    end_time = current_trade_end(trade_date, now=as_of) if as_of is not None else None

    frames_to_append = []
    for symbol in symbols:
        missing_slots = set(missing_map.get(symbol, []))
        if not missing_slots:
            continue
        frame = fetch_trade_day_frame(
            ts_code=symbol,
            trade_date=trade_date,
            freq=freq,
            logger=logger,
            max_retries=max_retries,
            pause=pause,
            retry_wait=retry_wait,
            end_time=end_time,
        )
        if frame.empty:
            continue
        frames_to_append.append(frame.loc[frame["trade_time"].isin(missing_slots)].reset_index(drop=True))
        time.sleep(pause)

    appended_rows = append_frames(appender, frames_to_append, logger)
    after_summary, _ = summarize_completeness(session, symbols, trade_date, as_of=as_of)
    return appended_rows, before_summary, after_summary


def verify_table_state(session: ddb.session) -> tuple[int, str | None]:
    script = f"select count(*) as row_count, max(trade_time) as max_trade_time from loadTable('{DB_PATH}', '{TABLE_NAME}')"
    result = session.run(script)
    return int(result.at[0, "row_count"]), str(result.at[0, "max_trade_time"])


def loop_sleep(loop_started_at: float, interval_seconds: float) -> None:
    elapsed = time.time() - loop_started_at
    if elapsed < interval_seconds:
        time.sleep(interval_seconds - elapsed)