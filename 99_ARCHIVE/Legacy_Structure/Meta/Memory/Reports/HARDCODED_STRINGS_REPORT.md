# Hardcoded Strings Report - i18n Coverage

**Date:** 2025-01-25  
**Status:** 🔴 Critical - Many user-facing strings are not internationalized

---

## Summary

Found **100+ hardcoded strings** that need i18n integration. These are categorized by:
1. **AI Prompts** - Turkish hardcoded
2. **Error Messages** - English hardcoded  
3. **Toast Messages** - Mixed Turkish/English
4. **Tool Executor Responses** - English hardcoded
5. **Flow Messages** - Turkish hardcoded
6. **UI Labels** - Various

---

## 1. AI Prompts (promptGenerator.ts)

**File:** `apps/mobile/src/services/ai/promptGenerator.ts`

All prompts are hardcoded in Turkish:

```typescript
// Line 15-16
'Kullanıcının son notları:\n...'
'Kullanıcının hiç notu yok.'

// Line 19-20
'Aktif görevleri:\n...'
'Kullanıcının hiç aktif görevi yok.'

// Line 23-24
'Bugünkü veya yaklaşan takvim etkinlikleri:\n...'
'Kullanıcının bugün veya yaklaşan takvim etkinliği yok.'

// Line 26-44
'Sen YBIS yapay zeka asistanısın...'
'Kullanıcı Türkçe konuşuyor. Sen de Türkçe yanıt ver.'
'TOOL KULLANIM REHBERİ:'
'NOT SİLME: Önce searchNotes ile notu bul...'
// ... etc
```

**Action Required:**
- Create i18n keys: `ai.system_prompt.*`
- Detect user language and use appropriate prompt
- Make tool usage guide language-aware

---

## 2. Error Messages (Multiple Files)

### 2.1. Authentication Errors

**File:** `apps/mobile/src/services/data/toolServiceFunctions.ts`

```typescript
// Lines 156, 181, 204, 236, 251, 275, 314, 329, 368, 407, 464, 530, 568, 619, 678, 705, 742, 764, 825
throw new Error('User not authenticated.');
throw new Error('Workspace not set. Please ensure you have a workspace.');
```

**File:** `apps/mobile/src/contexts/useAuth.ts`
```typescript
// Line 262
throw new Error('Google sign in was cancelled');
```

**File:** `apps/mobile/src/features/flows/hooks/useFlows.ts`
```typescript
// Lines 249, 666, 719
throw new Error('AI processor not initialized');
throw new Error('User not authenticated');
throw new Error('Invalid JSON structure');
```

**Action Required:**
- Create i18n keys: `errors.auth.*`, `errors.workspace.*`, `errors.ai.*`
- Replace all `throw new Error('...')` with `throw new Error(t('errors.*'))`

### 2.2. Logger Error Messages

**File:** `apps/mobile/src/hooks/useNotifications.ts`

```typescript
// Lines 76, 122, 176, 200, 219, 247
Logger.error('Failed to check notification permissions', ...);
Logger.error('Failed to request notification permission', ...);
Logger.error('Failed to schedule notification', ...);
Logger.error('Failed to cancel notification', ...);
Logger.error('Failed to cancel all notifications', ...);
Logger.error('Failed to register for push notifications', ...);
```

**File:** `apps/mobile/src/services/data/toolServiceFunctions.ts`

```typescript
// Multiple lines
Logger.error('createTask: User ID is missing', ...);
Logger.error(`Failed to create task: ${args.title}`, ...);
Logger.error('createNote: User ID is missing', ...);
// ... etc for all tool functions
```

**Action Required:**
- Logger messages can stay in English (internal), but user-facing errors need i18n

---

## 3. Toast Messages

### 3.1. FlowBuilder Component

**File:** `apps/mobile/src/features/flows/components/FlowBuilder.tsx`

```typescript
// Line 307
toast.error('Lütfen akış adı girin', 'Eksik Bilgi');

// Line 312
toast.error('AI işleme için talimat girin', 'Eksik Bilgi');

// Line 348
toast.success('Akış güncellendi', 'Başarılı');

// Line 355
toast.error(isEditMode ? 'Akış güncellenemedi' : 'Akış oluşturulamadı', 'Hata');
```

**Action Required:**
- Create i18n keys: `flows.validation.*`, `flows.success.*`, `flows.errors.*`

### 3.2. useFlows Hook

**File:** `apps/mobile/src/features/flows/hooks/useFlows.ts`

```typescript
// Line 652
toast.success('Sesli okuma başladı', 'Akış');

// Line 656
toast.info(cleanText, 'Akış Sonucu');

// Line 711
toast.success(`Not oluşturuldu: ${title}`, 'Akış');

// Line 954
toast.error('Workspace not ready. Please try again.', 'Error');

// Line 1052
toast.error('Flow not found', 'Error');

// Line 1058
toast.error('Flow is not active', 'Error');
```

