#!/bin/bash
# generate-skill.sh — scaffolds a new skill directory from chosen template + intake answers.
#
# Usage:
#   bash generate-skill.sh <skill-name> <template> [--with-references] [--with-scripts] [--state-location DIR]
#
# Templates: 01-stateless | 02-stateful-simple | 03-stateful-checkpointed |
#            04-stateful-multi-actor | 05-slash-command-router | 06-information-display |
#            07-multi-phase-feature
#
# After scaffolding, /skill-maker still does the intelligent SKILL.md content generation —
# this script just creates the directory + empty stubs.

set -e

NAME=$1
TEMPLATE=$2
SKILL_DIR=~/.claude/skills/$NAME

if [ -z "$NAME" ] || [ -z "$TEMPLATE" ]; then
  echo "Usage: $0 <skill-name> <template>"
  echo "Templates: 01-stateless | 02-stateful-simple | 03-stateful-checkpointed |"
  echo "           04-stateful-multi-actor | 05-slash-command-router | 06-information-display |"
  echo "           07-multi-phase-feature"
  exit 1
fi

if [ -e "$SKILL_DIR" ]; then
  echo "ERROR: $SKILL_DIR already exists. Pick a different name or rm -rf first."
  exit 1
fi

# Slash-command form is single file — different scaffolding
if [ "$TEMPLATE" = "05-slash-command-router" ]; then
  echo "WARN: For slash-command-router, write directly to ~/.claude/commands/$NAME.md, not skills dir."
  echo "Skipping skill dir scaffolding."
  exit 0
fi

mkdir -p "$SKILL_DIR"

# Stateless skills: just SKILL.md
if [ "$TEMPLATE" = "01-stateless" ]; then
  touch "$SKILL_DIR/SKILL.md"
  echo "Created $SKILL_DIR/SKILL.md (fill in via /skill-maker)"
  exit 0
fi

# Stateful skills: SKILL.md + state file + maybe references/ + scripts/
touch "$SKILL_DIR/SKILL.md"

if [ "$TEMPLATE" = "02-stateful-simple" ]; then
  touch "$SKILL_DIR/history.md"
elif [ "$TEMPLATE" = "03-stateful-checkpointed" ] || [ "$TEMPLATE" = "04-stateful-multi-actor" ]; then
  touch "$SKILL_DIR/${NAME}-history.md"
elif [ "$TEMPLATE" = "06-information-display" ]; then
  : # info skills are stateless
elif [ "$TEMPLATE" = "07-multi-phase-feature" ]; then
  : # state lives in .planning/, not skill dir
fi

# Optional subdirs based on flags
for arg in "$@"; do
  case "$arg" in
    --with-references) mkdir -p "$SKILL_DIR/references" ;;
    --with-scripts) mkdir -p "$SKILL_DIR/scripts" ;;
    --with-templates) mkdir -p "$SKILL_DIR/templates" ;;
    --with-state) mkdir -p "$SKILL_DIR/state" ;;
  esac
done

echo "Scaffolded $SKILL_DIR/"
ls -la "$SKILL_DIR/"
