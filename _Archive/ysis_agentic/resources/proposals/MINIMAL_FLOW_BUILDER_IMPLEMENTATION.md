# Minimal Flow Builder - Implementation Plan

**Date:** 2025-12-03
**Status:** Ready for Implementation
**Context:** Closed Beta MVP - Ship fast, iterate based on feedback
**Philosophy:** "Perfect olmasına gerek yok, closed beta'da geri bildirim toplayıp ihtiyaçlar belli olacak"

---

## 🎯 Core Concept

**NOT a complex visual flow editor.**
**NOT pre-built specific templates.**

✅ **Simple, linear flow builder** where users create their own flows:
1. Choose WHEN (trigger)
2. Choose WHAT (tool)
3. Set parameters
4. Choose output
5. Save

---

## 📱 User Experience (Mobile-first, Minimal UI)

### **Flow Creation Screen**

```
┌──────────────────────────────────┐
│ ← Create Flow                    │
├──────────────────────────────────┤
│                                  │
│ Flow Name                        │
│ ┌──────────────────────────────┐ │
│ │ My daily reminder            │ │
│ └──────────────────────────────┘ │
│                                  │
│ When to run?                     │
│ ┌──────────────────────────────┐ │
│ │ ( ) Manual                   │ │
│ │ (•) Schedule                 │ │
│ │   Every: [Daily ▼]           │ │
│ │   At: [09:00]                │ │
│ └──────────────────────────────┘ │
│                                  │
│ What to do?                      │
│ ┌──────────────────────────────┐ │
│ │ Tool: [searchTasks ▼]        │ │
│ │                              │ │
│ │ Parameters:                  │ │
│ │ Status: [pending ▼]          │ │
│ │ Priority: [all ▼]            │ │
│ └──────────────────────────────┘ │
│                                  │
│ How to show result?              │
│ ┌──────────────────────────────┐ │
│ │ (•) Notification             │ │
│ │ ( ) Create Note              │ │
│ │                              │ │
│ │ Message:                     │ │
│ │ ┌──────────────────────────┐ │ │
│ │ │ You have {{count}} tasks │ │ │
│ │ └──────────────────────────┘ │ │
│ └──────────────────────────────┘ │
│                                  │
│ [Cancel]        [Create Flow]    │
│                                  │
└──────────────────────────────────┘
```

### **Flow List Screen**

```
┌──────────────────────────────────┐
│ Flows                      [+ ]  │
├──────────────────────────────────┤
│                                  │
│ ┌──────────────────────────────┐ │
│ │ 🔔 Daily Task Reminder       │ │
│ │ Every day at 09:00      [🟢] │ │
│ │ [▶]                          │ │
│ └──────────────────────────────┘ │
│                                  │
│ ┌──────────────────────────────┐ │
│ │ 📅 Weekly Planning           │ │
│ │ Monday at 10:00         [🟢] │ │
│ │ [▶]                          │ │
│ └──────────────────────────────┘ │
│                                  │
│ ┌──────────────────────────────┐ │
│ │ 📚 Study Session             │ │
│ │ Manual                  [⚪] │ │
│ │ [▶]                          │ │
│ └──────────────────────────────┘ │
│                                  │
└──────────────────────────────────┘
```

---

## 🏗️ Technical Architecture

### **Data Model (Simplified)**

```typescript
interface Flow {
  id: string;
  user_id: string;
  workspace_id: string;
  name: string;
  is_active: boolean;

  // Trigger
  trigger: {
    type: 'manual' | 'schedule';
    schedule?: {
      frequency: 'daily' | 'weekly' | 'monthly';
      time: string; // "HH:MM"
      day_of_week?: number; // 0-6 for weekly
      day_of_month?: number; // 1-31 for monthly
    };
  };

  // Single tool execution (LINEAR - no multi-step)
  tool: {
    name: string; // 'searchTasks', 'createTask', etc.
    params: Record<string, any>; // user-provided parameters
  };

  // Output
  output: {
    type: 'notification' | 'note';
    template: string; // "You have {{count}} tasks"
  };

  created_at: string;
  updated_at: string;
}
```

### **NO Complex Features (Closed Beta)**

❌ **Multi-step flows** - Tek tool execution yeterli
❌ **Conditional logic** - If/else yok
❌ **Loops** - Repeat yok
❌ **Variables** - Sadece basic {{count}}, {{date}} gibi
❌ **Drag-drop UI** - Basit form yeterli
❌ **Visual flow editor** - Sonra
❌ **Flow marketplace** - Sonra
❌ **Template library** - Kullanıcı kendi yapar

✅ **Simple & Linear** - One trigger → One tool → One output

---

## 🛠️ Implementation Checklist

### **Phase 1: Backend (2-3 hours)**

