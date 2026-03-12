#!/usr/bin/env python
# coding: utf-8

import argparse
import datetime as dt
from pathlib import Path

import tushare as ts

import basic
from dataSource.stock_minute_1m_lib import (
    append_frames,
    build_appender,
    configure_logger,
    create_session,
    date_iter,
    fetch_trade_day_frame,
    filter_existing_rows,
    format_yyyymmdd,
    get_existing_trade_times,
    minute_task_defaults,
    parse_yyyymmdd,
    resolve_symbols,
    summarize_completeness,
    ensure_schema,
    verify_table_state,
)


def parse_args() -> argparse.Namespace:
    defaults = minute_task_defaults()
    today = dt.date.today()
    start_date = today - dt.timedelta(days=defaults["historyDays"] - 1)

    parser = argparse.ArgumentParser(description="Backfill historical A-share 1-minute bars into DolphinDB")
    parser.add_argument("--host", default=basic.session["host"], help="DolphinDB host")
    parser.add_argument("--port", type=int, default=basic.session["port"], help="DolphinDB port")
    parser.add_argument("--username", default=basic.session["username"], help="DolphinDB username")
    parser.add_argument("--password", default=basic.session["password"], help="DolphinDB password")
    parser.add_argument("--token", default=basic.token, help="Tushare token")
    parser.add_argument("--symbols", nargs="*", help="Explicit TS codes to import")
    parser.add_argument("--limit-symbols", type=int, default=0, help="Limit symbol count when symbols are omitted")
    parser.add_argument("--start-date", default=format_yyyymmdd(start_date), help="Backfill start date, format YYYYMMDD")
    parser.add_argument("--end-date", default=format_yyyymmdd(today), help="Backfill end date, format YYYYMMDD")
    parser.add_argument("--freq", default=defaults["freq"], help="Minute frequency")
    parser.add_argument("--pause", type=float, default=defaults["pause"], help="Pause in seconds between Tushare requests")
    parser.add_argument("--retry-wait", type=float, default=defaults["retryWait"], help="Minimum wait in seconds before retrying a failed Tushare request")
    parser.add_argument("--max-retries", type=int, default=defaults["maxRetries"], help="Maximum retries per symbol/date")
    parser.add_argument("--batch-size", type=int, default=defaults["batchSize"], help="Append batch size")
    parser.add_argument("--log-dir", default=basic.logDir, help="Log directory")
    parser.add_argument("--check-after-load", action="store_true", help="Run completeness summary after each trade date")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = configure_logger("logger_AutoLoadMinuteHistory", Path(args.log_dir), "AutoLoadMinuteHistory.log")

    start_date = parse_yyyymmdd(args.start_date)
    end_date = parse_yyyymmdd(args.end_date)
    if end_date < start_date:
        raise ValueError("end_date must be greater than or equal to start_date")

    session = create_session(args.host, args.port, args.username, args.password)
    ensure_schema(session, logger)

    symbols = resolve_symbols(args.token, explicit_symbols=args.symbols, limit_symbols=args.limit_symbols)
    if not symbols:
        raise ValueError("No symbols resolved for backfill.")

    ts.set_token(args.token)
    appender = build_appender(session)

    total_rows = 0
    for trade_date in date_iter(start_date, end_date):
        logger.info("Backfilling trade date %s for %d symbols", trade_date, len(symbols))
        existing_map = get_existing_trade_times(session, symbols, trade_date)
        buffered_frames = []

        for index, ts_code in enumerate(symbols, start=1):
            frame = fetch_trade_day_frame(
                ts_code=ts_code,
                trade_date=trade_date,
                freq=args.freq,
                logger=logger,
                max_retries=args.max_retries,
                pause=args.pause,
                retry_wait=args.retry_wait,
            )
            frame = filter_existing_rows(frame, existing_map.get(ts_code, set()))
            if not frame.empty:
                buffered_frames.append(frame)
            if len(buffered_frames) >= args.batch_size:
                total_rows += append_frames(appender, buffered_frames, logger)
                buffered_frames.clear()
            logger.info("Processed %d/%d symbols for %s", index, len(symbols), trade_date)

        total_rows += append_frames(appender, buffered_frames, logger)

        if args.check_after_load:
            summary, _ = summarize_completeness(session, symbols, trade_date)
            complete_count = int(summary["is_complete"].sum()) if not summary.empty else 0
            logger.info("Completeness for %s: %d/%d symbols complete", trade_date, complete_count, len(symbols))

    row_count, max_trade_time = verify_table_state(session)
    logger.info("History backfill finished. Appended %d rows. Table row count=%d, max_trade_time=%s", total_rows, row_count, max_trade_time)


if __name__ == "__main__":
    main()