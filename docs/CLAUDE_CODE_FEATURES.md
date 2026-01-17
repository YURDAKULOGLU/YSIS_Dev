# Claude Code Features Reference

> **Complete reference for Claude Code CLI capabilities within YBIS.**

---

## Overview

Claude Code is Anthropic's official CLI for Claude. It provides autonomous coding capabilities with built-in safety controls, tool access, and integration points.

---

## Core Concepts (Temel Kavramlar)

Claude Code'un 3 temel extension mekanizması vardır: **Commands**, **Skills**, ve **Hooks**.

### Commands vs Skills vs Hooks

| Özellik | Commands | Skills | Hooks |
|---------|----------|--------|-------|
| **Tetikleme** | Explicit (`/project:x`) | Implicit (pattern match) | Her tool call'da |
| **Kontrol** | User kontrol eder | Claude otomatik algılar | System intercept eder |
| **Amaç** | Workflow tanımlama | Akıllı davranış | Güvenlik/audit |
| **Timing** | İstendiğinde | Context'e göre | Her zaman |

### Custom Commands Nedir?

Custom Commands, proje-özel slash command'lar oluşturmanızı sağlar.

**Nasıl Çalışır:**
```
User: /project:deploy production
              ↓
Claude: .claude/commands/deploy.md dosyasını okur
              ↓
Claude: Dosyadaki talimatları system prompt olarak alır
              ↓
Claude: $ARGUMENTS = "production" ile çalışır
              ↓
Claude: Tanımlanan adımları uygular
```

