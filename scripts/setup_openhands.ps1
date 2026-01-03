Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path ".").Path
$targetRoot = Join-Path $repoRoot "tools\openhands"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is required to install OpenHands."
}

if (-not (Test-Path $targetRoot)) {
  Write-Host "[OpenHands] Cloning into $targetRoot"
  git clone https://github.com/OpenHands/OpenHands.git $targetRoot
} else {
  Write-Host "[OpenHands] Updating existing repo at $targetRoot"
  Push-Location $targetRoot
  git fetch --all --prune
  git pull --ff-only
  Pop-Location
}

$composePath = Join-Path $targetRoot "docker-compose.yml"
if (-not (Test-Path $composePath)) {
  throw "OpenHands docker-compose.yml not found at $composePath"
}

Write-Host ""
Write-Host "[OpenHands] Ready."
Write-Host "Run:"
Write-Host "  cd $targetRoot"
Write-Host "  docker compose up --build"
