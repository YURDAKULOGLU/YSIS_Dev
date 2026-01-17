#!/bin/bash
# YBIS Bootstrap Script - One-command setup
# Usage: ./scripts/bootstrap.sh

set -e  # Exit on error

echo "🚀 YBIS Bootstrap - Setting up the factory..."

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.11+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate || . .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
if [ -f "pyproject.toml" ]; then
    pip install -e ".[dev]" --quiet
    echo "✅ Dependencies installed from pyproject.toml"
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo "✅ Dependencies installed from requirements.txt"
else
    echo "⚠️  Warning: No pyproject.toml or requirements.txt found"
fi

# Initialize database
echo "🗄️  Initializing database..."
db_path="platform_data/control_plane.db"
db_dir=$(dirname "$db_path")
mkdir -p "$db_dir"

# Run database initialization if script exists
if [ -f "scripts/init_db.py" ]; then
    python scripts/init_db.py
    echo "✅ Database initialized"
else
    echo "⚠️  Warning: Database initialization script not found. Database will be created on first run."
fi

# Create workspace directories
echo "📁 Creating workspace directories..."
mkdir -p workspaces/active
mkdir -p workspaces/archive
mkdir -p platform_data/knowledge
echo "✅ Workspace directories created"

# Verify installation
echo "🔍 Verifying installation..."
if python -c "import ybis" 2>/dev/null; then
    echo "✅ YBIS package imported successfully"
else
    echo "⚠️  Warning: YBIS package import failed. Check installation."
fi

# Check for required tools
echo "🛠️  Checking required tools..."
missing_tools=()

if ! command -v git &> /dev/null; then
    missing_tools+=("git")
fi

if [ ${#missing_tools[@]} -gt 0 ]; then
    echo "⚠️  Warning: Missing tools: ${missing_tools[*]}"
    echo "   Some features may not work without these tools."
else
    echo "✅ All required tools available"
fi

echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Read: docs/AGENTS.md"
echo "   2. Read: docs/AI_START_HERE.md"
echo "   3. Run a task: python scripts/ybis_run.py TASK-123"
echo "   4. Or run worker: python scripts/ybis_worker.py"
echo ""
echo "💡 Tip: Activate the virtual environment with:"
echo "   source .venv/bin/activate  # Linux/Mac"
echo "   .venv\\Scripts\\activate     # Windows"
echo ""