#### **1.1 queryRAG Tool** (Critical for RAG feature demo)
- [ ] Add `queryRAG` to `apps/mobile/src/services/ai/tools.ts`
  ```typescript
  {
    name: 'queryRAG',
    description: 'Search user documents using semantic search',
    parameters: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' },
        limit: { type: 'number', default: 5 }
      },
      required: ['query']
    }
  }
  ```

- [ ] Implement `queryRAG` in `apps/mobile/src/services/data/toolServiceFunctions.ts`
  ```typescript
  export async function queryRAG(
    args: { query: string; limit?: number },
    userId: string,
    workspaceId: string | null
  ): Promise<any[]> {
    // Use existing RAG infrastructure
    // Semantic search via pgvector
    // Return top-k results with sources
  }
  ```

- [ ] Add case in `apps/mobile/src/services/ai/toolExecutor.ts`
  ```typescript
  case 'queryRAG': {
    const results = await queryRAG(args, userId, workspaceId);
    return `Found ${results.length} results:\n${formatResults(results)}`;
  }
  ```

- [ ] Basic test: AI can call queryRAG and get results

#### **1.2 Flow Database Schema** (if not exists)
- [ ] Check if `flows` table exists
- [ ] If not, create migration:
  ```sql
  CREATE TABLE flows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    trigger JSONB NOT NULL,
    tool JSONB NOT NULL,
    output JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
  ```

#### **1.3 Flow Execution Service**
- [ ] Use existing `FlowEngine` from `packages/core/src/services/FlowEngine.ts`
- [ ] Adapt to simple linear flows (one step only)
- [ ] Or create simplified `executeLinearFlow()` function

---

### **Phase 2: Frontend UI (4-5 hours)**

#### **2.1 Flow Creation Modal**
File: `apps/mobile/src/components/modals/FlowCreateModal.tsx`

```typescript
interface FlowCreateModalProps {
  visible: boolean;
  onClose: () => void;
  onFlowCreated: (flow: Flow) => void;
}

export function FlowCreateModal({ visible, onClose, onFlowCreated }: FlowCreateModalProps) {
  const [name, setName] = useState('');
  const [triggerType, setTriggerType] = useState<'manual' | 'schedule'>('schedule');
  const [frequency, setFrequency] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  const [time, setTime] = useState('09:00');
  const [selectedTool, setSelectedTool] = useState('searchTasks');
  const [toolParams, setToolParams] = useState({});
  const [outputType, setOutputType] = useState<'notification' | 'note'>('notification');
  const [outputTemplate, setOutputTemplate] = useState('');

  const handleCreate = async () => {
    const flow = {
      name,
      trigger: { type: triggerType, schedule: { frequency, time } },
      tool: { name: selectedTool, params: toolParams },
      output: { type: outputType, template: outputTemplate }
    };

    await createFlow(flow);
    onFlowCreated(flow);
    onClose();
  };

  return (
    <Modal visible={visible} onClose={onClose}>
      {/* Form fields */}
    </Modal>
  );
}
```

**Components needed:**
- [ ] `NameInput` - Simple text input
- [ ] `TriggerPicker` - Radio: Manual/Schedule
- [ ] `SchedulePicker` - Frequency dropdown + Time picker
- [ ] `ToolPicker` - Dropdown list of available tools
- [ ] `DynamicParamForm` - Form that changes based on selected tool
- [ ] `OutputPicker` - Radio: Notification/Note
- [ ] `TemplateInput` - Text input with variable hints ({{count}}, {{date}})

#### **2.2 Tool Parameter Forms**

Dynamic forms based on tool selection:

```typescript
const TOOL_PARAM_SCHEMAS = {
  searchTasks: [
    { name: 'status', type: 'enum', options: ['todo', 'done', 'all'] },
    { name: 'priority', type: 'enum', options: ['low', 'medium', 'high', 'all'] }
  ],
  createTask: [
    { name: 'title', type: 'string', required: true },
    { name: 'priority', type: 'enum', options: ['low', 'medium', 'high'] }
  ],
  createCalendarEvent: [
    { name: 'title', type: 'string', required: true },
    { name: 'start_time', type: 'time', required: true },
    { name: 'duration', type: 'number', default: 60 }
  ],
  queryRAG: [
    { name: 'query', type: 'string', required: true },
    { name: 'limit', type: 'number', default: 5 }
  ]
};
```

#### **2.3 Flow List Screen**
File: `apps/mobile/app/(tabs)/flows.tsx` (already exists, enhance it)

- [ ] List all flows (name, trigger description, active status)
- [ ] Toggle switch for active/inactive
- [ ] Manual trigger button (▶)
- [ ] Delete flow (swipe to delete)
- [ ] [+] button → Open FlowCreateModal

