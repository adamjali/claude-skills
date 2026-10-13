#!/bin/bash
# validate-skill.sh — sanity checks for a generated skill against the house style guide.
#
# Usage: bash validate-skill.sh <skill-name>
#
# Checks:
#  - Frontmatter description ≤ 1,536 chars (combined with when_to_use)
#  - SKILL.md size warning at >500 lines
#  - Required tags present per skill type
#  - References referenced in <context> actually exist
#  - Scripts referenced are executable
#
# Exit 0 = all pass. Exit 1 = blocking issues. Exit 2 = warnings only.

set +e

NAME=$1
SKILL_DIR=~/.claude/skills/$NAME

[ -z "$NAME" ] && { echo "Usage: $0 <skill-name>"; exit 1; }
[ ! -d "$SKILL_DIR" ] && { echo "ERROR: $SKILL_DIR not found"; exit 1; }
[ ! -f "$SKILL_DIR/SKILL.md" ] && { echo "ERROR: SKILL.md missing"; exit 1; }

PASS=0; WARN=0; FAIL=0

# 1. Description char-count
DESC=$(awk '/^description:/,/^[a-z_-]+:/{if(/^[a-z_-]+:/&&!/^description:/)exit; print}' "$SKILL_DIR/SKILL.md" | sed 's/^description://')
WTU=$(awk '/^when_to_use:/,/^[a-z_-]+:/{if(/^[a-z_-]+:/&&!/^when_to_use:/)exit; print}' "$SKILL_DIR/SKILL.md" | sed 's/^when_to_use://')
COMBINED_LEN=$((${#DESC} + ${#WTU}))
if [ "$COMBINED_LEN" -gt 1536 ]; then
  echo "✗ description+when_to_use combined = $COMBINED_LEN chars (HARD CAP 1,536)"; FAIL=$((FAIL+1))
elif [ "$COMBINED_LEN" -gt 1300 ]; then
  echo "⚠ description+when_to_use combined = $COMBINED_LEN chars (close to 1,536 cap)"; WARN=$((WARN+1))
else
  echo "✓ description+when_to_use = $COMBINED_LEN chars"; PASS=$((PASS+1))
fi

# 2. Body size
LINES=$(wc -l < "$SKILL_DIR/SKILL.md" | tr -d ' ')
if [ "$LINES" -gt 700 ]; then
  echo "⚠ SKILL.md is $LINES lines (convention is <500; consider offloading to references/)"; WARN=$((WARN+1))
elif [ "$LINES" -gt 500 ]; then
  echo "⚠ SKILL.md is $LINES lines (soft cap is 500)"; WARN=$((WARN+1))
else
  echo "✓ SKILL.md size: $LINES lines"; PASS=$((PASS+1))
fi

# 3. Required tags (always)
for tag in "<objective>" "<process>" "<success_criteria>"; do
  if grep -q "$tag" "$SKILL_DIR/SKILL.md"; then
    echo "✓ has $tag"; PASS=$((PASS+1))
  else
    echo "⚠ missing $tag (canonical scaffold)"; WARN=$((WARN+1))
  fi
done

# 4. Conditional tags hint
if grep -q "checkpoint:" "$SKILL_DIR/SKILL.md" || grep -q "IN_PROGRESS" "$SKILL_DIR/SKILL.md"; then
  if ! grep -q "<recovery_protocol>" "$SKILL_DIR/SKILL.md"; then
    echo "⚠ uses checkpoint/IN_PROGRESS but missing <recovery_protocol>"; WARN=$((WARN+1))
  fi
fi

# 5. @-injected references actually exist
grep -oE '@\./[^ ]+' "$SKILL_DIR/SKILL.md" | while read ref; do
  rel="${ref#@}"
  full="$SKILL_DIR/$rel"
  if [ ! -e "$full" ]; then
    echo "✗ <context> references missing file: $rel"; FAIL=$((FAIL+1))
  else
    echo "✓ <context> reference exists: $rel"; PASS=$((PASS+1))
  fi
done

# 6. Scripts mentioned are executable
grep -oE 'bash scripts/[a-z_-]+\.sh' "$SKILL_DIR/SKILL.md" | while read sh; do
  rel="${sh#bash }"
  full="$SKILL_DIR/$rel"
  if [ ! -e "$full" ]; then
    echo "⚠ script referenced but missing: $rel"; WARN=$((WARN+1))
  elif [ ! -x "$full" ]; then
    echo "⚠ script exists but not executable: $rel"; WARN=$((WARN+1))
  fi
done

echo ""
echo "═══ Validation: $PASS passed, $WARN warnings, $FAIL failures ═══"

if [ "$FAIL" -gt 0 ]; then exit 1; fi
if [ "$WARN" -gt 0 ]; then exit 2; fi
exit 0
