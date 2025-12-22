#!/bin/bash

# TASK-New-206: Project Structure Cleanup
# Moves files and directories to match ARCHITECTURE_V2.md standards

DRY_RUN=false

# Check for dry-run argument
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
    echo "DRY RUN MODE - No changes will be made"
    echo "========================================"
fi

# Function to move files safely
move_file() {
    local src="$1"
    local dest="$2"

    if [ -e "$src" ]; then
        if $DRY_RUN; then
            echo "[DRY-RUN] Would move: '$src' -> '$dest'"
        else
            mkdir -p "$(dirname "$dest")"
            mv "$src" "$dest"
            echo "✓ Moved: '$src' -> '$dest'"
        fi
    else
        if $DRY_RUN; then
            echo "[SKIP] Not found: '$src'"
        fi
    fi
}

# Function to remove empty file
remove_file() {
    local file="$1"

    if [ -e "$file" ]; then
        if $DRY_RUN; then
            echo "[DRY-RUN] Would remove: '$file'"
        else
            rm "$file"
            echo "✓ Removed: '$file'"
        fi
    fi
}

echo ""
echo "Phase 1: Root Cleanup (Loose Files)"
echo "===================================="
move_file "brain_debug.txt" "logs/archive/brain_debug.txt"
move_file "error_plan.json" "logs/archive/error_plan.json"
move_file "meta_optimization_log.md" "logs/archive/meta_optimization_log.md"
move_file "Block 1" "logs/archive/Block_1"
remove_file "nul"

echo ""
echo "Phase 2: Aider Cache Cleanup"
echo "============================"
move_file ".aider.chat.history.md" "logs/aider_cache/.aider.chat.history.md"
move_file ".aider.input.history" "logs/aider_cache/.aider.input.history"

echo ""
echo "Phase 3: Directory Consolidation"
echo "================================="

# 3.1 Meta/ -> docs/governance/ (ALREADY DONE, check if remnants exist)
if [ -d "Meta" ]; then
    echo "Warning: Meta/ directory still exists (should be moved already)"
fi

# 3.2 specs/ -> docs/specs/
if [ -d "specs" ]; then
    if $DRY_RUN; then
        echo "[DRY-RUN] Would move: specs/* -> docs/specs/"
    else
        mkdir -p docs/specs/
        if [ "$(ls -A specs)" ]; then
            mv specs/* docs/specs/ 2>/dev/null || true
            rmdir specs 2>/dev/null || echo "Warning: Could not remove specs/ (not empty)"
            echo "✓ Moved: specs/ -> docs/specs/"
        else
            rmdir specs
            echo "✓ Removed empty: specs/"
        fi
    fi
fi

# 3.3 Workflows/ -> legacy/Workflows/
move_file "Workflows" "legacy/Workflows"

# 3.4 30_INFRASTRUCTURE/ -> legacy/
move_file "30_INFRASTRUCTURE" "legacy/30_INFRASTRUCTURE"

# 3.5 path/ -> DELETE
if [ -d "path" ]; then
    if $DRY_RUN; then
        echo "[DRY-RUN] Would delete: path/"
    else
        rm -rf path/
        echo "✓ Deleted: path/"
    fi
fi

# 3.6 .YBIS_Dev/ -> legacy/
move_file ".YBIS_Dev" "legacy/.YBIS_Dev"

echo ""
echo "Phase 4: Archive Cleanup (Sandbox Dirs)"
echo "======================================="
move_file ".sandbox_hybrid__archived_2025_12_20" "legacy/sandbox_archives/.sandbox_hybrid__archived_2025_12_20"
move_file ".sandbox_hybrid__archived_2025_12_20_05_46_39" "legacy/sandbox_archives/.sandbox_hybrid__archived_2025_12_20_05_46_39"

echo ""
if $DRY_RUN; then
    echo "========================================"
    echo "DRY RUN COMPLETE - No changes were made"
    echo "Run without --dry-run to execute cleanup"
else
    echo "========================================"
    echo "CLEANUP COMPLETE!"
    echo ""
    echo "Next steps:"
    echo "1. Review moved files in logs/ and legacy/"
    echo "2. Run: python -m pytest tests/ -v"
    echo "3. Verify system still works"
fi
