#!/usr/bin/env bash
set -euo pipefail

# Copy local wrapper to remote hosts with interactive password prompt (no sshpass required)
# Example:
#   ./distribute_wrapper.sh ~/.local/bin/mihomo jrzhang@192.168.100.43 jrzhang@192.168.100.45

SRC_SCRIPT="${1:-$HOME/.local/bin/mihomo}"
shift || true

if [[ $# -lt 1 ]]; then
  echo "Usage: distribute_wrapper.sh [local_script_path] user@host [user@host ...]"
  exit 1
fi

if [[ ! -f "$SRC_SCRIPT" ]]; then
  echo "[ERR] local script not found: $SRC_SCRIPT"
  exit 1
fi

for host in "$@"; do
  echo "==== $host ===="
  ssh "$host" 'mkdir -p ~/.local/bin'
  scp "$SRC_SCRIPT" "$host":~/.local/bin/mihomo
  ssh "$host" 'chmod +x ~/.local/bin/mihomo && ls -l ~/.local/bin/mihomo'
done

echo "[OK] distribution complete"
