#!/bin/bash
# Command Coverage Test

COMMANDS_DIR=".YBIS_Dev/Veriler/commands"
FAILED=()

echo "Testing all YBIS commands..."

for cmd in "$COMMANDS_DIR"/*.md; do
    if [ -f "$cmd" ]; then
        cmd_name=$(basename "$cmd" .md)
        echo "Testing: $cmd_name"

        # Check required sections
        if ! grep -q "## What This Command Does" "$cmd"; then
            FAILED+=("$cmd_name: Missing 'What This Command Does'")
        fi

        if ! grep -q "## Steps" "$cmd"; then
            FAILED+=("$cmd_name: Missing 'Steps'")
        fi

        if ! grep -q "## Purpose" "$cmd"; then
            FAILED+=("$cmd_name: Missing 'Purpose'")
        fi

        echo "✅ $cmd_name: Structure OK"
    fi
done

if [ ${#FAILED[@]} -gt 0 ]; then
    echo "❌ Tests failed:"
    printf '%s\n' "${FAILED[@]}"
    exit 1
else
    echo "✅ All commands have required structure"
fi