**Use Cases:**
- Tekrarlayan görevleri standartlaştırma (deploy, test, review)
- Proje-özel workflow'lar (code generation, migration)
- Tool kısıtlamaları (sadece belirli tool'lara izin)
- Prompt engineering'i versiyon kontrollü dosyaya taşıma

**Örnek Senaryo:**
```bash
# Eskiden her seferinde:
"Şimdi deploy yap, önce testleri çalıştır, sonra build al,
staging'e deploy et, smoke test yap..."

# Şimdi:
/project:deploy staging
```

### Skills Nedir?

Skills, Claude'un conversation context'ine göre otomatik aktive olan yeteneklerdir.

**Nasıl Çalışır:**
```
User: "YBIS task T-123'ü çalıştır"
              ↓
Claude: Message'da "ybis task" pattern'ı algılar
              ↓
Claude: ybis-task-executor skill'ini bulur
              ↓
       ┌──────────────────────────────────┐
       │ auto_invoke: true  → Direkt çalış│
       │ auto_invoke: false → Öneri sun   │
       └──────────────────────────────────┘
              ↓
Claude: Skill talimatlarına göre çalışır
```

**Trigger Types:**
- **Pattern:** Regex ile message matching (`(?i)ybis\s+task`)
- **Keywords:** Belirli kelimeler geçtiğinde (`deploy`, `test`)
- **Files:** Belirli dosyalar context'te olduğunda (`*.md`, `Dockerfile`)
- **Context:** MCP server aktif, belirli dizinde olma, vs.

**Use Cases:**
- Domain-specific bilgi enjekte etme (YBIS task format'ı)
- Otomatik code review tetikleme (PR context'i algılama)
- Akıllı dosya handling (PDF algılayınca PDF skill aktif)

### Hooks Nedir?

Hooks, Claude'un her aksiyonunu intercept eden middleware script'leridir.

**Nasıl Çalışır:**
```
Claude: Edit tool'unu çağıracak (file: secrets.json)
              ↓
System: PreToolUse hook'u çalıştır
              ↓
Hook Script:
  stdin  → {"tool_name": "Edit", "tool_input": {"file_path": "secrets.json"}}
  logic  → "secrets.json korumalı dosya mı?" → EVET
  stdout → {"decision": "block", "reason": "Protected file"}
              ↓
       ┌─────────────────────────────────────┐
       │ decision: "allow"  → Tool çalışır   │
       │ decision: "block"  → Tool ÇALIŞMAZ  │
       └─────────────────────────────────────┘
              ↓
Claude: "Bu dosyayı düzenleyemiyorum: Protected file"
```

**4 Hook Tipi:**

| Hook | Trigger | Input | Yapabilecekleri |
|------|---------|-------|-----------------|
| **PreToolUse** | Tool çalışmadan önce | tool_name, tool_input | Block, modify input, log |
| **PostToolUse** | Tool çalıştıktan sonra | tool_name, tool_output, duration | Verify, metrics, alert |
| **Notification** | Bildirim gönderildiğinde | notification object | Route (Slack, Discord, email) |
| **Stop** | Session bittiğinde | context, session_info | Cleanup, final report, lease release |

**Use Cases:**
- **Güvenlik:** `.env`, `secrets.json` gibi dosyaları koruma
- **Governance:** Constitution'a aykırı değişiklikleri engelleme
- **Audit:** Her aksiyonu compliance için loglama
- **Rate Limiting:** API abuse'u önleme (50 Bash/dakika limit)
- **Verification:** Yazılan Python kodunun syntax check'i
- **Alerting:** Critical hatalarda Slack notification

**Hook Execution Flow:**
```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE SESSION                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User Request                                                │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────┐    ┌──────────────┐    ┌─────────┐             │
│  │ Claude  │───▶│ PreToolUse   │───▶│  Tool   │             │
│  │ Decides │    │ Hook         │    │ Execute │             │
│  └─────────┘    │ (can block)  │    └────┬────┘             │
│                 └──────────────┘         │                   │
│                                          ▼                   │
│                                   ┌──────────────┐           │
│                                   │ PostToolUse  │           │
│                                   │ Hook         │           │
│                                   │ (verify/log) │           │
│                                   └──────────────┘           │
│                                          │                   │
│                                          ▼                   │
│                                   ┌──────────────┐           │
│                                   │   Response   │           │
│                                   └──────────────┘           │
│                                                              │
│  ... session continues ...                                   │
│                                                              │
│  Session End                                                 │
│       │                                                      │
│       ▼                                                      │
│  ┌──────────────┐                                           │
│  │ Stop Hook    │                                           │
│  │ (cleanup)    │                                           │
│  └──────────────┘                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## CLI Flags (Başlatma Parametreleri)

Claude Code başlatılırken çeşitli flag'lerle davranışı özelleştirilebilir.

### Temel Kullanım

```bash
claude [flags] [prompt]
```

### Session Flags

| Flag | Açıklama |
|------|----------|
| `--resume`, `-r` | Son konuşmayı devam ettir |
| `--continue`, `-c` | En son session'dan devam et |
| `--print`, `-p` | Tek seferlik çalıştır, sonucu yazdır ve çık |

### Model Seçimi

| Flag | Açıklama |
|------|----------|
| `--model <model>` | Kullanılacak model (opus, sonnet, haiku) |
| `--model claude-opus-4-5-20251101` | Tam model ID |

### Headless Mode (Otomasyon)

Headless mode, Claude Code'u interaktif olmayan ortamlarda (CI/CD, scripts, automation) çalıştırmak için kullanılır.

```bash
# Headless mode - user input beklemez
claude --headless "Fix all TypeScript errors"

# Print mode ile birlikte - output al ve çık
claude --headless --print "What files are in src/"

# JSON output
claude --headless --output-format json "List all functions in main.py"
```

**Headless Mode Özellikleri:**
- User prompt beklemez
- Stdin'den input almaz
- Non-interactive terminal'lerde çalışır
- CI/CD pipeline'larında kullanılabilir
- Timeout ile birlikte kullanılabilir

```bash
# CI/CD örneği
claude --headless --timeout 300000 "Run tests and fix failures"
```

### Permission Flags

| Flag | Açıklama |
|------|----------|
| `--dangerously-skip-permissions` | TÜM izin kontrollerini atla (TEHLİKELİ) |
| `--allowedTools <tools>` | Sadece belirtilen tool'lara izin ver |
| `--disallowedTools <tools>` | Belirtilen tool'ları yasakla |

**⚠️ `--dangerously-skip-permissions` Hakkında:**

```bash
# TÜM izin kontrollerini atlar - DİKKATLİ KULLAN
claude --dangerously-skip-permissions "Delete all temp files"
```

**Ne Yapar:**
- Tool permission prompt'larını atlar
- File write/delete onayı istemez
- Bash command onayı istemez
- MCP tool onayı istemez

**Ne Zaman Kullanılır:**
- Güvenli, izole ortamlarda (Docker container)
- CI/CD pipeline'larında
- Automated testing'de
- Kontrollü script'lerde

**Ne Zaman KULLANILMAZ:**
- Production sistemlerde
- Bilinmeyen kodla çalışırken
- Güvenilmeyen input ile
- Kritik dosyaların olduğu yerlerde

### Output Flags

| Flag | Açıklama |
|------|----------|
| `--output-format <format>` | Output formatı: `text`, `json`, `stream-json` |
| `--verbose`, `-v` | Detaylı output |
| `--quiet`, `-q` | Minimal output |

```bash
# JSON output - parsing için
claude --print --output-format json "What is 2+2"

# Stream JSON - real-time processing
claude --output-format stream-json "Write a function"
```

### Working Directory

| Flag | Açıklama |
|------|----------|
| `--cwd <path>` | Çalışma dizinini ayarla |
| `--add-dir <path>` | Ek dizin ekle (multiple allowed) |

```bash
# Farklı dizinde çalış
claude --cwd /path/to/project "Fix the bug"

# Birden fazla dizin ekle
claude --add-dir ./lib --add-dir ./tests "Run all tests"
```

### MCP Flags

| Flag | Açıklama |
|------|----------|
| `--mcp-server <config>` | MCP server ekle (JSON string) |
| `--no-mcp` | MCP server'ları devre dışı bırak |

```bash
# Inline MCP server
claude --mcp-server '{"name":"db","command":"python","args":["db_server.py"]}'

# MCP olmadan çalış
claude --no-mcp "Simple task"
```

### Timeout ve Limitler

| Flag | Açıklama |
|------|----------|
| `--timeout <ms>` | Maksimum çalışma süresi (milisaniye) |
| `--max-turns <n>` | Maksimum conversation turn sayısı |

```bash
# 5 dakika timeout
claude --timeout 300000 "Complex refactoring task"

# Maksimum 10 turn
claude --max-turns 10 "Quick fix"
```

### System Prompt

| Flag | Açıklama |
|------|----------|
| `--system-prompt <prompt>` | Custom system prompt |
| `--append-system-prompt <text>` | Mevcut system prompt'a ekle |

```bash
# Custom system prompt
claude --system-prompt "You are a Python expert" "Review this code"

# Ek talimat
claude --append-system-prompt "Always use type hints" "Write a function"
```

### Debug ve Diagnostics

| Flag | Açıklama |
|------|----------|
| `--debug` | Debug mode |
| `--doctor` | Kurulum kontrolü |
| `--version` | Versiyon göster |
| `--help` | Yardım göster |

### Tam Örnek: CI/CD Pipeline

```bash
#!/bin/bash
# ci-claude.sh - CI/CD'de Claude Code kullanımı

claude \
  --headless \
  --dangerously-skip-permissions \
  --timeout 600000 \
  --max-turns 20 \
  --output-format json \
  --cwd /workspace \
  "Run tests, fix any failures, and commit the fixes"
```

### Tam Örnek: Automated Code Review

```bash
#!/bin/bash
# review.sh - Otomatik kod review

DIFF=$(git diff main...HEAD)

claude \
  --headless \
  --print \
  --model sonnet \
  --system-prompt "You are a code reviewer. Be concise." \
  "Review this diff and list issues:\n\n$DIFF"
```

### Flag Kombinasyonları

| Kombinasyon | Use Case |
|-------------|----------|
| `--headless --print` | Tek seferlik task, output al |
| `--headless --dangerously-skip-permissions` | Full automation |
| `--resume --model opus` | Önceki session'ı güçlü modelle devam |
| `--print --output-format json` | Programmatic output |

---

## Slash Commands (Built-in)

### Session Management
| Command | Description |
|---------|-------------|
| `/help` | Show help and available commands |
| `/clear` | Clear conversation history |
| `/compact` | Compact context (summarize and reduce token usage) |
| `/quit` or `/exit` | Exit Claude Code |
| `/resume` | Resume a previous conversation |

### Task Management
| Command | Description |
|---------|-------------|
| `/tasks` | List background tasks (shells, agents) |
| `/status` | Show current session status |

### Code Operations
| Command | Description |
|---------|-------------|
| `/init` | Initialize Claude Code in current directory |
| `/add-dir <path>` | Add directory to context |
| `/review` | Review recent changes |
| `/commit` | Stage and commit changes with AI-generated message |
| `/pr` | Create a pull request |
| `/diff` | Show current diff |

### Configuration
| Command | Description |
|---------|-------------|
| `/config` | Show/edit configuration |
| `/permissions` | Manage tool permissions |
| `/model` | Switch model (sonnet, opus, haiku) |
| `/memory` | Manage project memory (CLAUDE.md) |

### MCP & Tools
| Command | Description |
|---------|-------------|
| `/mcp` | Show MCP server status |
| `/tools` | List available tools |

### Mode Switching
| Command | Description |
|---------|-------------|
| `/vim` | Enter vim mode |
| `/plan` | Enter planning mode |

### Special
| Command | Description |
|---------|-------------|
| `/bug` | Report a bug |
| `/cost` | Show token/cost usage |
| `/doctor` | Diagnose installation issues |
| `/login` | Authenticate with Anthropic |
| `/logout` | Clear authentication |

---

## Custom Commands

Create project-specific commands in `.claude/commands/`:

### Structure
```
.claude/
  commands/
    my-command.md      # Simple command
    complex/
      index.md         # Multi-file command
```

### Format
```markdown
---
description: "What this command does"
allowed-tools: ["Read", "Edit", "Bash"]  # Optional tool restrictions
---

# Command Instructions

Your prompt/instructions here.
$ARGUMENTS will be replaced with user input.
```

### Usage
```bash
/project:my-command arg1 arg2
```

---

## Skills (Auto-triggered Capabilities)

Skills are specialized capabilities that Claude Code can invoke based on context:

| Skill | Trigger | Description |
|-------|---------|-------------|
| `commit` | `/commit` or commit request | Git staging and committing |
| `review-pr` | PR review request | Pull request review |
| `pdf` | PDF file in context | PDF reading and analysis |

Skills are defined in `.claude/skills/` or provided by MCP servers.

---

## Subagents

Claude Code can spawn specialized subagents for complex tasks:

### Available Subagents

| Type | Description | Use Case |
|------|-------------|----------|
| `Explore` | Fast codebase exploration | Finding files, searching code, understanding structure |
| `Plan` | Software architect | Designing implementation plans, architectural decisions |
| `Bash` | Command execution | Git operations, terminal tasks |
| `general-purpose` | Multi-step tasks | Complex research, code searching |
| `claude-code-guide` | Documentation | Questions about Claude Code features |

### Usage Pattern
Subagents are automatically invoked via the `Task` tool when needed:
```
Task: "Find all API endpoints in the codebase"
Subagent: Explore (quick)
```

---

## Hooks System

Hooks, belirli olaylarda özel shell komutları çalıştırmanızı sağlayan güçlü bir interceptor sistemidir. Claude Code'un her tool çağrısını izleyebilir, loglayabilir veya engelleyebilirsiniz.

### Hook Types

| Hook | Trigger | Use Case |
|------|---------|----------|
| `PreToolUse` | Tool çalışmadan ÖNCE | Validation, logging, blocking |
| `PostToolUse` | Tool çalıştıktan SONRA | Cleanup, verification, audit |
| `Notification` | Bildirim gönderildiğinde | Alerts, Slack/Discord integration |
| `Stop` | Claude durduğunda | Cleanup, final reporting |

### Configuration
```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "command": "echo 'Editing file...' >> /tmp/claude.log"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "command": "python scripts/log_action.py"
      }
    ]
  }
}
```

### Hook Response Format
Hooks can return JSON to influence behavior:
```json
{
  "decision": "allow",  // or "block"
  "reason": "Optional explanation"
}
```

### PreToolUse Blocking Mechanism (Detaylı)

PreToolUse hook'u, Claude'un bir tool'u çalıştırmasını **engelleyebilir**. Bu güçlü bir güvenlik ve kontrol mekanizmasıdır.

**Nasıl Çalışır:**
1. Claude bir tool çağırmaya karar verir (örn: `Edit` ile dosya düzenleme)
2. Tool çalışmadan ÖNCE, PreToolUse hook'u tetiklenir
3. Hook script'i çalışır ve JSON response döner
4. Response `"decision": "block"` içeriyorsa, tool ÇALIŞMAZ
5. Claude, block reason'ı görür ve alternatif yol arar

**Örnek: Belirli Dosyaları Koruma**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "command": "python scripts/hooks/protect_files.py"
      }
    ]
  }
}
```

