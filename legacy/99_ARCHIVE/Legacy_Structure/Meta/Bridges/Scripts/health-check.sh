#!/bin/bash

echo "--- 🏥 YBIS System Health Check ---"

# 1. Check Dependencies
echo "📦 Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules missing! Running pnpm install..."
    pnpm install
else
    echo "✅ Dependencies present"
fi

# 2. TypeScript Check
echo "📘 Checking TypeScript..."
# Check if tsc is available
if ! command -v npx &> /dev/null; then
    echo "❌ npx could not be found"
    exit 1
fi

npx tsc --noEmit
if [ $? -eq 0 ]; then
    echo "✅ TypeScript: OK"
else
    echo "❌ TypeScript: ERRORS FOUND"
fi

# 3. Lint Check
echo "🧹 Checking Lint..."
pnpm lint --quiet
if [ $? -eq 0 ]; then
    echo "✅ Lint: OK"
else
    echo "⚠️ Lint: WARNINGS FOUND (Check output)"
fi

echo "--- 🏁 Health Check Complete ---"
