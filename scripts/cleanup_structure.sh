#!/bin/bash

# Define dry-run flag
DRY_RUN=false

# Check for dry-run argument
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
fi

# Function to move files safely and idempotently
move_file() {
    local src="$1"
    local dest="$2"

    if [ -e "$src" ]; then
        if $DRY_RUN; then
            echo "Dry-run: Moving '$src' to '$dest'"
        else
            mkdir -p "$(dirname "$dest")"
            mv "$src" "$dest"
            echo "Moved '$src' to '$dest'"
        fi
    else
        echo "'$src' does not exist, skipping."
    fi
}

# Move files to proper locations
move_file "brain_debug.txt" ".YBIS_Dev/logs/brain_debug.txt"
move_file "meta_optimization_log.md" ".YBIS_Dev/docs/meta_optimization_log.md"
move_file "error.json" ".YBIS_Dev/logs/error.json"
move_file "error_plan.json" ".YBIS_Dev/logs/error_plan.json"
move_file "execution_log.md" ".YBIS_Dev/logs/execution_log.md"

# Add more moves as necessary
