# Manual Deployment Guide: DolphinDB Single Node

This guide details the manual steps to deploy a specific version of DolphinDB (Single Node) on a Linux server.

## 1. Prerequisites
*   Linux Server (CentOS/Ubuntu/etc.) available via SSH.
*   `unzip` utility installed (`apt install unzip` or `yum install unzip`).
*   Network access to download the binary.

## 2. Download
Download the community edition or your licensed version.
**URL Pattern**: `https://www.dolphindb.cn/downloads/DolphinDB_Linux64_V<VERSION>.zip`

Example:
```bash
wget https://www.dolphindb.cn/downloads/DolphinDB_Linux64_V3.00.4.zip -O dolphindb.zip
```

## 3. Installation
Extract the package.
```bash
unzip dolphindb.zip -d server
cd server/server
chmod +x dolphindb
```

## 4. Configuration (`dolphindb.cfg`)
Located in `/server/dolphindb.cfg`. Critical settings for single node:

```properties
# Set mode to single node
mode=single

# Bind IP and Port
# Syntax: localSite=IP:PORT:ALIAS
# Use the server's actual LAN IP, e.g., 192.168.1.5
localSite=192.168.1.5:8848:local8848

# Essential Params
maxConnections=512
workerNum=4
console=0
```

> **Important**: Do not mix configuration in `dolphindb.cfg` with command line arguments (e.g., `-localSite`). Keep `start.sh` simple: `./dolphindb -logFile dolphindb.log`.

## 5. Startup Script (`start.sh`)
Create a standardized startup script to run in the background.

```bash
#!/bin/bash
# start.sh
nohup ./dolphindb -logFile dolphindb.log > single.nohup 2>&1 &
echo "DolphinDB started. Logs: dolphindb.log"
```

Run it:
```bash
chmod +x start.sh
./start.sh
```

## 6. Verification
Check if the port is listening.
```bash
netstat -tulnp | grep 8848
# OR
ss -tulnp | grep 8848
```

If you see a listener, open your browser: `http://<SERVER_IP>:8848`.