```python
# scripts/hooks/protect_files.py
import sys
import json
import os

# Hook, tool parametrelerini stdin'den alır
input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name")
tool_input = input_data.get("tool_input", {})

# Korunan dosyalar
PROTECTED_FILES = [
    "src/ybis/constants.py",
    "docs/CONSTITUTION.md",
    "docs/DISCIPLINE.md",
    ".env",
    "secrets.json"
]

file_path = tool_input.get("file_path", "")

if any(protected in file_path for protected in PROTECTED_FILES):
    # BLOCK - Tool çalışmayacak
    print(json.dumps({
        "decision": "block",
        "reason": f"Protected file: {file_path} cannot be modified without approval"
    }))
else:
    # ALLOW - Tool normal çalışacak
    print(json.dumps({
        "decision": "allow"
    }))
```

**Kullanım Senaryoları:**
- **Güvenlik:** Kritik dosyaların (config, secrets) korunması
- **Governance:** Belirli değişikliklerin onay gerektirmesi
- **Audit:** Tüm file operations'ların loglanması
- **Rate Limiting:** Çok fazla API call'ı engelleme
- **Custom Validation:** Business rules enforcement

**Dikkat:**
- Hook script hata verirse, tool ÇALIŞMAZ (fail-safe)
- Hook timeout'u vardır (~30 saniye)
- Blocking çok kullanılırsa Claude çalışamaz hale gelir

