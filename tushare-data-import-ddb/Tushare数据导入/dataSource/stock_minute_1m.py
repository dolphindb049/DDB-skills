#!/usr/bin/env python
# coding: utf-8

import argparse
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
DEFAULT_FREQ = "1min"
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


def configure_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("logger_stock_minute_1m")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_dir / "stock_minute_1m.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import latest Tushare 1-minute stock bars into DolphinDB")
    parser.add_argument("--host", default=basic.session["host"], help="DolphinDB host")
    parser.add_argument("--port", type=int, default=basic.session["port"], help="DolphinDB port")
    parser.add_argument("--username", default=basic.session["username"], help="DolphinDB username")
    parser.add_argument("--password", default=basic.session["password"], help="DolphinDB password")
    parser.add_argument("--token", default=basic.token, help="Tushare token")
    parser.add_argument("--symbols", nargs="*", help="Explicit TS codes to import, e.g. 000001.SZ 600000.SH")
    parser.add_argument("--limit-symbols", type=int, default=0, help="When symbols are omitted, limit the fetched active stock list to the first N codes; 0 means all")
    parser.add_argument("--freq", default=DEFAULT_FREQ, help="Minute frequency, e.g. 1min/5min/15min")
    parser.add_argument("--pause", type=float, default=31.0, help="Pause in seconds between Tushare requests")
    parser.add_argument("--retry-wait", type=float, default=35.0, help="Minimum wait in seconds before retrying a failed Tushare request")
    parser.add_argument("--max-retries", type=int, default=3, help="Maximum retries per symbol")
    parser.add_argument("--batch-size", type=int, default=20, help="Append batch size")
    parser.add_argument("--log-dir", default=basic.logDir, help="Log directory")
    return parser.parse_args()


def get_active_symbols(token: str, limit_symbols: int) -> list[str]:
    ts.set_token(token)
    pro = ts.pro_api()
    data = pro.stock_basic(exchange="", list_status="L", fields="ts_code")
    symbols = data["ts_code"].dropna().astype(str).tolist()
    if limit_symbols > 0:
        return symbols[:limit_symbols]
    return symbols


def normalize_minute_data(frame: pd.DataFrame) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame(columns=DEFAULT_FIELDS)

    data = frame.copy()
    data["trade_time"] = pd.to_datetime(data["trade_time"])
    data["trade_date"] = pd.to_datetime(data["trade_date"], format="%Y%m%d")
    latest_trade_date = data["trade_date"].max()
    data = data.loc[data["trade_date"] == latest_trade_date].copy()
    data["update_time"] = pd.Timestamp.now()
    data = data[DEFAULT_FIELDS]
    data = data.sort_values(["ts_code", "trade_time"]).reset_index(drop=True)
    return data


def fetch_symbol_minute_data(ts_code: str, freq: str, max_retries: int, pause: float, retry_wait: float, logger: logging.Logger) -> pd.DataFrame:
    for attempt in range(1, max_retries + 1):
        try:
            frame = ts.pro_bar(ts_code=ts_code, freq=freq, asset="E")
            data = normalize_minute_data(frame)
            if data.empty:
                logger.info("No minute data returned for %s", ts_code)
            else:
                logger.info("Fetched %d rows for %s, latest trade date %s", len(data), ts_code, data["trade_date"].max())
            return data
        except Exception as exc:
            wait_seconds = max(retry_wait, pause * attempt)
            logger.warning("Attempt %d/%d failed for %s: %s. Waiting %.1f seconds before retry.", attempt, max_retries, ts_code, exc, wait_seconds)
            if attempt == max_retries:
                raise
            time.sleep(wait_seconds)
    return pd.DataFrame(columns=DEFAULT_FIELDS)


def ensure_schema(session: ddb.session, logger: logging.Logger) -> None:
    ddl_script = DDL_FILE.read_text(encoding="utf-8")
    session.run(ddl_script)
    session.run("createStockMinute1m()")
    logger.info("Ensured %s/%s exists", DB_PATH, TABLE_NAME)


def append_frames(appender: ddb.TableAppender, frames: list[pd.DataFrame], logger: logging.Logger) -> int:
    valid_frames = [frame for frame in frames if not frame.empty]
    if not valid_frames:
        return 0
    merged = pd.concat(valid_frames, ignore_index=True)
    appender.append(merged)
    logger.info("Appended %d rows into %s/%s", len(merged), DB_PATH, TABLE_NAME)
    return len(merged)


def verify_import(session: ddb.session) -> tuple[int, str | None]:
    script = f"select count(*) as row_count, max(trade_time) as max_trade_time from loadTable('{DB_PATH}', '{TABLE_NAME}')"
    result = session.run(script)
    return int(result.at[0, "row_count"]), str(result.at[0, "max_trade_time"])


def main() -> None:
    args = parse_args()
    logger = configure_logger(Path(args.log_dir))

    session = ddb.session(args.host, args.port, args.username, args.password)
    ensure_schema(session, logger)

    if args.symbols:
        symbols = args.symbols
    else:
        symbols = get_active_symbols(args.token, args.limit_symbols)

    if not symbols:
        raise ValueError("No symbols resolved for import.")

    ts.set_token(args.token)
    appender = ddb.TableAppender(dbPath=DB_PATH, tableName=TABLE_NAME, ddbSession=session)

    buffered_frames: list[pd.DataFrame] = []
    total_rows = 0
    for index, ts_code in enumerate(symbols, start=1):
        frame = fetch_symbol_minute_data(ts_code, args.freq, args.max_retries, args.pause, args.retry_wait, logger)
        if not frame.empty:
            buffered_frames.append(frame)
        if len(buffered_frames) >= args.batch_size:
            total_rows += append_frames(appender, buffered_frames, logger)
            buffered_frames.clear()
        time.sleep(args.pause)
        logger.info("Processed %d/%d symbols", index, len(symbols))

    total_rows += append_frames(appender, buffered_frames, logger)
    total_count, max_trade_time = verify_import(session)
    logger.info("Import finished. This run appended %d rows. Table row count=%d, max trade_time=%s", total_rows, total_count, max_trade_time)


if __name__ == "__main__":
    main()