import paramiko
import sys
import time

# Configuration
HOSTNAME = "192.168.100.45"
USERNAME = "jrzhang"
PASSWORD = "123456"
PORT = 7739
TARGET_DIR = "/hdd/hdd9/jrzhang/deploy_test"
SERVER_DIR = f"{TARGET_DIR}/server/server"

# Bash Script Content
BASH_SCRIPT = f"""
#!/bin/bash
set -e

# Config
PORT={PORT}
TARGET_DIR="{TARGET_DIR}"
DDB_URL="https://www.dolphindb.cn/downloads/DolphinDB_Linux64_V3.00.4.zip"
SERVER_DIR="$TARGET_DIR/server/server"
CFG_FILE="$SERVER_DIR/dolphindb.cfg"

echo "=== Starting DolphinDB Deployment (Port: $PORT) ==="

# 1. Cleanup
echo "[Step 1] Cleaning up old processes..."
pkill -u {USERNAME} -f "localSite .*$PORT" || true
pkill -u {USERNAME} -f "dolphindb" || true 
sleep 2

# 2. Prepare Dir
if [ -d "$TARGET_DIR" ]; then
    echo "Directory exists, cleaning up..."
    rm -rf "$TARGET_DIR"
fi
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

# 5. Modify Config
echo "[Step 5] Configuring dolphindb.cfg..."
# Ensure we bind to IP so we can access remotely (using explicit IP or 0.0.0.0 usually safer for access)
# User asked to modify localSite. 
# Default usually commented out or localhost.
# We will append the config.
echo "" >> "$CFG_FILE"
echo "localSite={HOSTNAME}:{PORT}:local{PORT}" >> "$CFG_FILE"
echo "mode=single" >> "$CFG_FILE"

# 6. Create start script
echo "[Step 6] Creating startSingle.sh..."
cd "$SERVER_DIR"
chmod +x dolphindb

cat <<EOF > startSingle.sh
#!/bin/sh
nohup ./dolphindb -console 0 -mode single > single.nohup 2>&1 &
EOF

chmod +x startSingle.sh

# 7. Start
echo "[Step 7] Starting server..."
./startSingle.sh

# Wait
echo "Waiting 5 seconds..."
sleep 5

# 8. Verify
echo "[Step 8] Verifying process..."
if ps aux | grep -v grep | grep "dolphindb"; then
    echo "SUCCESS: DolphinDB is running"
    netstat -tulnp | grep $PORT
else
    echo "ERROR: Process not found"
    cat single.nohup
    exit 1
fi
"""

def deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOSTNAME}...")
        client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        
        print("Sending and executing Bash script...")
        stdin, stdout, stderr = client.exec_command("bash -s")
        stdin.write(BASH_SCRIPT)
        stdin.flush()
        stdin.channel.shutdown_write()

        while True:
            line = stdout.readline()
            if not line:
                break
            print(line, end="")
            
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("\\nDeployment Successful")
        else:
            print(f"\\nDeployment Failed (Code: {exit_status})")
            print("STDERR:", stderr.read().decode())

    finally:
        client.close()

if __name__ == "__main__":
    deploy()
