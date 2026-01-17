# Setup Mem0 - Clone to vendors/ directory (PowerShell)

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$VENDORS_DIR = Join-Path $PROJECT_ROOT "vendors"
$MEM0_DIR = Join-Path $VENDORS_DIR "mem0"

Write-Host "Setting up Mem0 in vendors/ directory..."

# Create vendors directory if it doesn't exist
if (-not (Test-Path $VENDORS_DIR)) {
    New-Item -ItemType Directory -Path $VENDORS_DIR | Out-Null
}

# Check if already cloned
if (Test-Path $MEM0_DIR) {
    Write-Host "Mem0 already cloned at $MEM0_DIR"
    Write-Host "Updating..."
    Push-Location $MEM0_DIR
    git pull
    Pop-Location
} else {
    Write-Host "Cloning Mem0 to $MEM0_DIR..."
    git clone https://github.com/mem0ai/mem0.git $MEM0_DIR
}

Write-Host "✅ Mem0 cloned successfully!"
Write-Host ""
Write-Host "To use Mem0:"
Write-Host "  1. Local mode (self-hosted): No API key needed"
Write-Host "  2. Cloud mode: Set MEM0_API_KEY environment variable"
Write-Host ""
Write-Host "Mem0 will be automatically detected from vendors/mem0"


