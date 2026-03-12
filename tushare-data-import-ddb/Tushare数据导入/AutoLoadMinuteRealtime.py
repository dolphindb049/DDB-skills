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
    chunked_symbols,
    configure_logger,
    create_session,
    ensure_schema,
    fetch_realtime_batch_frame,
    filter_existing_rows,
    get_active_symbols,
    get_existing_watermarks,
    in_trading_session,
    loop_sleep,
    minute_task_defaults,
    repair_missing_slots,
    resolve_symbols,
    verify_table_state,
)


def parse_args() -> argparse.Namespace:
    defaults = minute_task_defaults()
    parser = argparse.ArgumentParser(description="Incrementally append current-day 1-minute bars into DolphinDB every minute")
    parser.add_argument("--host", default=basic.session["host"], help="DolphinDB host")
    parser.add_argument("--port", type=int, default=basic.session["port"], help="DolphinDB port")
    parser.add_argument("--username", default=basic.session["username"], help="DolphinDB username")
    parser.add_argument("--password", default=basic.session["password"], help="DolphinDB password")
    parser.add_argument("--token", default=basic.token, help="Tushare token")
    parser.add_argument("--symbols", nargs="*", help="Explicit TS codes to import")
    parser.add_argument("--all-active-symbols", action="store_true", help="Ignore basic.py configured symbols and use the full active stock list")
    parser.add_argument("--limit-symbols", type=int, default=0, help="Limit symbol count when symbols are omitted")
    parser.add_argument("--freq", default=defaults["freq"], help="Minute frequency")
    parser.add_argument("--pause", type=float, default=defaults["pause"], help="Pause in seconds between Tushare requests")
    parser.add_argument("--retry-wait", type=float, default=defaults["retryWait"], help="Minimum wait in seconds before retrying a failed Tushare request")
    parser.add_argument("--max-retries", type=int, default=defaults["maxRetries"], help="Maximum retries per symbol")
    parser.add_argument("--batch-size", type=int, default=defaults["batchSize"], help="Append batch size")
    parser.add_argument("--api-batch-codes", type=int, default=defaults["apiBatchCodes"], help="How many symbols to request together in one rt_min call")
    parser.add_argument("--loop-interval-seconds", type=float, default=defaults["loopIntervalSeconds"], help="Loop interval in seconds")
    parser.add_argument("--check-every-loops", type=int, default=defaults["checkEveryLoops"], help="Run completeness check every N loops")
    parser.add_argument("--max-batches-per-loop", type=int, default=0, help="Limit the number of rt_min batches processed in each loop; 0 means all batches")
    parser.add_argument("--trade-date", help="Force a target trade date, format YYYYMMDD")
    parser.add_argument("--run-once", action="store_true", help="Only run one incremental cycle")
    parser.add_argument("--repair-missing", action="store_true", help="Repair intraday missing bars during periodic completeness checks")
    parser.add_argument("--exit-after-close", action="store_true", help="Exit once market close checks are finished")
    parser.add_argument("--log-dir", default=basic.logDir, help="Log directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = configure_logger("logger_AutoLoadMinuteRealtime", Path(args.log_dir), "AutoLoadMinuteRealtime.log")

    session = create_session(args.host, args.port, args.username, args.password)
    ensure_schema(session, logger)

    if args.all_active_symbols:
        symbols = get_active_symbols(args.token, limit_symbols=args.limit_symbols)
    else:
        symbols = resolve_symbols(args.token, explicit_symbols=args.symbols, limit_symbols=args.limit_symbols)
    if not symbols:
        raise ValueError("No symbols resolved for realtime minute import.")

    ts.set_token(args.token)
    appender = build_appender(session)

    loop_index = 0
    batch_cursor = 0
    while True:
        loop_index += 1
        loop_started_at = dt.datetime.now()
        reference_trade_date = dt.datetime.strptime(args.trade_date, "%Y%m%d").date() if args.trade_date else loop_started_at.date()

        if args.exit_after_close and loop_started_at.date() == reference_trade_date and loop_started_at.time() > dt.time(15, 0):
            logger.info("Market already closed for %s, running final completeness pass before exit.", reference_trade_date)
            if args.repair_missing:
                appended_rows, before_summary, after_summary = repair_missing_slots(
                    session=session,
                    appender=appender,
                    symbols=symbols,
                    trade_date=reference_trade_date,
                    freq=args.freq,
                    logger=logger,
                    max_retries=args.max_retries,
                    pause=args.pause,
                    retry_wait=args.retry_wait,
                    as_of=loop_started_at,
                )
                logger.info(
                    "Final completeness repair appended %d rows. Complete symbols before=%d after=%d",
                    appended_rows,
                    int(before_summary["is_complete"].sum()) if not before_summary.empty else 0,
                    int(after_summary["is_complete"].sum()) if not after_summary.empty else 0,
                )
            break

        if in_trading_session(loop_started_at):
            logger.info("Starting incremental loop %d for %s", loop_index, reference_trade_date)
            watermarks = get_existing_watermarks(session, symbols, reference_trade_date)
            incremental_frames = []
            all_symbol_batches = chunked_symbols(symbols, args.api_batch_codes)
            if args.max_batches_per_loop > 0:
                selected_batches = []
                for offset in range(args.max_batches_per_loop):
                    batch_index = (batch_cursor + offset) % len(all_symbol_batches)
                    selected_batches.append(all_symbol_batches[batch_index])
                batch_cursor = (batch_cursor + args.max_batches_per_loop) % len(all_symbol_batches)
            else:
                selected_batches = all_symbol_batches

            for batch_index, symbol_batch in enumerate(selected_batches, start=1):
                frame = fetch_realtime_batch_frame(
                    ts_codes=symbol_batch,
                    freq=args.freq,
                    logger=logger,
                    max_retries=args.max_retries,
                    pause=args.pause,
                    retry_wait=args.retry_wait,
                    trade_date=reference_trade_date,
                )
                if not frame.empty:
                    filtered_frames = []
                    for ts_code, ts_frame in frame.groupby("ts_code"):
                        watermark = watermarks.get(ts_code)
                        if watermark is not None:
                            ts_frame = ts_frame.loc[ts_frame["trade_time"] > watermark].reset_index(drop=True)
                        ts_frame = filter_existing_rows(ts_frame, None)
                        if not ts_frame.empty:
                            filtered_frames.append(ts_frame)
                    if filtered_frames:
                        incremental_frames.extend(filtered_frames)
                if len(incremental_frames) >= args.batch_size:
                    append_frames(appender, incremental_frames, logger)
                    incremental_frames.clear()
                logger.info("Processed realtime batch %d/%d in loop %d", batch_index, len(selected_batches), loop_index)

            append_frames(appender, incremental_frames, logger)
        else:
            logger.info("Loop %d is outside the trading session for %s, skipping incremental fetch.", loop_index, reference_trade_date)

        if args.repair_missing and loop_index % max(args.check_every_loops, 1) == 0:
            appended_rows, before_summary, after_summary = repair_missing_slots(
                session=session,
                appender=appender,
                symbols=symbols,
                trade_date=reference_trade_date,
                freq=args.freq,
                logger=logger,
                max_retries=args.max_retries,
                pause=args.pause,
                retry_wait=args.retry_wait,
                as_of=loop_started_at,
            )
            logger.info(
                "Loop %d completeness repair appended %d rows. Complete symbols before=%d after=%d",
                loop_index,
                appended_rows,
                int(before_summary["is_complete"].sum()) if not before_summary.empty else 0,
                int(after_summary["is_complete"].sum()) if not after_summary.empty else 0,
            )

        row_count, max_trade_time = verify_table_state(session)
        logger.info("Loop %d finished. Table row count=%d, max_trade_time=%s", loop_index, row_count, max_trade_time)

        if args.run_once:
            break
        loop_sleep(loop_started_at.timestamp(), args.loop_interval_seconds)


if __name__ == "__main__":
    main()