#### **2.4 Flow Execution**
- [ ] Manual execution: Call `executeFlow()` on button press
- [ ] Scheduled execution: Backend cron or React Native scheduler
- [ ] Show result as notification or create note
- [ ] Handle errors gracefully

---

### **Phase 3: Testing (1 hour)**

#### **End-to-End Test Scenarios:**

1. **Create Manual Flow**
   - [ ] Create flow: "Quick Task List"
   - [ ] Trigger: Manual
   - [ ] Tool: searchTasks (status: pending)
   - [ ] Output: Notification "{{count}} tasks pending"
   - [ ] Press ▶ button → Notification appears

2. **Create Scheduled Flow**
   - [ ] Create flow: "Daily Morning Reminder"
   - [ ] Trigger: Schedule (Daily at 09:00)
   - [ ] Tool: searchTasks (priority: high)
   - [ ] Output: Note "Today's priorities"
   - [ ] Wait for 09:00 OR manually trigger for testing
   - [ ] Note created in workspace

3. **RAG Flow**
   - [ ] Create flow: "Document Search"
   - [ ] Trigger: Manual
   - [ ] Tool: queryRAG (query: "user input")
   - [ ] Output: Note with search results
   - [ ] Execute → Note with RAG results

4. **Calendar Flow**
   - [ ] Create flow: "Weekly Review"
   - [ ] Trigger: Schedule (Weekly, Sunday 18:00)
   - [ ] Tool: getCalendarEvents (date range: this week)
   - [ ] Output: Note "This week's events"
   - [ ] Execute → Note created

---

## 📋 Minimal Feature Set (Closed Beta)

### **Triggers (2 types)**
- ✅ Manual (button click)
- ✅ Schedule (daily/weekly at HH:MM)

### **Tools (6 tools)** - Existing AI tools
- ✅ searchTasks
- ✅ createTask
- ✅ createNote
- ✅ createCalendarEvent
- ✅ getCalendarEvents
- ✅ queryRAG (NEW)

### **Output (2 types)**
- ✅ Notification (push notification)
- ✅ Note (create note in workspace)

### **Variables (Basic)**
- ✅ `{{count}}` - Result count
- ✅ `{{date}}` - Current date
- ✅ `{{time}}` - Current time
- ✅ Tool-specific outputs (e.g., `{{task_titles}}`)

---

## ⏱️ Estimated Timeline

| Task | Time | Priority |
|------|------|----------|
| queryRAG Tool Implementation | 2h | P0 |
| Flow Database Schema | 30min | P0 |
| Flow Creation Modal UI | 3h | P0 |
| Dynamic Param Forms | 1.5h | P0 |
| Flow List & Execution | 1.5h | P0 |
| Testing & Bug Fixes | 1h | P0 |
| **TOTAL** | **9.5h** | **~1-1.5 days** |

---

## 🚀 Ship Criteria (Closed Beta)

### **Must Have:**
- ✅ Users can create flows via simple form
- ✅ Manual flows execute on button press
- ✅ Scheduled flows execute at specified time
- ✅ Notifications work
- ✅ Notes are created
- ✅ queryRAG demonstrates RAG capability

### **Nice to Have (Post-Beta):**
- Event-based triggers
- Multi-step flows
- Conditional logic
- Visual flow editor
- Template marketplace
- Flow analytics

---

## 💡 Post-Beta Iteration Strategy

1. **Ship minimal flow builder** → Closed beta
2. **Collect feedback:**
   - Which tools are most used?
   - Which triggers are most needed?
   - What output formats are preferred?
   - What parameters are confusing?
3. **Iterate:**
   - Add most-requested tools
   - Improve UX based on confusion points
   - Add advanced features if needed
4. **Expand:**
   - Multi-step flows (if requested)
   - More complex triggers (if requested)
   - Community templates (if requested)

---

## 📝 Key Decisions

### **Why Linear (Single Tool) Flows?**
- Simpler to implement
- Easier to understand for users
- Covers 80% of use cases
- Can add multi-step later if needed

### **Why Minimal UI?**
- Mobile-first (simple forms work best)
- Faster to ship
- Less overwhelming for users
- Can enhance based on feedback

### **Why No Pre-built Templates?**
- More flexible (users create what they need)
- Less maintenance
- Avoids template explosion
- Generic flow builder > specific templates

---

## 🎯 Success Metrics (Closed Beta)

- [ ] 80%+ users create at least 1 flow
- [ ] 50%+ users create 3+ flows
- [ ] 0 critical bugs in flow execution
- [ ] Average flow creation time < 2 minutes
- [ ] Positive feedback on flexibility vs ease-of-use balance

---

**Status:** Ready for implementation
**Next Step:** Start with queryRAG tool implementation
**Target:** Ship to closed beta in 1-1.5 days
