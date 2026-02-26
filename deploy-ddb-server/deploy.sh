#!/bin/bash
set -e

# Config
PORT=7739
TARGET_DIR="/hdd/hdd9/jrzhang/deploy_test"
DDB_URL="https://www.dolphindb.cn/downloads/DolphinDB_Linux64_V3.00.4.zip"
SERVER_DIR="$TARGET_DIR/server/server"

echo "=== Starting DolphinDB Deployment (Port: $PORT) ==="

# 1. Cleanup
echo "[Step 1] Cleaning up old processes..."
pkill -u $(whoami) -f "localSite .*$PORT" || true
pkill -u $(whoami) -f "dolphindb" || true 
sleep 2

# 2. Prepare Dir
echo "[Step 2] Preparing directory: $TARGET_DIR"
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# 3. Download
echo "[Step 3] Downloading..."
wget -q "$DDB_URL" -O dolphindb.zip
if [ ! -f dolphindb.zip ]; then
    echo "Download failed"
    exit 1
fi

# 4. Unzip
echo "[Step 4] Unzipping..."
unzip -q -o dolphindb.zip -d server

# 5. Start
echo "[Step 5] Starting server..."
cd "$SERVER_DIR"
chmod +x dolphindb

# Start command (bind 0.0.0.0)
nohup ./dolphindb -localSite 0.0.0.0:$PORT:local$PORT -logFile dolphindb.log > /dev/null 2>&1 &

# Wait
echo "Waiting 5 seconds..."
sleep 5

# 6. Verify
echo "[Step 6] Verifying process..."
if ps aux | grep -v grep | grep "localSite .*$PORT"; then
    echo "SUCCESS: DolphinDB is running"
else
    echo "ERROR: Process not found"
    cat dolphindb.log
    exit 1
fi
