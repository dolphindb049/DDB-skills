#!/usr/bin/env python
# coding: utf-8

import argparse
import datetime as dt
from pathlib import Path

import tushare as ts

import basic
from dataSource.stock_minute_1m_lib import (
    build_appender,
    configure_logger,
    create_session,
    ensure_schema,
    minute_task_defaults,
    parse_yyyymmdd,
    repair_missing_slots,
    resolve_symbols,
    summarize_completeness,
)


def parse_args() -> argparse.Namespace:
    defaults = minute_task_defaults()
    parser = argparse.ArgumentParser(description="Check or repair completeness of A-share 1-minute bars in DolphinDB")
    parser.add_argument("--host", default=basic.session["host"], help="DolphinDB host")
    parser.add_argument("--port", type=int, default=basic.session["port"], help="DolphinDB port")
    parser.add_argument("--username", default=basic.session["username"], help="DolphinDB username")
    parser.add_argument("--password", default=basic.session["password"], help="DolphinDB password")
    parser.add_argument("--token", default=basic.token, help="Tushare token")
    parser.add_argument("--symbols", nargs="*", help="Explicit TS codes to check")
    parser.add_argument("--limit-symbols", type=int, default=0, help="Limit symbol count when symbols are omitted")
    parser.add_argument("--trade-date", default=dt.date.today().strftime("%Y%m%d"), help="Target trade date, format YYYYMMDD")
    parser.add_argument("--freq", default=defaults["freq"], help="Minute frequency")
    parser.add_argument("--pause", type=float, default=defaults["pause"], help="Pause in seconds between Tushare requests")
    parser.add_argument("--retry-wait", type=float, default=defaults["retryWait"], help="Minimum wait in seconds before retrying a failed Tushare request")
    parser.add_argument("--max-retries", type=int, default=defaults["maxRetries"], help="Maximum retries per symbol")
    parser.add_argument("--repair-missing", action="store_true", help="Repair missing minute bars by refetching the day slice")
    parser.add_argument("--full-day", action="store_true", help="Check against a full trading day instead of only checking up to now")
    parser.add_argument("--log-dir", default=basic.logDir, help="Log directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = configure_logger("logger_CheckMinuteCompleteness", Path(args.log_dir), "CheckMinuteCompleteness.log")

    session = create_session(args.host, args.port, args.username, args.password)
    ensure_schema(session, logger)

    symbols = resolve_symbols(args.token, explicit_symbols=args.symbols, limit_symbols=args.limit_symbols)
    if not symbols:
        raise ValueError("No symbols resolved for completeness check.")

    trade_date = parse_yyyymmdd(args.trade_date)
    reference_now = None if args.full_day else dt.datetime.now()
    summary, missing_map = summarize_completeness(session, symbols, trade_date, as_of=reference_now)

    complete_count = int(summary["is_complete"].sum()) if not summary.empty else 0
    logger.info("Completeness summary for %s: %d/%d symbols complete", trade_date, complete_count, len(symbols))
    for symbol, missing_slots in missing_map.items():
        if missing_slots:
            logger.warning("%s is missing %d minute bars on %s", symbol, len(missing_slots), trade_date)

    if args.repair_missing:
        ts.set_token(args.token)
        appender = build_appender(session)
        appended_rows, before_summary, after_summary = repair_missing_slots(
            session=session,
            appender=appender,
            symbols=symbols,
            trade_date=trade_date,
            freq=args.freq,
            logger=logger,
            max_retries=args.max_retries,
            pause=args.pause,
            retry_wait=args.retry_wait,
            as_of=reference_now,
        )
        logger.info(
            "Repair finished. Appended %d rows. Complete symbols before=%d after=%d",
            appended_rows,
            int(before_summary["is_complete"].sum()) if not before_summary.empty else 0,
            int(after_summary["is_complete"].sum()) if not after_summary.empty else 0,
        )


if __name__ == "__main__":
    main()