---

## MCP Integration

Model Context Protocol enables external tool integration:

### Configuration
```json
// .claude/settings.json
{
  "mcpServers": {
    "ybis": {
      "command": "python",
      "args": ["scripts/ybis_mcp_server.py"],
      "cwd": "/path/to/project"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem", "/allowed/path"]
    }
  }
}
```

### YBIS MCP Tools (25 tools)

**Task Management:**
- `task_create` - Create new task
- `task_status` - Get task status
- `get_tasks` - List tasks with filters
- `claim_task` - Claim task atomically
- `claim_next_task` - Claim next available
- `update_task_status` - Update status
- `task_complete` - Mark complete
- `task_run` - Run workflow immediately

**Artifacts:**
- `artifact_read` - Read artifact
- `artifact_write` - Write artifact
- `artifact_list` - List artifacts

**Messaging:**
- `send_message` - Send to agent
- `read_messages` - Read inbox
- `mark_read` - Mark as read
- `broadcast` - Send to all

**Debate:**
- `start_debate` - Start debate
- `add_position` - Add position
- `vote` - Cast vote
- `close_debate` - Close debate

**Memory:**
- `memory_store` - Store memory
- `memory_search` - Search memories
- `memory_list` - List memories

**System:**
- `system_status` - System health
- `worker_register` - Register worker
- `run_logs` - Get run logs

