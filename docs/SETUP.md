# YBIS_Dev Tier 1 - Setup Guide

**Quick setup for MCP server integration with Cursor**

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Python Environment (2 min)

```bash
# Navigate to .YBIS_Dev
cd C:\Projeler\YBIS\.YBIS_Dev

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Or if using PowerShell
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastmcp-0.2.0 gitignore-parser-0.1.11 ...
```

---

### Step 2: Configure Environment (1 min)

```bash
# Copy example env file
copy .env.example .env

# Edit .env (optional - defaults work fine)
# PROJECT_ROOT=C:\Projeler\YBIS  <- Already correct
```

---

### Step 3: Test Components (1 min)

```bash
# Run test script
python test_tier1.py
```

**Expected output:**
```
YBIS_Dev Tier 1 - Component Tests
============================================================
Testing ProjectScanner...
✓ All tests passed!
```

If tests fail, check:
- Python version (need 3.11+): `python --version`
- Dependencies installed: `pip list`

---

### Step 4: Start MCP Server (1 min)

```bash
# Start the server
python Agentic\server.py
```

**Expected output:**
```
[LAUNCH] YBIS_Dev MCP Server - Tier 1
📂 Project: C:\Projeler\YBIS
[DOC] Logs: C:\Projeler\YBIS\.YBIS_Dev\logs\session_2025-12-14_21-45-00.log

⚡ Server running. Use @YBIS_Dev in Cursor to interact.
```

**Keep this terminal open!** Server must run while using Cursor.

---

## [TARGET] Cursor Integration

### Method 1: Cursor Settings (Recommended)

1. Open Cursor
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Search: "MCP: Edit Config"
4. Add this to the JSON:

```json
{
  "mcpServers": {
    "YBIS_Dev": {
      "command": "python",
      "args": [
        "C:\\Projeler\\YBIS\\.YBIS_Dev\\Agentic\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Projeler\\YBIS\\.YBIS_Dev"
      }
    }
  }
}
```

5. Save and restart Cursor

---

### Method 2: Manual Start (Alternative)

If Cursor doesn't auto-start the server:

1. Keep server running in terminal (Step 4)
2. In Cursor, use `@YBIS_Dev` commands

---

## [TEST] Test in Cursor

Once Cursor is configured, try these commands:

```
Test 1 - Basic info:
@YBIS_Dev get_ybis_dev_info

Test 2 - Project structure:
@YBIS_Dev list_project_structure

Test 3 - Read a file:
@YBIS_Dev read_files ["README.md"]

Test 4 - Mobile app structure:
@YBIS_Dev list_project_structure apps/mobile

Test 5 - Log something:
@YBIS_Dev append_log "Testing YBIS_Dev for the first time"
```

**Expected:** Each command returns relevant data

---

## [SEARCH] Troubleshooting

### Server won't start

**Error:** `ModuleNotFoundError: No module named 'fastmcp'`
**Fix:**
```bash
pip install -r requirements.txt
```

---

**Error:** `ImportError: cannot import name 'ProjectScanner'`
**Fix:** Make sure you're in `.YBIS_Dev` folder:
```bash
cd C:\Projeler\YBIS\.YBIS_Dev
python Agentic\server.py
```

---

### Cursor can't find @YBIS_Dev

1. Check server is running (terminal should show "Server running")
2. Verify MCP config path is correct (no typos)
3. Restart Cursor completely
4. Check Cursor MCP logs: `Ctrl+Shift+P` -> "MCP: Show Logs"

---

### Tools return errors

**Error:** `Error: Path 'apps/mobile' not found`
**Fix:** Use relative paths from project root:
```
✓ apps/mobile
✗ C:\Projeler\YBIS\apps\mobile
✗ /apps/mobile
```

---

**Error:** `File too large (10.5MB > 5MB)`
**Fix:** Edit `.env`:
```
MAX_FILE_SIZE_MB=10
```
Then restart server.

---

## 📂 File Structure (After Setup)

```
.YBIS_Dev/
├── .venv/                    <- Python virtual environment
├── .env                      <- Your config (created from .env.example)
├── logs/                     <- Session logs (auto-created)
│   └── session_*.log
├── Agentic/
│   ├── server.py            <- Main MCP server
│   └── utils.py             <- Scanner & Logger
├── requirements.txt
├── test_tier1.py
└── SETUP.md                 <- You are here
```

---

## 🎓 Usage Examples

### Example 1: Analyze Mobile App

```
User: "@YBIS_Dev show me the structure of the mobile app"

YBIS_Dev calls: list_project_structure("apps/mobile", max_depth=3)

Returns: ASCII tree of apps/mobile/
```

---

### Example 2: Read Multiple Config Files

```
User: "@YBIS_Dev read all package.json files"

YBIS_Dev calls: read_files([
  "package.json",
  "apps/mobile/package.json",
  "apps/backend/package.json"
])

Returns: All package.json contents with line numbers
```

---

### Example 3: Track Your Session

```
User: "@YBIS_Dev log that I'm starting to refactor the auth system"

YBIS_Dev calls: append_log("Starting auth system refactor")

Later:
User: "@YBIS_Dev what did I log earlier?"

YBIS_Dev calls: get_recent_logs(20)
```

---

## [LAUNCH] Next Steps

After Tier 1 is working:

1. **Use it!** Practice with real YBIS queries
2. **Give feedback:** What works? What's missing?
3. **Tool calling bug:** Finish that first
4. **Then:** Move to Tier 2 (LangGraph loop)

---

## [DOC] Logs Location

Session logs are saved to:
```
.YBIS_Dev/logs/session_YYYY-MM-DD_HH-MM-SS.log
```

Each server start creates a new log file.

---

## 🛑 Stopping the Server

**To stop:**
1. Go to terminal running server
2. Press `Ctrl+C`
3. Server shuts down gracefully

**Note:** Cursor will lose @YBIS_Dev until you restart server

---

## [OK] Success Criteria

Tier 1 is working if:
- [ ] Server starts without errors
- [ ] `@YBIS_Dev get_ybis_dev_info` returns system info
- [ ] Can read project structure
- [ ] Can read files with line numbers
- [ ] Logs are being created

---

**Setup Date:** 2025-12-14
**Status:** Ready to use
**Next:** Start server and test in Cursor!
