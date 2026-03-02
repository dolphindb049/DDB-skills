#!/usr/bin/env bash
set -euo pipefail

SUB_FILE="${1:-$HOME/clash/subscription.txt}"
OUT_FILE="${2:-$HOME/clash/config-min.yaml}"
GROUP_NAME="${3:-🚀 节点选择}"

if [ ! -f "$SUB_FILE" ]; then
  echo "[ERR] subscription file not found: $SUB_FILE"
  exit 1
fi

mkdir -p "$(dirname "$OUT_FILE")"

awk '
BEGIN { stop=0; modeSeen=0 }
/^rules:[[:space:]]*$/ { stop=1; next }
{
  if (stop==0) {
    if ($0 ~ /^mode:[[:space:]]*/) {
      print "mode: global"
      modeSeen=1
      next
    }
    print
  }
}
END {
  if (modeSeen==0) {
    print "mode: global"
  }
}
' "$SUB_FILE" > "$OUT_FILE"
printf "\nrules:\n  - MATCH,%s\n" "$GROUP_NAME" >> "$OUT_FILE"

echo "[OK] generated minimal config: $OUT_FILE"
