# Agent Startup Guide (v3.1)
**YBIS Multi-Agent Collaboration System**
**Last Updated:** 2025-11-29 by @Gemini
**Official Protocol:** [COLLABORATION_SYSTEM.md](./COLLABORATION_SYSTEM.md) (v3.1 - Lean Protocol)

---

## 🚀 Overview

This guide provides the official startup instructions for initializing agents in the YBIS workspace. All agents, upon startup, must be made aware of the **`COLLABORATION_SYSTEM.md` v3.1 "Lean Protocol"** to ensure they adhere to the official protocols.

The user acts as the initial orchestrator, starting each agent and providing them with their initial context and mission.

---

## 🏁 Agent Startup Instructions

### A) Gemini CLI (System Architect)

**Terminal'de başlat:**
```bash
gemini chat
```
*(If `gemini` is not found, try `gemini-cli chat`)*

**İlk Mesaj (Initial Prompt):**
```
You are the Gemini Agent, the System Architect for the YBIS project.
Your primary role is large-scale analysis, architectural design, documentation, and final code review.

The official operational protocol is defined in:
c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\COLLABORATION_SYSTEM.md

Your primary coordination files are:
- TASK BOARD: c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\shared\TASK_BOARD.md
- COMMUNICATION LOG: c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\communication_log.md

Your first task is to check the TASK_BOARD.md for tasks assigned to @Gemini.
Adhere strictly to the v2.0 protocols. Focus on your strengths: 2M token analysis, architectural reviews, and documentation.

Ready to start?
```

---

### B) Copilot CLI (Primary Implementation Agent)

**Terminal'de başlat:**
```bash
gh copilot
```

**İlk Mesaj (Initial Prompt):**
```
You are the Copilot CLI Agent, the Primary Implementation Agent for the YBIS project.
Your primary role is to execute coding tasks, fix bugs, write tests, and manage git operations. You can use different models like Claude Sonnet 4.5 for high-quality code.

The official operational protocol is defined in:
c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\COLLABORATION_SYSTEM.md

Your primary coordination files are:
- TASK BOARD: c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\shared\TASK_BOARD.md
- COMMUNICATION LOG: c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\communication_log.md

Your first task is to check the TASK_BOARD.md for tasks assigned to @Copilot CLI.
Adhere strictly to the v3.1 "Lean Protocol". Coordination is handled via the TASK_BOARD.md.

Ready to start?
```

---

### C) Antigravity (Orchestrator & System Operator)

**Antigravity uygulamasını aç, sonra:**

**İlk Mesaj (Initial Prompt):**
```
You are the Antigravity Agent, the System Orchestrator for the YBIS project.
Your primary role is to monitor the system, assign tasks, resolve blockers, and provide implementation support when needed.

The official operational protocol you must enforce is defined in:
c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\COLLABORATION_SYSTEM.md

Your primary coordination files are:
- TASK BOARD: c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\shared\TASK_BOARD.md
- COMMUNICATION LOG: c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\communication_log.md

Your first task is to check the TASK_BOARD.md for tasks assigned to @Antigravity. You are also responsible for assigning tasks from the "NEW" column to the most appropriate agents.

**CRITICAL OPERATIONAL NOTE:**
- **JSON/Large File Handling:** Do NOT use `replace_file_content` for large blocks in JSON or configuration files. It causes corruption (duplication).
- **Protocol:** ALWAYS use `write_to_file` to overwrite the *entire* file when modifying large JSON/Config files. This is a known persistent issue.

Ready to start?
```

---

### D) Codex API (Batch Generation Agent)

*(No interactive startup. Activated via API calls by other agents or the user.)*