---

## Plugins (Extension System)

Plugins, Claude Code'un yeteneklerini genişleten modüler extension'lardır. MCP'den farklı olarak, plugins doğrudan Claude Code runtime'ına entegre olur.

### Plugin Türleri

| Tür | Açıklama | Örnek |
|-----|----------|-------|
| **Tool Plugins** | Yeni tool'lar ekler | Custom file processors |
| **Command Plugins** | Yeni slash command'lar | `/deploy`, `/test-all` |
| **Provider Plugins** | Alternatif LLM provider'lar | Local Ollama, Azure OpenAI |
| **Formatter Plugins** | Output formatting | Custom code formatters |
| **Auth Plugins** | Authentication extensions | SSO, custom auth |

### Plugin Yapısı

```
.claude/
  plugins/
    my-plugin/
      manifest.json     # Plugin metadata
      index.js          # Entry point (Node.js)
      # veya
      index.py          # Entry point (Python)
```

### Manifest Format

```json
{
  "name": "my-custom-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "type": "tool",
  "entrypoint": "index.js",
  "permissions": ["read", "write", "network"],
  "config": {
    "apiKey": "${MY_API_KEY}"
  }
}
```

### Örnek: Custom Tool Plugin

```javascript
// .claude/plugins/jira-integration/index.js
module.exports = {
  name: "jira",
  description: "JIRA integration for task management",

  tools: [
    {
      name: "jira_create_issue",
      description: "Create a JIRA issue",
      parameters: {
        type: "object",
        properties: {
          title: { type: "string" },
          description: { type: "string" },
          project: { type: "string" }
        },
        required: ["title", "project"]
      },
      handler: async (params) => {
        // JIRA API call
        const response = await fetch(`${JIRA_URL}/rest/api/2/issue`, {
          method: "POST",
          headers: {
            "Authorization": `Basic ${JIRA_TOKEN}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            fields: {
              project: { key: params.project },
              summary: params.title,
              description: params.description,
              issuetype: { name: "Task" }
            }
          })
        });
        return await response.json();
      }
    }
  ]
};
```

### Plugin vs MCP: Ne Zaman Hangisi?

| Özellik | Plugin | MCP Server |
|---------|--------|------------|
| **Kurulum** | Lokal dosya | Ayrı process |
| **Dil** | JS/Python | Herhangi biri |
| **Izolasyon** | Düşük (in-process) | Yüksek (subprocess) |
| **Use Case** | Basit extensions | Complex integrations |
| **State** | Paylaşımlı | İzole |

**Plugin Kullan:**
- Basit tool ekleme
- Code formatting
- Quick integrations

**MCP Kullan:**
- Database bağlantıları
- External API'ler
- Complex state management
- Multi-client support

### Built-in Plugins

Claude Code bazı built-in plugin'lerle gelir:

| Plugin | Açıklama |
|--------|----------|
| `git` | Git operations (commit, branch, etc.) |
| `prettier` | Code formatting |
| `eslint` | JavaScript linting |
| `typescript` | TypeScript type checking |

### Plugin Geliştirme Best Practices

1. **Minimal permissions** - Sadece gerekli izinleri iste
2. **Error handling** - Graceful failure
3. **Logging** - Debug için log yaz
4. **Versioning** - Semantic versioning kullan
5. **Documentation** - README.md ekle

### Plugin Aktivasyonu

```json
// .claude/settings.json
{
  "plugins": {
    "enabled": ["jira-integration", "custom-formatter"],
    "disabled": ["experimental-feature"]
  }
}
```

---

## Built-in Tools

Claude Code has direct access to these tools:

| Tool | Description |
|------|-------------|
| `Read` | Read file contents |
| `Write` | Write file (requires prior read) |
| `Edit` | Edit file with string replacement |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `Bash` | Execute shell commands |
| `WebFetch` | Fetch URL content |
| `WebSearch` | Search the web |
| `Task` | Spawn subagent |
| `TodoWrite` | Manage todo list |
| `AskUserQuestion` | Ask clarifying questions |
| `NotebookEdit` | Edit Jupyter notebooks |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit (when input empty) |
| `Ctrl+L` | Clear screen |
| `Ctrl+R` | Reverse search history |
| `Ctrl+Z` | Undo (in supported contexts) |
| `Tab` | Autocomplete |
| `Up/Down` | Navigate history |

---

## IDE Integrations

Claude Code integrates with:

### VS Code
- Extension: "Claude Code"
- Features: Inline suggestions, chat panel, code actions

### JetBrains IDEs
- Plugin: "Claude Code"
- Features: Tool window, intentions, inspections

### Vim/Neovim
- `/vim` mode in CLI
- Plugin: vim-claude (community)

### Terminal Integration
- iTerm2: Shell integration
- Windows Terminal: Full support
- tmux: Session persistence

---

## Configuration Files

### Project Settings
```
.claude/
  settings.json     # Project settings
  settings.local.json  # Local overrides (gitignored)
  commands/         # Custom commands
  skills/           # Custom skills
  memory/           # Persistent memory