**Action Required:**
- Create i18n keys: `flows.toast.*`
- Mix of Turkish and English - standardize

### 3.3. Tasks Screen

**File:** `apps/mobile/app/(tabs)/tasks.tsx`

```typescript
// Line 58
toast.success('Task updated');
```

**Action Required:**
- Create i18n key: `tasks.toast.updated`

---

## 4. Tool Executor Responses

**File:** `apps/mobile/src/services/ai/toolExecutor.ts`

All tool responses are hardcoded in English:

```typescript
// Line 66
return `Task "${task.title}" (ID: ${task.id}) updated successfully. ${updates.length > 0 ? `Updates: ${updates.join(', ')}` : ''}`;

// Line 72
return `No events found matching your criteria.`;

// Line 74
return `Found ${events.length} events:\n${events.map(...)}`;

// Line 79
return `Task with ID ${deleteTaskArgs.id} deleted successfully.`;

// Line 85
return `No tasks found matching your criteria.`;

// Line 91
return `Found ${tasks.length} tasks${filters.length > 0 ? ` (${filters.join(', ')})` : ''}:\n...`;

// Line 99
return `Calendar event "${event.title}" created successfully (ID: ${event.id}).\nTime: ${startDate.toLocaleString()} - ${endDate.toLocaleTimeString()}\nCategory: ${event.category}${eventArgs.task_id ? `\nLinked to task: ${eventArgs.task_id}` : ''}`;

// Line 105
return `No calendar events found for the specified time period.`;

// Line 107-111
return `Found ${events.length} calendar event(s):\n${events.map(...)}`;

// Line 120
return `Task "${result.task.title}" scheduled successfully!\nTime: ${startTime.toLocaleString()} - ${endTime.toLocaleTimeString()} (${duration} min)`;

// Line 123
response += `\nCalendar event created (ID: ${result.event.id})`;

// Line 132
return `Calendar event deleted successfully (ID: ${result.deletedIds[0]}).`;

// Line 134
return `Successfully deleted ${result.deletedCount} calendar events.\nDeleted IDs: ${result.deletedIds.join(', ')}`;

// Line 193
return `No results found for "${contextArgs.query}".`;

// Line 196
let response = `Found ${result.totalCount} results for "${contextArgs.query}":\n`;

// Line 199
response += `\n📝 Notes (${result.notes.length}):\n`;

// Line 204
response += `\n\n✅ Tasks (${result.tasks.length}):\n`;

// Line 209
response += `\n\n📅 Events (${result.events.length}):\n`;

// Line 217
return `Error: Unknown tool "${toolName}".`;

// Line 228
return `Error executing tool "${toolName}": ${(error as Error).message}`;
```

**Action Required:**
- Create i18n keys: `tools.responses.*`
- All tool responses need to be translatable
- Use template strings with interpolation

---

## 5. Flow Messages

**File:** `apps/mobile/src/features/flows/hooks/useFlows.ts`

```typescript
// Line 592
title = parsed.title ?? 'Akış';
message = parsed.message ?? parsed.content ?? processedResult;

// Line 597
title = lines[0]?.substring(0, 50) ?? 'Akış';

// Line 601
message = (params['template'] as string) ?? 'Akış tamamlandı';
title = 'Akış';

// Line 623
textToSpeak = (params['template'] as string) ?? 'Akış tamamlandı';

// Line 690
title = lines[0]?.replace(/^#+\s*/, '').trim().substring(0, 100) ?? 'Flow Note';

// Line 696
title = 'Flow Note';

// Line 711
toast.success(`Not oluşturuldu: ${title}`, 'Akış');

// Line 735
description = parsed.description ?? parsed.content ?? '';

// Line 743
title = lines[0]?.replace(/^[-*]\s*/, '').trim().substring(0, 100) ?? 'Flow Task';

// Line 745
description = lines.length > 1 ? lines.slice(1).join('\n').trim() : '';

// Line 748
Logger.info('Using AI JSON result for task', { type: 'FLOW_ENGINE', title });

// Line 751
Logger.info('Using AI text result for task', { type: 'FLOW_ENGINE', title });

// Line 796
title = lines[0]?.replace(/^[-*#]\s*/, '').trim().substring(0, 100) ?? 'Flow Event';

// Line 962
name: flowData.name ?? 'Untitled Flow',
```

**Action Required:**
- Create i18n keys: `flows.defaults.*`
- Standardize default values (mix of Turkish/English)

---

## 6. UI Labels & Placeholders

Need to check:
- Button labels
- Placeholder texts
- Empty state messages
- Loading messages
- Confirmation dialogs

---

## Recommended i18n Keys Structure

