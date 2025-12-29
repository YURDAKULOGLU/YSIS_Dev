#!/bin/bash
# Example RUNBOOK.sh template
# Self-verifying, executable task replay script
# Exit codes: 1=file operation failed, 2=commit failed, 3=verification failed

set -e  # Exit on first error

# Step 1: Modify files
git add docs/file.md || exit 1
git add scripts/script.py || exit 1

# Step 2: Commit changes
git commit -m "TASK-ID: Description of changes

Detailed commit message body.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
" || exit 2

# Step 3: Verify artifacts (adjust tier as needed)
python scripts/protocol_check.py --task-id TASK-ID --tier auto || exit 3

# Success
echo "[OK] Task replay completed successfully"
exit 0