```

### Global Settings
- Linux/macOS: `~/.claude/settings.json`
- Windows: `%USERPROFILE%\.claude\settings.json`

### Settings Schema
```json
{
  "defaultModel": "sonnet",
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": ["Bash:rm -rf"]
  },
  "mcpServers": {},
  "hooks": {},
  "memory": {
    "enabled": true,
    "path": ".claude/memory"
  }
}
```

---

## Memory System

### CLAUDE.md
Project-specific context file read at startup:
```markdown
# Project: YBIS

## Architecture
- LangGraph orchestration
- Aider code generation

## Conventions
- Use src/ybis/ for all source code
- All tests in tests/
```

### Persistent Memory
Claude Code can store and retrieve memories:
```
/memory add "User prefers TypeScript over JavaScript"
/memory list
/memory search "preferences"
```

---

## Permission System

### Tool Permissions
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Bash:git *",
      "Bash:npm *"
    ],
    "deny": [
      "Bash:rm -rf *",
      "Bash:sudo *"
    ]
  }
}
```

### Permission Prompts
When a tool requires permission:
1. Claude asks for confirmation
2. User can allow once, always, or deny
3. Choices are saved to settings

---

## Model Selection

| Model | ID | Best For |
|-------|-----|----------|
| Claude Opus 4.5 | `opus` | Complex reasoning, large codebases |
| Claude Sonnet 4 | `sonnet` | General coding, good balance |
| Claude Haiku | `haiku` | Quick tasks, low latency |

