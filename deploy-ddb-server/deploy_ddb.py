import paramikoimport sysimport time# ConfigurationHOSTNAME = "192.168.100.45"USERNAME = "jrzhang"PASSWORD = "123456"PORT = 7739TARGET_DIR = "/hdd/hdd9/jrzhang/deploy_test"# Bash Script ContentBASH_SCRIPT = f"""#!/bin/bashset -e# ConfigPORT={PORT}TARGET_DIR="{TARGET_DIR}"DDB_URL="https://www.dolphindb.cn/downloads/DolphinDB_Linux64_V3.00.4.zip"
SERVER_DIR="$TARGET_DIR/server/server"

echo "=== Starting DolphinDB Deployment (Port: $PORT) ==="

# 1. Cleanup
echo "[Step 1] Cleaning up old processes..."
pkill -u {USERNAME} -f "localSite .*$PORT" || true
pkill -u {USERNAME} -f "dolphindb" || true 
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
