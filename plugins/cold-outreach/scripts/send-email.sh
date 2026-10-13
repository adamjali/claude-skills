#!/bin/bash
# Send a cold outreach email via the Resend API.
# Usage: ./send-email.sh <from> <subject> <to-email> <html-body> <text-body>
# Requires RESEND_API_KEY (free key at https://resend.com). Nothing is hardcoded —
# the from-address and subject come from references/config.md via the caller.

FROM="$1"
SUBJECT="$2"
TO_EMAIL="$3"
HTML_BODY="$4"
TEXT_BODY="$5"

if [ -z "$FROM" ] || [ -z "$SUBJECT" ] || [ -z "$TO_EMAIL" ] || [ -z "$HTML_BODY" ] || [ -z "$TEXT_BODY" ]; then
  echo "Usage: $0 <from> <subject> <to-email> <html-body> <text-body>"
  exit 1
fi

RESEND_API_KEY="${RESEND_API_KEY:?Set RESEND_API_KEY first (get a free key at https://resend.com)}"

curl -s -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"from\": $(echo "$FROM" | jq -Rs .),
    \"to\": \"$TO_EMAIL\",
    \"subject\": $(echo "$SUBJECT" | jq -Rs .),
    \"html\": $(echo "$HTML_BODY" | jq -Rs .),
    \"text\": $(echo "$TEXT_BODY" | jq -Rs .)
  }"