Switch models:
```bash
/model opus
/model haiku
```

---

## Context Compaction (Detaylı)

Context Compaction, Claude Code'un uzun konuşmaları yönetmek için kullandığı otomatik özetleme mekanizmasıdır.

### Problem: Context Window Limiti

Claude'un bir context window limiti vardır (~200K token). Uzun bir coding session'da:
- Okunan dosyalar
- Tool çıktıları
- Konuşma geçmişi
- Kod değişiklikleri

Tüm bunlar token tüketir. Limit aşılırsa Claude çalışamaz.

### Çözüm: Automatic Compaction

**Nasıl Çalışır:**
1. Context ~150K token'a ulaştığında otomatik tetiklenir
2. Claude, konuşma geçmişini analiz eder
3. Önemli bilgileri (kararlar, değişiklikler, context) korur
4. Detayları (tam dosya içerikleri, uzun çıktılar) özetler
5. Yeni, sıkıştırılmış context ile devam eder

**Otomatik Compaction Çıktısı:**
```
[Context compacted: 156K → 45K tokens]
Preserved:
- Current task: Implement user authentication
- Modified files: src/auth.py, src/routes.py
- Key decisions: Using JWT tokens, 24h expiry
- Pending: Add refresh token logic
```

### Manuel Compaction

```bash
/compact
```

