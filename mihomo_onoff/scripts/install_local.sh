#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  install_local.sh --binary-gz /path/to/mihomo-linux-amd64-*.gz --subscription-url URL [--base-dir DIR]

Options:
  --binary-gz        Local path of Mihomo gzip binary
  --subscription-url Clash subscription URL (YAML or compatible)
  --base-dir         Base directory for config/log (default: $HOME/clash)
USAGE
}

BINARY_GZ=""
SUB_URL=""
BASE_DIR="$HOME/clash"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --binary-gz)
      BINARY_GZ="$2"; shift 2 ;;
    --subscription-url)
      SUB_URL="$2"; shift 2 ;;
    --base-dir)
      BASE_DIR="$2"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "[ERR] unknown arg: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$BINARY_GZ" || -z "$SUB_URL" ]]; then
  usage
  exit 1
fi

if [[ ! -f "$BINARY_GZ" ]]; then
  echo "[ERR] binary gz not found: $BINARY_GZ"
  exit 1
fi

for cmd in curl gunzip; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERR] required command not found: $cmd"
    exit 1
  fi
done

mkdir -p "$HOME/.local/bin" "$BASE_DIR"
cp -f "$BINARY_GZ" "$HOME/.local/bin/mihomo.gz"
gunzip -f "$HOME/.local/bin/mihomo.gz"

if [[ -f "$HOME/.local/bin/mihomo" && ! -f "$HOME/.local/bin/mihomo-core" ]]; then
  mv -f "$HOME/.local/bin/mihomo" "$HOME/.local/bin/mihomo-core"
fi

if [[ -f "$HOME/.local/bin/mihomo-linux-amd64-v1.19.20" ]]; then
  mv -f "$HOME/.local/bin/mihomo-linux-amd64-v1.19.20" "$HOME/.local/bin/mihomo-core"
fi

chmod +x "$HOME/.local/bin/mihomo-core"

curl --fail --retry 3 --retry-delay 2 --connect-timeout 10 -L "$SUB_URL" -o "$BASE_DIR/subscription.txt"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/generate_min_config.sh" "$BASE_DIR/subscription.txt" "$BASE_DIR/config-min.yaml"

cp -f "$SCRIPT_DIR/mihomo" "$HOME/.local/bin/mihomo"
chmod +x "$HOME/.local/bin/mihomo"

if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo '[INFO] add this to ~/.bashrc:'
  echo 'export PATH="$HOME/.local/bin:$PATH"'
fi

echo "[OK] install complete"
"$HOME/.local/bin/mihomo" --version
