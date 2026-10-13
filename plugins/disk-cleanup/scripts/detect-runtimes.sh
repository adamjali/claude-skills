#!/usr/bin/env bash
# detect-runtimes.sh — scan ~/projects-style dirs for runtime version markers.
#
# Output: JSON listing Node/Python versions actually referenced by config files.
# Used to decide which nvm/pyenv versions are safe to delete.
#
# Usage: bash detect-runtimes.sh [search-root1] [search-root2] ...
# Defaults to $HOME (excluding common heavy/irrelevant dirs + iCloud).

set -eu
# pipefail intentionally omitted — find/grep can have OK partial failures
# (permission denied, no matches) that we want to tolerate per-root.

if [[ $# -gt 0 ]]; then
  roots=("$@")
else
  roots=("$HOME")
fi

# Convert a newline-separated list of strings on stdin to a JSON array.
# Escapes backslashes and double-quotes; skips empty lines.
strings_to_json_array() {
  awk '
    BEGIN { printf "[" }
    NF > 0 {
      val = $0
      gsub(/\\/, "\\\\", val)
      gsub(/"/, "\\\"", val)
      printf "%s\"%s\"", (count++ > 0 ? "," : ""), val
    }
    END { printf "]" }
  '
}

# Run find with the canonical exclusion set. Inline (not via eval) so paths
# containing spaces (like "Mobile Documents") are passed correctly to find.
do_find() {
  local root=$1
  shift
  find "$root" \
    -not -path '*/node_modules/*' \
    -not -path '*/.git/*' \
    -not -path '*/.npm/*' \
    -not -path '*/Library/*' \
    -not -path '*/Mobile Documents/*' \
    -not -path '*/.Trash/*' \
    -not -path '*/.cache/*' \
    "$@" 2>/dev/null
}

node_versions=$(
  for root in "${roots[@]}"; do
    # .nvmrc files (one version per file, one file per project)
    do_find "$root" -name '.nvmrc' \
      | while read -r f; do tr -d '[:space:]' < "$f" 2>/dev/null; echo; done
    # package.json engines.node (depth-limited; skip vendored deps)
    do_find "$root" -name 'package.json' -maxdepth 5 \
      | head -200 \
      | while read -r f; do
          grep -oE '"node"[[:space:]]*:[[:space:]]*"[^"]+"' "$f" 2>/dev/null \
            | sed 's/.*"\([^"]*\)"$/\1/'
        done
  done | grep -v '^$' | sort -u
)

python_versions=$(
  for root in "${roots[@]}"; do
    do_find "$root" -name '.python-version' \
      | while read -r f; do tr -d '[:space:]' < "$f" 2>/dev/null; echo; done
    do_find "$root" -name 'pyproject.toml' -maxdepth 5 \
      | head -200 \
      | while read -r f; do
          grep -oE 'requires-python[[:space:]]*=[[:space:]]*"[^"]+"' "$f" 2>/dev/null \
            | sed 's/.*"\([^"]*\)"$/\1/'
        done
  done | grep -v '^$' | sort -u
)

# Currently installed (from nvm + pyenv if available)
installed_node=""
if [[ -d "$HOME/.nvm/versions/node" ]]; then
  installed_node=$(ls "$HOME/.nvm/versions/node" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
fi

installed_python=""
if [[ -d "$HOME/.pyenv/versions" ]]; then
  installed_python=$(ls "$HOME/.pyenv/versions" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
fi

# Format output. The strings_to_json_array helper emits valid JSON arrays.
node_json=$(printf '%s\n' "$node_versions" | strings_to_json_array)
python_json=$(printf '%s\n' "$python_versions" | strings_to_json_array)

cat <<EOF
{
  "referenced_node": $node_json,
  "referenced_python": $python_json,
  "installed_node": "$installed_node",
  "installed_python": "$installed_python"
}
EOF
