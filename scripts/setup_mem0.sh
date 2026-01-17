#!/bin/bash
# Setup Mem0 - Clone to vendors/ directory

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDORS_DIR="$PROJECT_ROOT/vendors"
MEM0_DIR="$VENDORS_DIR/mem0"

echo "Setting up Mem0 in vendors/ directory..."

# Create vendors directory if it doesn't exist
mkdir -p "$VENDORS_DIR"

# Check if already cloned
if [ -d "$MEM0_DIR" ]; then
    echo "Mem0 already cloned at $MEM0_DIR"
    echo "Updating..."
    cd "$MEM0_DIR"
    git pull
else
    echo "Cloning Mem0 to $MEM0_DIR..."
    git clone https://github.com/mem0ai/mem0.git "$MEM0_DIR"
fi

echo "✅ Mem0 cloned successfully!"
echo ""
echo "To use Mem0:"
echo "  1. Local mode (self-hosted): No API key needed"
echo "  2. Cloud mode: Set MEM0_API_KEY environment variable"
echo ""
echo "Mem0 will be automatically detected from vendors/mem0"


