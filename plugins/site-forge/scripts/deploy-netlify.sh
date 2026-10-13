#!/usr/bin/env bash
# Deploy a static site folder to Netlify (free), enabling Forms if a form exists.
# Usage: deploy-netlify.sh <dir> <site-name> [account-slug]
#   <dir>          folder containing index.html (e.g. ./site)
#   <site-name>    desired subdomain → <site-name>.netlify.app
#   [account-slug] Netlify team slug (optional; omit to use the default team)
#
# Idempotent: reuses the site if <site-name> already exists. Login is interactive
# the first time — if not logged in, the script stops and asks the user to run
# `netlify login` themselves (browser auth can't be scripted here).
set -euo pipefail

DIR="${1:?usage: deploy-netlify.sh <dir> <site-name> [account-slug]}"
NAME="${2:?usage: deploy-netlify.sh <dir> <site-name> [account-slug]}"
ACCOUNT="${3:-}"

# 1. Ensure the CLI (only installed at deploy time).
if ! command -v netlify >/dev/null 2>&1; then
  echo "Installing netlify-cli..."
  npm i -g netlify-cli
fi

# 2. Require an authenticated session.
if ! netlify status >/dev/null 2>&1; then
  echo "Not logged in to Netlify. Please run:  netlify login" >&2
  echo "(interactive browser auth — then re-run this script)" >&2
  exit 1
fi

# 3. Create the site (reuse if the name is taken by this account).
if [ -n "$ACCOUNT" ]; then
  netlify sites:create --name "$NAME" --account-slug "$ACCOUNT" 2>/dev/null \
    || echo "Site '$NAME' exists or name taken — continuing with existing."
else
  netlify sites:create --name "$NAME" 2>/dev/null \
    || echo "Site '$NAME' exists or name taken — continuing with existing."
fi

# 4. First production deploy.
netlify deploy --prod --dir "$DIR" --site "$NAME"

# 5. If the site has an HTML form, enable form detection and redeploy.
if grep -riqE 'data-netlify="true"|netlify[[:space:]]+name=|<form[^>]*netlify' "$DIR" 2>/dev/null; then
  SITE_ID="$(netlify api getSite --data "{\"site_id\":\"$NAME\"}" 2>/dev/null \
    | grep -oE '"id"[: ]*"[^"]+"' | head -1 | grep -oE '[0-9a-f-]{36}')" || true
  if [ -n "${SITE_ID:-}" ]; then
    echo "HTML form detected — enabling Netlify Forms..."
    netlify api updateSite --data \
      "{\"site_id\":\"$SITE_ID\",\"processing_settings\":{\"html\":{\"ignore_html_forms\":false}}}" >/dev/null
    netlify deploy --prod --dir "$DIR" --site "$NAME"   # redeploy so the form registers
    echo "Form enabled. Add an email notification with createHookBySiteId (see deploy.md)."
  else
    echo "Could not resolve site id; enable forms manually (see deploy.md)."
  fi
fi

echo "Done → https://${NAME}.netlify.app"