```json
{
  "errors": {
    "auth": {
      "not_authenticated": "User not authenticated.",
      "google_cancelled": "Google sign in was cancelled",
      "workspace_not_set": "Workspace not set. Please ensure you have a workspace."
    },
    "ai": {
      "processor_not_initialized": "AI processor not initialized",
      "invalid_json": "Invalid JSON structure"
    },
    "flows": {
      "not_found": "Flow not found",
      "not_active": "Flow is not active",
      "workspace_not_ready": "Workspace not ready. Please try again."
    }
  },
  "toast": {
    "flows": {
      "validation": {
        "name_required": "Lütfen akış adı girin",
        "ai_prompt_required": "AI işleme için talimat girin"
      },
      "success": {
        "created": "Akış oluşturuldu",
        "updated": "Akış güncellendi",
        "note_created": "Not oluşturuldu: {{title}}",
        "speech_started": "Sesli okuma başladı"
      },
      "error": {
        "create_failed": "Akış oluşturulamadı",
        "update_failed": "Akış güncellenemedi"
      }
    },
    "tasks": {
      "updated": "Task updated"
    }
  },
  "tools": {
    "responses": {
      "task_updated": "Task \"{{title}}\" (ID: {{id}}) updated successfully. {{updates}}",
      "task_deleted": "Task with ID {{id}} deleted successfully.",
      "no_events": "No events found matching your criteria.",
      "events_found": "Found {{count}} events:",
      "no_tasks": "No tasks found matching your criteria.",
      "tasks_found": "Found {{count}} tasks{{filters}}:",
      "event_created": "Calendar event \"{{title}}\" created successfully (ID: {{id}}).\nTime: {{start}} - {{end}}\nCategory: {{category}}",
      "event_deleted": "Calendar event deleted successfully (ID: {{id}}).",
      "events_deleted": "Successfully deleted {{count}} calendar events.",
      "task_scheduled": "Task \"{{title}}\" scheduled successfully!\nTime: {{start}} - {{end}} ({{duration}} min)",
      "no_results": "No results found for \"{{query}}\".",
      "results_found": "Found {{count}} results for \"{{query}}\":",
      "unknown_tool": "Error: Unknown tool \"{{toolName}}\".",
      "execution_failed": "Error executing tool \"{{toolName}}\": {{message}}"
    }
  },
  "ai": {
    "system_prompt": {
      "intro": "Sen YBIS yapay zeka asistanısın. Kullanıcının günlük üretkenliğini artırmasına yardımcı olursun.",
      "notes_section": "Kullanıcının son notları:",
      "notes_empty": "Kullanıcının hiç notu yok.",
      "tasks_section": "Aktif görevleri:",
      "tasks_empty": "Kullanıcının hiç aktif görevi yok.",
      "events_section": "Bugünkü veya yaklaşan takvim etkinlikleri:",
      "events_empty": "Kullanıcının bugün veya yaklaşan takvim etkinliği yok.",
      "language_note": "Kullanıcı Türkçe konuşuyor. Sen de Türkçe yanıt ver.",
      "tool_guide": {
        "title": "TOOL KULLANIM REHBERİ:",
        "delete_note": "NOT SİLME: Önce searchNotes ile notu bul, ID'sini al, sonra deleteNote(id) çağır",
        "update_task": "TASK GÜNCELLEME: Önce searchTasks ile taski bul, ID'sini al, sonra updateTask(id, updates) çağır",
        "delete_task": "TASK SİLME: Önce searchTasks ile taski bul, ID'sini al, sonra deleteTask(id) çağır",
        "view_events": "EVENT GÖRÜNTÜLEME: searchEvents ile kullanıcının eventlerini görebilirsin",
        "uuid_format": "ID'ler UUID formatında (örn: \"550e8400-e29b-41d4-a716-446655440000\")",
        "recent_items": "Kullanıcı \"方才 oluşturduğum not/task\" derse, query ile ara ve en son created_at'e sahip olanı seç",
        "important": "ÖNEMLİ: Title veya description'ı ID yerine ASLA kullanma! Her zaman search yapıp UUID al."
      }
    }
  },
  "flows": {
    "defaults": {
      "title": "Akış",
      "completed": "Akış tamamlandı",
      "note_title": "Flow Note",
      "task_title": "Flow Task",
      "event_title": "Flow Event",
      "untitled": "Untitled Flow"
    }
  }
}
```

---

## Priority Actions

1. **🔴 Critical:** AI prompts (promptGenerator.ts) - affects all AI interactions
2. **🔴 Critical:** Error messages - user-facing errors
3. **🟡 High:** Toast messages - visible to users
4. **🟡 High:** Tool executor responses - shown to users in chat
5. **🟢 Medium:** Flow default values - fallback text
6. **🟢 Low:** Logger messages - internal only

---

## Next Steps

1. Add all missing i18n keys to `packages/i18n/src/locales/tr/mobile.json` and `en/mobile.json`
2. Update all files to use `useTranslation` hook
3. Replace hardcoded strings with `t('key')` calls
4. Test with both Turkish and English locales
5. Update AI prompt generator to detect user language

