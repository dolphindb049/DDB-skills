---
name: ddb-deployment-skill
description: A step-by-step interactive guide to deploying and debugging DolphinDB Single Node. Focuses on granular commands for error detection.
license: MIT
metadata:
  author: ddb-user
  version: "1.1.0"
---

# DolphinDB Deployment & Debugging Skill

This skill guides you through the deployment process using **atomic, verifiable bash commands**. Instead of running a black-box script, you execute these steps one by one to ensure success at each stage.

## 📍 Phase 1: Environment & Cleanup

**Goal**: Ensure the port is free and define where we install.

1.  **Define Variables** (Copy this block to your terminal)
    ```bash
    # Set your target version and port
    export DDB_VERSION="3.00.4.0"
    export DDB_PORT=7739
    export INSTALL_DIR="/hdd/hdd9/jrzhang/deploy_test"
    export LOCAL_IP=$(hostname -I | awk '{print $1}')
    
    echo "Deploying V$DDB_VERSION on $LOCAL_IP:$DDB_PORT at $INSTALL_DIR"
    ```

2.  **Check for conflicts**
    ```bash
    # Ensure port is not in use
    lsof -i:$DDB_PORT
    # If satisfied (empty output), proceed.
    ```

3.  **Prepare Directory**
    ```bash
    mkdir -p $INSTALL_DIR
    cd $INSTALL_DIR
    ```

## 📦 Phase 2: Installation

**Goal**: Get the binaries ready.

1.  **Download** (Skip if file exists)
    ```bash
    if [ ! -f "dolphindb.zip" ]; then
        wget -q "https://www.dolphindb.cn/downloads/DolphinDB_Linux64_V${DDB_VERSION}.zip" -O dolphindb.zip
        echo "Download complete."
    else
        echo "Zip file exists. Skipping verify."
    fi
    ```

2.  **Extract**
    ```bash
    unzip -q -o dolphindb.zip -d server
    chmod +x server/server/dolphindb
    ```

## ⚙️ Phase 3: Configuration (Critical)

**Goal**: Write a clean, conflict-free configuration file.

> **💡 Experience Note**: 
> 1. Always **overwrite** (`>`) config files instead of appending (`>>`). Appending creates duplicate keys, and DolphinDB only reads the first one (often the wrong one).
> 2. Ensure `localSite` explicitly binds to the LAN IP (e.g., `192.168.x.x`), not `localhost`, or you won't be able to access it remotely.

1.  **Backup existing config**
    ```bash
    cd server/server
    [ -f dolphindb.cfg ] && cp dolphindb.cfg dolphindb.cfg.bak
    ```

2.  **Write Config (Overwrite mode)**
    *   *Why*: Appending causes duplicate keys (e.g., `localSite` defined twice).
    *   *Command*:
    ```bash
    cat <<EOF > dolphindb.cfg
    mode=single
    localSite=$LOCAL_IP:$DDB_PORT:local$DDB_PORT
    maxMemSize=4
    maxConnections=512
    workerNum=4
    console=0
    EOF
    ```

3.  **Verify Config Content**
    ```bash
    cat dolphindb.cfg
    # CHECK: Ensure 'localSite' matches your IP:PORT and appears ONLY ONCE.
    ```

## 🚀 Phase 4: Start & Verify

**Goal**: Start the process safely and confirm it is working.

1.  **Safe Stop (By Port)**
    *   ⚠️ **Crucial**: Never run `pkill dolphindb` on a shared server! It will kill everyone's jobs.
    *   Stop only the process listening on your specific port:
    ```bash
    PID=$(lsof -t -i:$DDB_PORT -sTCP:LISTEN)
    if [ -n "$PID" ]; then 
        echo "Stopping existing process on port $DDB_PORT (PID $PID)..."
        kill $PID
        sleep 2
    else
        echo "Port $DDB_PORT is free."
    fi
    ```

2.  **Start Server**
    ```bash
    # Start in background
    nohup ./dolphindb -logFile dolphindb.log > single.nohup 2>&1 &
    
    # Get New PID
    sleep 1
    NEW_PID=$(pgrep -n dolphindb)
    echo "New Process ID: $NEW_PID"
    ```

3.  **Immediate Log Check** (The most common point of failure)
    ```bash
    head -n 20 dolphindb.log
    # CHECK: Look for "localSite =" line. Does it match your expectation?
    ```

3.  **Network Verification** (The "True" Test)
    ```bash
    # Check if LISTENING
    lsof -i:$DDB_PORT
    
    # Or use netstat
    netstat -tulnp | grep $DDB_PORT
    ```
    *   ✅ **Success**: You see `LISTEN` on your specific IP (or `*:7739`).
    *   ❌ **Fail**: Empty output? Check `tail dolphindb.log` for license errors or immediate crash.

## 🛠️ Phase 5: Debugging Cheat Sheet

If `lsof` returns nothing:

1.  **Check complete log tail**:
    ```bash
    tail -n 50 dolphindb.log
    ```
2.  **Check if bound to localhost instead**:
    ```bash
    lsof -i | grep dolphindb
    ```
3.  **Test Internal Connectivity**:
    ```bash
    curl -v http://$LOCAL_IP:$DDB_PORT
    ```