**Ne Zaman Kullanılır:**
- Uzun bir session'dan sonra temiz başlangıç
- Farklı bir konuya geçmeden önce
- Token tasarrufu yapmak istediğinizde

### Compaction Stratejileri

| Strateji | Açıklama | Korunan |
|----------|----------|---------|
| **Aggressive** | Maksimum sıkıştırma | Sadece son kararlar |
| **Balanced** | Dengeli (default) | Kararlar + key context |
| **Conservative** | Minimal sıkıştırma | Çoğu detay korunur |

### Ne Korunur, Ne Kaybolur?

**Korunan:**
- Task tanımı ve hedefler
- Alınan kararlar ve nedenleri
- Değiştirilen dosyaların listesi
- Karşılaşılan hatalar ve çözümleri
- User tercihleri

**Özetlenen/Kaybolan:**
- Tam dosya içerikleri (path korunur)
- Uzun tool çıktıları
- Ara adımların detayları
- Deneme-yanılma süreçleri

### Compaction ve Session Continuity

Compaction sonrası Claude:
- Önceki context'i "hatırlar" (özet olarak)
- Gerekirse dosyaları tekrar okuyabilir
- Kararları tutarlı şekilde sürdürür

**Örnek Senaryo:**
```
Session Start: 0K tokens
... 2 saat coding ...
Before Compaction: 156K tokens
After Compaction: 45K tokens
... devam ...
```

### Best Practices

1. **Büyük dosyaları parça parça oku** - Tüm codebase'i bir anda okuma
2. **Subagent kullan** - Explore agent kendi context'ini yönetir
3. **Periyodik compact** - Her 1-2 saatte bir `/compact`
4. **CLAUDE.md kullan** - Kritik bilgiler her zaman yüklenir

---

## Cost Management

### View Costs
```bash
/cost
```

### Reduce Costs
1. Use `/compact` to summarize context
2. Use `haiku` for simple tasks
3. Limit tool outputs with filters
4. Use subagents for exploration

### Token Limits
- Context window: ~200K tokens
- Automatic compaction at ~150K
- Manual compaction with `/compact`

---

## Troubleshooting

### Common Issues

**Tool Permission Denied:**
```bash
/permissions
# Add required tool to allow list
```

**MCP Server Not Starting:**
```bash
/mcp
# Check server configuration
python scripts/ybis_mcp_server.py  # Test manually
```

**Context Too Large:**
```bash
/compact
# Or start fresh session
```

**Authentication Issues:**
```bash
/doctor
/login
```

---

## YBIS Integration

### Configuration
```json
// .claude/settings.json
{
  "mcpServers": {
    "ybis": {
      "command": "python",
      "args": ["scripts/ybis_mcp_server.py"],
      "cwd": "C:\\Projeler\\YBIS_Dev"
    }
  }
}
```

### Workflow
1. Check tasks: `get_tasks`
2. Claim task: `claim_next_task`
3. Execute: `task_run`
4. Complete: `task_complete`

### Best Practices
- Use MCP tools for task management
- Follow governance (CONSTITUTION.md)
- Create artifacts (PLAN.md, RESULT.md)
- Log all actions

---

## Version Information

- **Claude Code Version:** 1.x
- **Model:** Claude Opus 4.5 (claude-opus-4-5-20251101)
- **Knowledge Cutoff:** May 2025
- **Last Updated:** 2026-01-10

---

## References

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [MCP Specification](https://modelcontextprotocol.io)
- [YBIS Constitution](docs/CONSTITUTION.md)
- [YBIS Discipline](docs/DISCIPLINE.md)
- [YBIS Agents Guide](docs/AGENTS.md)
- [Quick Reference](docs/QUICK_REFERENCE.md)
