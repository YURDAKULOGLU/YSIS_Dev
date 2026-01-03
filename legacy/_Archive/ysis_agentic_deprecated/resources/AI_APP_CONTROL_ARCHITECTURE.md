# AI-Controlled App State & UI System Architecture

**Date:** 2025-10-29
**Purpose:** AI can control theme, navigation, and show live updates during execution
**Scope:** AppActionPort - AI → App Control Interface

---

## 🎯 CORE REQUIREMENTS

### **AI Yetenekleri:**
```yaml
1. Theme Control:
   - "Switch to dark mode"
   - "Change theme to blue"

2. Navigation Control:
   - "Open settings"
   - "Go to tasks page"
   - "Show calendar"

3. Live UI Updates:
   - Task oluştururken widget'ta görünsün (streaming)
   - Database'e yazmadan önce UI'da preview
   - AI çalışırken progress göster
```

---

## 🏗️ ARCHITECTURE: AppActionPort

### **1. AppActionPort Interface**

```typescript
// packages/core/src/ports/AppActionPort.ts

export interface AppActionPort {
  // Navigation Control
  navigate(route: string): Promise<void>;
  goBack(): Promise<void>;

  // Theme Control
  setTheme(theme: 'light' | 'dark' | 'system'): Promise<void>;
  setAccentColor(color: string): Promise<void>;

  // UI State Control
  showLoading(message?: string): void;
  hideLoading(): void;
  showToast(message: string, type?: 'success' | 'error' | 'info'): void;

  // Live Updates (Optimistic UI)
  previewTask(task: Partial<Task>): string; // Returns preview ID
  confirmTask(previewId: string, task: Task): void; // Commit to store
  cancelPreview(previewId: string): void; // Rollback

  previewNote(note: Partial<Note>): string;
  confirmNote(previewId: string, note: Note): void;
  cancelPreview(previewId: string): void;
}
```

---

## 🎯 COMPLETE FLOW EXAMPLE

```
USER: "Add task to review PR and switch to dark mode"

AI PROCESSING:
  ↓
  [Calls createTask + setTheme tools in parallel]
  ↓
EXECUTION:

  createTask Tool:
    1. appActionPort.previewTask()
       → Widget shows gray task card with spinner ⚡
    2. databasePort.create() (background)
    3. appActionPort.confirmTask()
       → Gray card turns blue ✅
    4. Toast: "Task created!"

  setTheme Tool:
    1. appActionPort.setTheme('dark')
       → Theme instantly changes 🌙

RESULT: Both actions complete, UI smooth! ✨
```

---

## 📋 KEY FEATURES

**1. Optimistic UI:**
- Preview shows immediately
- Database save in background
- Confirm or rollback based on result

**2. Live Feedback:**
- Spinner during creation
- Opacity change for preview state
- Smooth animations

**3. App Control:**
- AI can change theme
- AI can navigate screens
- AI can show toasts

---

**Full implementation details in Epic 8 Story 8.6**
