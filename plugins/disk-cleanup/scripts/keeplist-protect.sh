#!/usr/bin/env bash
# keeplist-protect.sh — atomically nuke a directory's contents while preserving named keepers.
#
# Usage: bash keeplist-protect.sh <target-dir> <keeper1> [keeper2] [...]
#
# Mechanism: mv keepers to /tmp/dlkeep_<ts>/, find -delete the rest, mv keepers back.
# Keeper names are basenames relative to <target-dir>, not absolute paths.
#
# Exit codes: 0 success, 1 bad args, 2 target missing, 3 partial restore (manual review needed).

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <target-dir> [keeper1 keeper2 ...]" >&2
  exit 1
fi

target="$1"
shift
keepers=("$@")

if [[ ! -d "$target" ]]; then
  echo "target dir does not exist: $target" >&2
  exit 2
fi

stage="/tmp/dlkeep_$(date +%s)"
mkdir -p "$stage"

# Move keepers to stage (silently skip missing — caller may overspecify)
for k in "${keepers[@]}"; do
  if [[ -e "$target/$k" ]]; then
    mv "$target/$k" "$stage/" 2>/dev/null || true
  fi
done

# Nuke remaining contents (preserve target dir itself)
find "$target" -mindepth 1 -delete 2>&1 | tail -5 || true

# Restore keepers
restore_failed=0
for entry in "$stage"/*; do
  [[ -e "$entry" ]] || continue
  if ! mv "$entry" "$target/"; then
    echo "WARN: could not restore $entry to $target" >&2
    restore_failed=1
  fi
done

# Cleanup stage if empty
rmdir "$stage" 2>/dev/null || true

if [[ $restore_failed -eq 1 ]]; then
  echo "PARTIAL: some keepers may still be in $stage — manual review needed" >&2
  exit 3
fi

echo "OK: keepers preserved in $target"
