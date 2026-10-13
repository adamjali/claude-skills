#!/usr/bin/env bash
# scan-disk.sh — read-only disk inventory.
# Output: JSON to stdout. Never modifies disk.
#
# Usage: bash scan-disk.sh > /tmp/disk-cleanup-findings.json
#
# Captures: df, du cascading from $HOME + Library, APFS snapshots, swap state,
# conditional Xcode dev paths if present.

set -eu
# pipefail intentionally omitted — du/grep/sort can have OK partial failures
# (permission denied on some paths, no matches in grep) that we want to tolerate.

# Convert `du -sh` output (tab-separated: size\tpath) to a JSON array of
# {size, path} objects. Handles paths with spaces (uses -F'\t') and escapes
# backslashes + double-quotes correctly so the result is always valid JSON.
du_to_json_array() {
  awk -F'\t' '
    BEGIN { printf "[" }
    {
      size = $1
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", size)
      path = $2
      gsub(/\\/, "\\\\", path)
      gsub(/"/, "\\\"", path)
      printf "%s{\"size\":\"%s\",\"path\":\"%s\"}", (NR>1?",":""), size, path
    }
    END { printf "]" }
  '
}

# df baseline (root volume)
df_line=$(df -h / | tail -1)
df_used=$(echo "$df_line" | awk '{print $3}')
df_avail=$(echo "$df_line" | awk '{print $4}')
df_pct=$(echo "$df_line" | awk '{print $5}')

# Top-level home consumers (visible vs hidden)
home_visible=$(du -sh "$HOME"/[A-Za-z]* 2>/dev/null | sort -rh | head -20 | du_to_json_array)
home_hidden=$(du -sh "$HOME"/.[a-zA-Z]* 2>/dev/null | sort -rh | head -15 | du_to_json_array)

# Library breakdown
library=$(du -sh "$HOME/Library"/* 2>/dev/null | sort -rh | head -15 | du_to_json_array)
library_caches=$(du -sh "$HOME/Library/Caches"/* 2>/dev/null | sort -rh | head -20 | du_to_json_array)
library_appsupport=$(du -sh "$HOME/Library/Application Support"/* 2>/dev/null | sort -rh | head -15 | du_to_json_array)

# APFS snapshots (size info requires sudo — list count only here).
# Use `wc -l` instead of `grep -c` so an empty match returns 0 cleanly without
# triggering grep's exit-1-on-no-match (which would double-print under `|| echo 0`).
snapshots=$(tmutil listlocalsnapshots / 2>/dev/null | grep 'com.apple.TimeMachine' | wc -l | tr -d ' ')
[[ -z "$snapshots" ]] && snapshots=0 || true

# Swap state — strip newline AND trailing whitespace from the regex match
swap_line=$(sysctl vm.swapusage 2>/dev/null | sed 's/.*total = //; s/ used.*//' | tr -d '\n' | sed 's/[[:space:]]*$//')

# Conditional Xcode paths — empty string if dir absent
# Helper: extract du size column, trim leading/trailing whitespace
du_size_only() { awk -F'\t' '{gsub(/^[[:space:]]+|[[:space:]]+$/, "", $1); print $1}'; }

xcode_dd=""
if [[ -d "$HOME/Library/Developer/Xcode/DerivedData" ]]; then
  xcode_dd=$(du -sh "$HOME/Library/Developer/Xcode/DerivedData" 2>/dev/null | du_size_only)
fi

xcode_sim=""
if [[ -d "$HOME/Library/Developer/CoreSimulator/Devices" ]]; then
  xcode_sim=$(du -sh "$HOME/Library/Developer/CoreSimulator/Devices" 2>/dev/null | du_size_only)
fi

xcode_devsupport=""
if [[ -d "$HOME/Library/Developer/Xcode/iOS DeviceSupport" ]]; then
  xcode_devsupport=$(du -sh "$HOME/Library/Developer/Xcode/iOS DeviceSupport" 2>/dev/null | du_size_only)
fi

trash_size=$(du -sh "$HOME/.Trash" 2>/dev/null | du_size_only || true)
[[ -z "$trash_size" ]] && trash_size="0B" || true

# Final assembly. The du_to_json_array helper outputs full arrays with brackets;
# the scalar fields are simple strings/numbers we can safely interpolate
# (no user-controlled content reaches them).
cat <<EOF
{
  "df": {"used": "$df_used", "avail": "$df_avail", "capacity_pct": "$df_pct"},
  "swap_total": "$swap_line",
  "trash_size": "$trash_size",
  "snapshots_count": $snapshots,
  "home_visible": $home_visible,
  "home_hidden": $home_hidden,
  "library": $library,
  "library_caches": $library_caches,
  "library_appsupport": $library_appsupport,
  "xcode": {
    "DerivedData": "$xcode_dd",
    "CoreSimulator": "$xcode_sim",
    "iOS DeviceSupport": "$xcode_devsupport"
  }
}
EOF
