# Aider Chat Isolation Fix

## Problem

Aider her task için ayrı chat context'i kullanmıyor. Tüm task'lar aynı global chat history'yi paylaşıyor, bu da:
- Token limit aşılmasına (32,773 > 32,768)
- Hallucination'lara (eski task'lardan mesajlar kalıyor)
- Yanlış dosyalara odaklanmaya neden oluyor

## Current Implementation

```python
# src/agentic/core/plugins/aider_executor_enhanced.py
# History dosyaları task-specific ama yeterli değil
"--input-history-file", str(log_dir / "aider_input_history.txt"),
"--chat-history-file", str(log_dir / "aider_chat_history.md"),
"--llm-history-file", str(log_dir / "aider_llm_history.jsonl"),
```

**Sorun:** Aider'ın internal state'i (chat context) hala global olabilir.

## Framework Comparison

### Temporal
- Her workflow ayrı execution context
- State isolation: Her workflow kendi state'ini tutar
- Crash recovery: Workflow state persistent

### Ray
- Her task ayrı ObjectRef
- Actor isolation: Her actor ayrı process/thread
- Resource isolation: CPU/GPU allocation per task

### Prefect
- Her flow run ayrı context
- Task isolation: Her task ayrı execution environment
- State isolation: Flow run state separate

### SPADE
- Her agent ayrı XMPP session
- Message isolation: Agent-to-agent messages separate
- Behaviour isolation: Each behaviour runs independently

### Celery
- Her task ayrı worker process
- Process isolation: Complete OS-level isolation
- State isolation: Task state in Redis/database

## Solution: Aider Chat Isolation

### Option 1: --clear Flag (RECOMMENDED)
```python
# Her task için chat'i temizle
cmd_parts.extend([
    "--clear",  # Clear chat history before starting
    "--no-restore-chat-history",
    # ... rest of flags
])
```

### Option 2: Separate Aider Instance Per Task
```python
# Her task için yeni Aider process
# Worktree zaten ayrı, Aider da ayrı process olmalı
subprocess.Popen([...], cwd=sandbox_path)
```

### Option 3: Chat Context Reset
```python
# Aider'ın chat context'ini reset et
# --message-file ile yeni prompt gönder
# Eski chat history'yi ignore et
```

## Implementation

### Step 1: Add --clear Flag
```python
# src/agentic/core/plugins/aider_executor_enhanced.py
cmd_parts.extend([
    "--clear",  # NEW: Clear chat before starting
    "--no-restore-chat-history",
    "--input-history-file", str(log_dir / "aider_input_history.txt"),
    "--chat-history-file", str(log_dir / "aider_chat_history.md"),
    "--llm-history-file", str(log_dir / "aider_llm_history.jsonl"),
])
```

### Step 2: Verify Isolation
```python
# Test: İki task aynı anda çalıştır
# Her task'ın kendi chat history'si olmalı
# Bir task'ın mesajları diğerine geçmemeli
```

### Step 3: Framework Integration
```python
# Unified task abstraction'da isolation ekle
class UnifiedTask:
    def __init__(self, task_id: str, ...):
        self.task_id = task_id
        self.isolated_context = True  # Her task ayrı context
    
    async def start(self, ...):
        # Framework-specific isolation
        if self.framework == "aider":
            # Aider için --clear flag
        elif self.framework == "temporal":
            # Temporal için workflow isolation
        # ...
```

## Benefits

1. **Token Efficiency:** Her task sadece kendi context'ini kullanır
2. **No Hallucination:** Eski task mesajları yeni task'a geçmez
3. **Correct Focus:** Her task sadece kendi dosyalarına odaklanır
4. **Framework Consistency:** Tüm framework'ler aynı isolation pattern'i kullanır

## Testing

```bash
# Test 1: İki task aynı anda
python scripts/run_orchestrator.py --task-id TASK-1 &
python scripts/run_orchestrator.py --task-id TASK-2 &

# Her task'ın kendi chat history'si olmalı
# TASK-1'in mesajları TASK-2'ye geçmemeli
```

## Status

- [ ] Add --clear flag to Aider command
- [ ] Test chat isolation
- [ ] Update unified task abstraction
- [ ] Document isolation pattern