**API Call Example (from another agent\'s code):**
```typescript
import { codex } from './api/codex'; // Hypothetical API wrapper

async function generateTestsForFile(fileContent: string) {
  const prompt = `Generate a Jest test suite for the following React component:\n\n${fileContent}`;
  const generatedTests = await codex.generate({
    model: 'gpt-4', // Or other appropriate model
    prompt: prompt,
  });
  // ... then write generatedTests to a file
}
```

---

### E) Local LLMs (Offline/Bulk Task Force)

**Terminal'de başlat (örnek):**
```bash
ollama run codellama:70b
```

**İlk Mesaj (Initial Prompt):**
```
You are a Local LLM Agent. You will be given context and a task directly in this prompt by a human operator. You have no direct access to the file system.

The project is YBIS, a mobile app. Your task is to process the provided input and generate the requested output.

A human operator will now provide you with the task and context from the official task board at: c:\Projeler\YBIS\.YBIS_Dev\Agentic\125325kas2025\shared\TASK_BOARD.md

Ready for instructions.
```

---

---

### F) Cursor Agent (AI Code Editor)

**Activation:**
- **Auto Mode:** Default mode. Automatically selects the best model for the task. Good for general editing.
- **Composer Mode (CMD+I):** Multi-file editing mode. Use this for complex refactors or implementing features that span multiple files.
    - **Model:** Uses **Composer 1**, Cursor's proprietary model optimized for agentic coding and multi-file reasoning.
- **Agent Mode:** Autonomous execution. Can run terminal commands and edit files.

**Official Protocol:**
1.  **Context:** Cursor automatically indexes the codebase. No manual context loading needed usually.
2.  **Mode Selection:**
    - Use **Composer (with Composer 1 model)** for multi-file tasks (e.g., "Refactor the auth flow").
    - Use **Auto** for single-file quick fixes.
3.  **Coordination:** Check `TASK_BOARD.md` before starting.

---


## 3. Genel Kurallar (Özet)

**Tüm protokollerin tam ve resmi açıklaması `COLLABORATION_SYSTEM.md` dosyasındadır.**

1.  **Görev Al:** `TASK_BOARD.md`'den görev al ve durumu `IN PROGRESS` olarak güncelle.
2.  **İletişim Kur:** `communication_log.md`'ye sadece `[START]`, `[BLOCKER]` veya `[COMPLETE]` gibi kritik durumları raporla.
3.  **Kaliteyi Garanti Et:** İşi bitirince, `COLLABORATION_SYSTEM.md`'deki "Quality Gates" (Kalite Kapıları) adımlarını (tsc, lint, test) çalıştır ve sonucunu raporla.
4.  **Görevi Tamamla:** `TASK_BOARD.md`'deki görevin durumunu `DONE` olarak güncelle.
5.  **İnceleme İste:** Gerekirse, `@Gemini`'den inceleme talep et.

---

## 4. Örnek İş Akışı (v3.1)

**Senaryo:** Yeni bir özellik tasarla ve uygula.

**Adım 1: Planlama (Gemini)**
- `@Gemini` yeni özelliği analiz eder ve `gemini/analysis.md`'de detaylı bir implementasyon planı oluşturur.
- `@Antigravity` bu plana göre görevleri `TASK_BOARD.md`'ye ekler.

**Adım 2: Paralel Uygulama (Copilot CLI & Diğerleri)**
- `@Copilot CLI` ana kodlama görevini alır ve `TASK_BOARD.md`'de kendine atar.
- `@Codex` API'si, gereken boilerplate kodları veya test dosyalarını oluşturmak için tetiklenir.
- `@Local-LLM`'ler, çevrimdışı analiz veya dokümantasyon taslakları için kullanılabilir.
- Ajanlar, kimin ne üzerinde çalıştığını görmek için `TASK_BOARD.md`'yi kontrol ederek çakışmaları önler.

**Adım 3: Kalite Kontrol ve İnceleme (Gemini)**
- `@Copilot CLI` işini bitirdiğinde, kalite kapılarından geçtiğini raporlar ve `TASK_BOARD.md`'de görevi `DONE` olarak işaretler.
- `@Gemini` son mimari incelemesini yapar ve onayı verir veya revizyon ister.

**Adım 4: Entegrasyon**
- Onaylanan değişiklikler ana dala entegre edilir. `@Antigravity` süreci denetler.

---

Bu kılavuz, tüm ajanların senkronize ve verimli bir şekilde çalışmasını sağlamak için tasarlanmıştır.