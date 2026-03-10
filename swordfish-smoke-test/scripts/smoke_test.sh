#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /abs/path/to/swordfish-project"
  exit 2
fi

PROJECT_ROOT="$1"
BUILD_DIR="$PROJECT_ROOT/build"
BIN_DIR="$BUILD_DIR/bin"

if [[ ! -f "$PROJECT_ROOT/CMakeLists.txt" ]]; then
  echo "[FAIL] CMakeLists.txt not found in: $PROJECT_ROOT"
  exit 2
fi

echo "[1/4] Build project ..."
mkdir -p "$BUILD_DIR"
cmake -S "$PROJECT_ROOT" -B "$BUILD_DIR"
cmake --build "$BUILD_DIR" -j8

echo "[2/4] Check runtime assets ..."
for f in dolphindb.dos dolphindb.lic dolphindb.cfg; do
  if [[ ! -f "$BIN_DIR/$f" ]]; then
    echo "[FAIL] Missing runtime file: $BIN_DIR/$f"
    exit 1
  fi
done
if [[ ! -d "$BIN_DIR/dict" ]]; then
  echo "[FAIL] Missing runtime directory: $BIN_DIR/dict"
  exit 1
fi

echo "[3/4] Run baseDemo ..."
BASE_LOG="$(mktemp)"
if ! (cd "$BIN_DIR" && ./baseDemo >"$BASE_LOG" 2>&1); then
  echo "[FAIL] baseDemo failed."
  tail -n 80 "$BASE_LOG"
  exit 1
fi
if ! rg -q "Inintialize DolphinDB runtime" "$BASE_LOG" || ! rg -q "Finalize DolphinDB runtime" "$BASE_LOG"; then
  echo "[FAIL] baseDemo did not show expected init/finalize markers."
  tail -n 80 "$BASE_LOG"
  exit 1
fi

echo "[4/4] Run streamEngineDemo ..."
STREAM_LOG="$(mktemp)"
if ! (cd "$BIN_DIR" && ./streamEngineDemo >"$STREAM_LOG" 2>&1); then
  echo "[FAIL] streamEngineDemo failed."
  tail -n 120 "$STREAM_LOG"
  exit 1
fi
if ! rg -q "create oltp table" "$STREAM_LOG" || ! rg -q "clean environment" "$STREAM_LOG"; then
  echo "[FAIL] streamEngineDemo output missing expected markers."
  tail -n 120 "$STREAM_LOG"
  exit 1
fi

echo "[PASS] Swordfish smoke test passed."
echo "  - Build: OK"
echo "  - baseDemo: OK"
echo "  - streamEngineDemo: OK"
