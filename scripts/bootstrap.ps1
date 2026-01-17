# YBIS Bootstrap Script (PowerShell) - One-command setup
# Usage: .\scripts\bootstrap.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 YBIS Bootstrap - Setting up the factory..." -ForegroundColor Cyan

# Check Python version
Write-Host "📋 Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1 | Out-String
    $pythonVersion = $pythonVersion.Trim()
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Python 3.11+
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
        Write-Host "❌ Error: Python 3.11+ required. Found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
if (Test-Path "pyproject.toml") {
    pip install -e ".[dev]" --quiet
    Write-Host "✅ Dependencies installed from pyproject.toml" -ForegroundColor Green
} elseif (Test-Path "requirements.txt") {
    pip install -r requirements.txt --quiet
    Write-Host "✅ Dependencies installed from requirements.txt" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: No pyproject.toml or requirements.txt found" -ForegroundColor Yellow
}

# Initialize database
Write-Host "🗄️  Initializing database..." -ForegroundColor Yellow
$dbPath = "platform_data\control_plane.db"
$dbDir = Split-Path -Parent $dbPath
if (-not (Test-Path $dbDir)) {
    New-Item -ItemType Directory -Path $dbDir -Force | Out-Null
}

# Run database initialization if script exists
if (Test-Path "scripts\init_db.py") {
    python scripts\init_db.py
    Write-Host "✅ Database initialized" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: Database initialization script not found. Database will be created on first run." -ForegroundColor Yellow
}

# Create workspace directories
Write-Host "📁 Creating workspace directories..." -ForegroundColor Yellow
@("workspaces\active", "workspaces\archive", "platform_data\knowledge") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}
Write-Host "✅ Workspace directories created" -ForegroundColor Green

# Verify installation
Write-Host "🔍 Verifying installation..." -ForegroundColor Yellow
try {
    python -c "import ybis" 2>&1 | Out-Null
    Write-Host "✅ YBIS package imported successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: YBIS package import failed. Check installation." -ForegroundColor Yellow
}

# Check for required tools
Write-Host "🛠️  Checking required tools..." -ForegroundColor Yellow
$missingTools = @()

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    $missingTools += "git"
}

if ($missingTools.Count -gt 0) {
    Write-Host "⚠️  Warning: Missing tools: $($missingTools -join ', ')" -ForegroundColor Yellow
    Write-Host "   Some features may not work without these tools." -ForegroundColor Yellow
} else {
    Write-Host "✅ All required tools available" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Bootstrap complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📖 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Read: docs\AGENTS.md"
Write-Host "   2. Read: docs\AI_START_HERE.md"
Write-Host "   3. Run a task: python scripts\ybis_run.py TASK-123"
Write-Host "   4. Or run worker: python scripts\ybis_worker.py"
Write-Host ""
Write-Host "💡 Tip: Activate the virtual environment with:" -ForegroundColor Cyan
Write-Host "   .\.venv\Scripts\Activate.ps1"
Write-Host ""

