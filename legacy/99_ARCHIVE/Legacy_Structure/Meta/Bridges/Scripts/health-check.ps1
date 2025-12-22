Write-Host "--- 🏥 YBIS System Health Check ---" -ForegroundColor Cyan

# 1. Check Dependencies
Write-Host "📦 Checking dependencies..."
if (-not (Test-Path "node_modules")) {
    Write-Host "❌ node_modules missing! Running pnpm install..." -ForegroundColor Red
    pnpm install
} else {
    Write-Host "✅ Dependencies present" -ForegroundColor Green
}

# 2. TypeScript Check
Write-Host "📘 Checking TypeScript..."
try {
    npx tsc --noEmit
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ TypeScript: OK" -ForegroundColor Green
    } else {
        Write-Host "❌ TypeScript: ERRORS FOUND" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Failed to run tsc" -ForegroundColor Red
}

# 3. Lint Check
Write-Host "🧹 Checking Lint..."
try {
    pnpm lint --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Lint: OK" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Lint: WARNINGS FOUND" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Failed to run lint" -ForegroundColor Red
}

Write-Host "--- 🏁 Health Check Complete ---" -ForegroundColor Cyan
