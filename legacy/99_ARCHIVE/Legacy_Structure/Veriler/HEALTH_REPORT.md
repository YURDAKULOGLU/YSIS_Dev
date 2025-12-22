# YBIS Code Health Report
**Date:** 2025-12-16 17:31:54
**Target:** `C:\Projeler\YBIS\.YBIS_Dev`

## 1. Cyclomatic Complexity (Radon)
> Goal: Average Complexity < 5 (A). Blocks > 10 (B) allow. Blocks > 20 (C) fail.

```text
C:\Projeler\YBIS\.YBIS_Dev\scripts\code_health.py
    F 55:0 generate_report - A (3)
    F 13:0 run_command - A (2)
    F 22:0 scan_complexity - A (1)
    F 33:0 scan_lint - A (1)
C:\Projeler\YBIS\.YBIS_Dev\scripts\context_analysis.py
    F 4:0 analyze_rag_availability - A (1)

5 blocks (classes, functions, methods) analyzed.
Average complexity: A (1.6)
```

## 2. Lint Issues (Flake8)
> Goal: 0 Errors.

```text
0
```

## 3. Action Plan
- [ ] Fix High Complexity Blocks.
- [ ] Resolve Lint Errors.
