#!/bin/bash
# YBIS Autonomous Factory Runbook (v5.0 - Steward OroYstein)
# Usage: ./examples/RUNBOOK.sh [task_description]

# 1. Environment Setup
export PYTHONUTF8=1
export YBIS_USE_CREWAI=true
export YBIS_USE_POETIQ=true
export YBIS_USE_WORKTREES=true

# 2. Activate Virtual Environment (if exists)
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# 3. Mode Selection
if [ -z "$1" ]; then
    echo "Starting YBIS in Autonomous Loop Mode..."
    echo "Press Ctrl+C to stop."
    python src/orchestrator/runner.py --loop
else
    echo "Executing Single Task..."
    python src/orchestrator/runner.py --task "$1"
fi
