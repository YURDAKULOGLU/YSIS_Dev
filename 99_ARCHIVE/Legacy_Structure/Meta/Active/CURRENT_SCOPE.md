# YBIS Closed Beta - Scope Definition
**Date:** 2025-11-25 21:00
**Status:** 🎯 Defining Scope & Priorities
**Kapsam Notu:** Tek kaynak docs/CLOSED_BETA_FINAL_SCOPE.md. Release train: 1.0.x (Closed Beta patch), 1.1.x (Closed Beta hardening), 1.2.0 (Open Beta adayı). Google entegrasyonları post-beta; bu dokümandaki entegrasyon istekleri Post-Beta olarak ele alınmalıdır.

---

## ✅ IN SCOPE (Closed Beta)

### 1. CRITICAL BUGS (Fix Now)
- ❌ AI tool calling (delete notes, see events, update task status)
- ❌ Event creation broken
- ❌ i18n translations showing keys
- 🟡 Menu button intermittent
- 🟡 Chat markdown rendering

---

### 2. DATA MODEL REFACTORING (Foundation)

**Problem:** Sayfalar çalışıyor ama sadece liste var, ne olmalı belli değil

#### 2.1 Task Model - Parametre Tanımı
**Soru:** Bir Task nedir? Ne bilgileri olmalı?

**Önerilen Model:**
```typescript
interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'done' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: Date;
  completed_at?: Date;

  // Recurring/Flexible
  recurrence?: {
    type: 'daily' | 'weekly' | 'monthly' | 'flexible';
    interval?: number; // "haftada en az 2 kez"
    flexibility?: boolean;
  };

  // Organization
  tags: string[];
  category?: string;

  // Nested tasks
  parent_id?: string;
  subtasks?: Task[];

  // Metadata
  workspace_id: string;
  user_id: string;
  created_at: Date;
  updated_at: Date;
}
```

**Clarify:** Bu model doğru mu? Eksik/fazla ne var?

---

#### 2.2 Event Model - Parametre Tanımı
**Soru:** Bir Event nedir? Ne bilgileri olmalı?

**Önerilen Model:**
```typescript
interface Event {
  id: string;
  title: string;
  description?: string;
  location?: string;

  // Time
  start_time: Date;
  end_time: Date;
  is_all_day: boolean;
  timezone?: string;

  // Recurrence
  recurrence_rule?: string; // iCal RRULE format

  // Attendees
  attendees: Array<{
    id: string;
    name: string;
    email?: string;
    status: 'accepted' | 'declined' | 'tentative' | 'pending';
  }>;

  // Organization
  category: 'work' | 'personal' | 'health' | 'urgent' | 'social';
  tags: string[];

  // Notifications
  reminders: Array<{
    minutes_before: number;
    method: 'notification' | 'email';
  }>;

  // Metadata
  workspace_id: string;
  user_id: string;
  created_at: Date;
  updated_at: Date;
}
```

**Clarify:** Bu model doğru mu?

---

#### 2.3 Note Model - Parametre Tanımı
**Soru:** Bir Note nedir? Not tipleri neler?

**Önerilen Model:**
```typescript
interface Note {
  id: string;
  title: string;
  content: string; // Markdown supported

  // Type system
  type: 'general' | 'person' | 'file' | 'meeting' | 'idea';

  // For person notes
  person_metadata?: {
    contact_id?: string;
    phone?: string;
    email?: string;
    relationship?: string;
  };

  // For file notes
  file_metadata?: {
    file_path?: string;
    file_type?: string;
    file_size?: number;
  };

  // Organization
  tags: string[];
  is_favorite: boolean;

  // Linking
  linked_tasks?: string[]; // Task IDs
  linked_events?: string[]; // Event IDs

  // Metadata
  workspace_id: string;
  user_id: string;
  created_at: Date;
  updated_at: Date;
}
```

**Clarify:** Note tipleri yeterli mi? Başka ne lazım?

---

#### 2.4 Conversation Model - ChatGPT Gibi
**Soru:** ChatGPT konuşmaları nasıl handle ediyor?

**Önerilen Model (ChatGPT-style):**
```typescript
interface Conversation {
  id: string;
  title: string; // Auto-generated from first message

  // Organization
  folder_id?: string; // Organize conversations
  is_pinned: boolean;
  is_archived: boolean;

  // Metadata
  user_id: string;
  workspace_id: string;
  created_at: Date;
  updated_at: Date; // Last message time
  message_count: number;
}

interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;

  // Function calling
  function_call?: {
    name: string;
    arguments: string;
    result?: string;
  };

  // Metadata
  user_id: string;
  created_at: Date;
}

interface ConversationFolder {
  id: string;
  name: string;
  user_id: string;
  created_at: Date;
}
```

**ChatGPT Features to Implement:**
- ✅ Conversation list (geçmiş sohbetler)
- ✅ Auto-title from first message
- ✅ Pin conversations
- ✅ Archive conversations
- ✅ Organize into folders
- ✅ Search conversations
- ✅ Delete conversations

**Clarify:** Bu yeterli mi? Başka ne lazım?

---

#### 2.5 Flow Model - Akış Sistemi
**Soru:** Akış nedir? Nasıl çalışmalı?

**Önerilen Model:**
```typescript
interface Flow {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;

  // Trigger (when to run)
  trigger: {
    type: 'schedule' | 'event' | 'data_change' | 'manual';

    // For schedule
    schedule?: {
      cron?: string; // "0 9 * * *" (every day 9am)
      timezone?: string;
    };

    // For event
    event?: {
      source: 'email' | 'calendar' | 'notification' | 'webhook';
      filter?: Record<string, any>;
    };

    // For data change
    data_change?: {
      table: 'tasks' | 'notes' | 'events';
      operation: 'create' | 'update' | 'delete';
      filter?: Record<string, any>;
    };
  };

  // Condition (check if should run)
  conditions?: Array<{
    field: string;
    operator: 'equals' | 'contains' | 'greater_than' | 'less_than';
    value: any;
  }>;

  // Actions (what to do)
  actions: Array<{
    type: 'create_task' | 'create_note' | 'send_notification' | 'update_data' | 'call_ai';
    params: Record<string, any>;
  }>;

  // Execution log
  last_run?: Date;
  run_count: number;

  // Metadata
  user_id: string;
  workspace_id: string;
  created_at: Date;
  updated_at: Date;
}
```

**Use Case Örnekleri:**
1. **Mail Kargo Takip:**
   - Trigger: Email geldiğinde
   - Condition: "kargo" içeriyor + "yaklaştı/teslim"
   - Action: Notification gönder + Task oluştur

2. **Deadline Reminder:**
   - Trigger: Her sabah 9:00
   - Condition: Due date bugün veya yarın olan tasklar var
   - Action: Notification gönder

3. **Auto-categorization:**
   - Trigger: Not oluşturulduğunda
   - Condition: Herhangi
   - Action: AI ile kategori belirle + tag ekle

**Clarify:** Bu akış sistemi yeterli mi? Daha fazla ne lazım?

---

### 3. VIEW REFACTORING (UI Improvements)

#### 3.1 Calendar Views
**Current:** Sadece liste
**Needed:**
- 📅 Daily view (günlük)
- 📅 Weekly view (haftalık)
- 📅 Monthly view (aylık)
- 📅 Yearly view (yıllık)

**Reference:** Google Calendar benzeri

---

#### 3.2 Task Views
**Current:** Basit liste
**Needed:**
- 📋 List view (mevcut)
- 📊 Board view (Kanban - todo/in-progress/done)
- 📅 Calendar view (taskları takvimde göster)
- 📈 Timeline view (Gantt-style)

**Reference:** Todoist, Notion benzeri

---

#### 3.3 Notes Views
**Current:** Basit liste
**Needed:**
- 📋 List view (mevcut)
- 🔍 Search/filter by type
- 🏷️ Tag-based organization
- 📁 Folder structure?

**Reference:** Notion, Evernote benzeri

---

#### 3.4 Conversations View (ChatGPT-style)
**Current:** Tek conversation
**Needed:**
- 📜 Conversation list (sidebar)
- 🔍 Search conversations
- 📁 Folders/organization
- 📌 Pin important conversations
- 🗑️ Delete conversations

**Reference:** ChatGPT UI exactly!

---

### 4. ENTEGRASYONLAR (İntegrations)

**Priority Order:**
1. 📧 **Email** (en önemli - kargo tracking, etc.)
2. 📞 **Phone Notifications** (bildirim entegrasyonu)
3. 👥 **Google Contacts** (kişiler/rehber)
4. 📧 **Gmail specific** (mail filtreleme)

**Out of Scope for Now:**
- ❌ Calendar sync (Google/Outlook) - Later
- ❌ File storage (Dropbox/Drive) - Later
- ❌ Social media - Later

---

## ❌ OUT OF SCOPE (Post-Beta / Future)

### Gamification (Sonraki versiyonlarda)
- ❌ Motivasyon modu
- ❌ Achievements
- ❌ Streak tracking
- ❌ Heat maps

**Reason:** Önce core functionality çalışmalı

### Advanced Analytics (Sonraki versiyonlarda)
- ❌ Yıllık rapor
- ❌ İstatistikler sayfası
- ❌ Günlük tutma mod takibi

**Reason:** Önce data collection solid olmalı

### Advanced UI (Sonraki versiyonlarda)
- ❌ Ses dizaynı
- ❌ Temalar
- ❌ Özel ayarlar

**Reason:** Core features önce

---

## 🎯 CLOSED BETA SCOPE - FINAL

### Phase 1: Bug Fixes (Bu Hafta)
1. ✅ AI tool calling fixes
2. ✅ Event creation fix
3. ✅ i18n translations
4. ✅ Menu button
5. ✅ Chat markdown

### Phase 2: Data Models (Önümüzdeki Hafta)
1. ✅ Task model definition & migration
2. ✅ Event model enhancement
3. ✅ Note model with types
4. ✅ Conversation model (ChatGPT-style)
5. ✅ Flow model foundation

### Phase 3: View Refactoring (Sonraki Sprint)
1. ✅ Calendar views (daily/weekly/monthly/yearly)
2. ✅ Task views (list/board/calendar)
3. ✅ Conversations UI (ChatGPT-style sidebar)
4. ✅ Notes organization (tags/search)

### Phase 4: Core Flows (Sonraki Sprint)
1. ✅ Flow engine implementation
2. ✅ Email trigger support
3. ✅ Basic automations (kargo tracking, reminders)

### Phase 5: Integrations (Son Sprint)
1. ✅ Email integration
2. ✅ Phone notifications
3. ✅ Google Contacts

---

## 🔴 ADDITIONAL CRITICAL ISSUES (Devam Eden)

### 6. Conversation Lifecycle & Naming
**Status:** 🔴 MISSING CORE FEATURE

**Current Problem:**
- Tek permanent conversation var
- App yeniden açıldığında aynı chat devam ediyor

**Required Behavior (ChatGPT mantığı):**

#### 6.1 Boş Chat Başlatma
- ✅ App açıldığında boş chat gösterilmeli
- ✅ Sidebar'da önceki chatler görünmeli
- ✅ Kullanıcı istediği chat'e geçebilmeli

#### 6.2 Chat Oluşturma Logic
- ❌ **ASLA** boş chat oluşturulmamalı
- ✅ Kullanıcı mesaj attığında → YENİ chat oluştur
- ✅ Yeni chat otomatik kaydet
- ✅ Chat list'e ekle

#### 6.3 Conversation Renaming (ChatGPT gibi)
- ✅ AI ilk mesajdan otomatik başlık üretir
  - Örnek: "How to fix TypeScript errors" → "TypeScript Error Help"
- ✅ Kullanıcı manuel rename edebilir
- ✅ Başlık 50-60 karakter max

#### 6.4 Chat Navigation
**Sidebar UI:**
```
┌─────────────────────────┐
│  + New Chat             │ ← Always visible
├─────────────────────────┤
│  📌 Pinned              │
│  • TypeScript Errors    │
│  • Week Planning        │
├─────────────────────────┤
│  📅 Today               │
│  • Calendar Setup       │
│  • Task Management      │
├─────────────────────────┤
│  📅 Yesterday           │
│  • Bug Fixes            │
├─────────────────────────┤
│  📅 Previous 7 Days     │
│  • ...                  │
└─────────────────────────┘
```

**Features:**
- ✅ Group by time (Today/Yesterday/7 days/30 days)
- ✅ Pin conversations
- ✅ Delete conversations
- ✅ Search conversations

**Priority:** 🔴 P0 - Critical for UX

---

### 7. Widget Design System
**Status:** 🔴 NEEDS COMPLETE REDESIGN

**Current Problems:**
1. ❌ Widgetler çok dar (too narrow)
2. ❌ Çok basic (no visual hierarchy)
3. ❌ Liste item'ları çok kalın (thick)
4. ❌ Çok az içerik görünüyor (poor info density)

**Requirements:**

#### 7.1 Widget Genişlik
- **Current:** Dar, tek column
- **Needed:** Daha geniş, responsive grid
- **Design:** Horizontal scroll or 2-column grid

#### 7.2 Liste Item Design
**Current:** Kalın, az bilgi
```
┌──────────────────────────┐
│  📝 Task Title          │  ← Çok kalın
│  Description line       │
│  Due: Tomorrow          │
└──────────────────────────┘
```

**Needed:** İnce, yoğun bilgi
```
┌──────────────────────────┐
│ 📝 Task Title  Due: 2h  │  ← İnce
│ Description...          │
├──────────────────────────┤
│ 📅 Event Title  15:00   │
│ Location • 30min        │
└──────────────────────────┘
```

**Design Goals:**
- ✅ Daha ince items (half current height)
- ✅ Daha fazla bilgi göster
- ✅ Visual hierarchy (icons, colors)
- ✅ Quick actions (swipe, tap)

#### 7.3 Widget Types & Content

**Widget 1: Quick Add**
- Hızlı task/note/event ekleme
- Minimal form
- Voice input option?

**Widget 2: Today's Tasks**
- Bugünkü tasklar
- Status indicators
- Quick complete checkbox

**Widget 3: Upcoming Events**
- Yaklaşan eventler (bugün + yarın)
- Time countdown
- Location if exists

**Widget 4: Recent Notes**
- Son eklenen/düzenlenen notlar
- Quick preview
- Favorite indicator

**Widget 5: AI Suggestions**
- AI önerileri
- "You have 3 overdue tasks"
- "Meeting in 30 minutes"
- "Weekly review due"

#### 7.4 Design System Principles
- **Density:** High info density
- **Clarity:** Clear visual hierarchy
- **Action:** Easy interaction
- **Consistency:** Same design language across widgets

**Action Required:**
- 🎨 Design system önerileri toparlayacağız
- 🎨 Her widget için mockup
- 🎨 Responsive behavior
- 🎨 Dark mode support

**Priority:** 🟡 P1 - High (UX critical but not blocker)

---

### 8. List Component Optimization
**Status:** 🔴 NEEDS OPTIMIZATION

**Problem:** Widget içindeki liste item'ları çok kalın

**Current Metrics:**
- Item height: ~80-100px (estimated)
- Visible items: 2-3 max
- Wasted space: High padding/margins

**Target Metrics:**
- Item height: ~40-50px
- Visible items: 5-6 minimum
- Compact but readable

**Changes Needed:**
1. ✅ Reduce vertical padding (16px → 8px)
2. ✅ Smaller font sizes (title: 16px → 14px)
3. ✅ Single-line descriptions (ellipsis)
4. ✅ Inline metadata (not stacked)
5. ✅ Remove unnecessary spacing

**Example Redesign:**
```typescript
// Before (Kalın)
<ListItem padding="$4" gap="$3">
  <Title fontSize="$6">Task Title</Title>
  <Description fontSize="$4">Long description...</Description>
  <Metadata fontSize="$3">Due: Tomorrow</Metadata>
</ListItem>

// After (İnce)
<ListItem padding="$2" gap="$1">
  <HStack space="between">
    <Title fontSize="$4">Task Title</Title>
    <Metadata fontSize="$2" color="$gray9">2h</Metadata>
  </HStack>
  <Description fontSize="$3" numberOfLines={1}>Description...</Description>
</ListItem>
```

**Component to Refactor:**
- TaskItem.tsx
- NoteItem.tsx
- EventItem.tsx
- Widget item components

**Priority:** 🟡 P1 - High (tied to widget redesign)

---

### 9. Widget Orijinal Design & Interactions
**Status:** 🔴 NEEDS CREATIVE DESIGN

**Current Problem:**
- Sadece liste + buton + ekleme yeri (too basic)
- No unique design language
- Static, boring

**Required Innovation:**

#### 9.1 Orijinal Tasarımlar
- ❌ **SADECE LİSTE DEĞİL!**
- ✅ Her widget unique design
- ✅ Visual storytelling
- ✅ Data visualization where appropriate
- ✅ Micro-interactions

**Examples:**
- Tasks: Kanban-style mini cards, not list
- Calendar: Mini month view + today's timeline
- Notes: Card grid with previews
- AI: Chat bubble style suggestions

#### 9.2 Widget Interactions
**Swipe Gestures:**
- Swipe left → Quick actions (complete, delete)
- Swipe right → Details
- Long press → Drag & reorder widgets

**Widget Bar:**
- Horizontal scroll
- Customize order
- Add/remove widgets
- Widget settings (size, content filter)

**Live Updates:**
- Real-time changes visible
- Smooth animations
- Loading states

**Priority:** 🟡 P1 - Design critical

---

### 10. AI Tool Calling - Live Widget Updates
**Status:** 🔴 CRITICAL FEATURE - AI Working Indicator

**Problem:** AI tool calling çalışıyor ama görünmüyor

**Required Behavior:**

#### 10.1 Dynamic Widget Navigation
**Scenario:** AI task ekliyor
1. Chat'te: "Toplantı için hazırlık taskı ekliyorum..."
2. **Widget bar otomatik → Tasks widget'e scroll eder**
3. Tasks widget'te: "AI ekleme yapıyor..." loading indicator
4. Task eklendi → Smooth animation ile görünür
5. Widget'te yeni task highlight olur (2 saniye)

#### 10.2 Cross-Widget Coordination
```typescript
// AI tool execution flow
AI: "Creating task..."
→ Navigate to Tasks widget
→ Show "AI working..." indicator
→ Create task in database
→ Animate new task into widget
→ Return to chat

AI: "Task created: Meeting Prep ✓"
```

#### 10.3 Visual Feedback
- 🤖 "AI çalışıyor" indicator on widget
- ⚡ Loading shimmer effect
- ✨ Success animation
- 🎯 Highlight new/updated item

**Goal:** Kullanıcı AI'ın çalıştığını HİSSETMELİ

**Priority:** 🔴 P0 - Critical for AI UX

---

### 11. AI System Access & Permissions
**Status:** 🔴 ARCHITECTURE NEEDED

**AI Capabilities Expansion:**

#### 11.1 Theme Control
- AI tema değiştirebilir
- "Dark mode'a geç" → Instant switch
- "Mavi temayı kullan" → Apply theme
- Store user preferences

#### 11.2 Settings Access
- AI ayarlara erişebilir
- "Bildirimleri aç" → Enable notifications
- "Otomatik yedeklemeyi başlat" → Configure backup

#### 11.3 System Functions
- Widget reordering
- View switching (calendar daily → weekly)
- Filter adjustments
- Data export

**Tool Definitions Needed:**
```typescript
// Example new tools
{
  name: "change_theme",
  description: "Change app theme",
  parameters: { theme: "light" | "dark" | "blue" | ... }
}

{
  name: "adjust_settings",
  description: "Modify app settings",
  parameters: { setting: string, value: any }
}

{
  name: "switch_view",
  description: "Change current view (calendar, tasks, etc.)",
  parameters: { screen: string, view: string }
}
```

**Priority:** 🟡 P1 - Enhances AI capabilities

---

### 12. Flow System - Template Architecture
**Status:** 🔴 CRITICAL - WORKFLOW DESIGN

**Problem:** Workflow tasarlatmak çok kompleks

**Solution:** Template-based Flow Creation

#### 12.1 Flow Templates
**Pre-built Templates:**

**Template 1: Daily Summary**
```yaml
name: "Daily Summary at 9 AM"
trigger:
  type: schedule
  cron: "0 9 * * *"
actions:
  - call_ai:
      prompt: "Bugünün özeti: {today_tasks}, {today_events}"
  - send_notification:
      title: "Günlük Özet"
      body: "{ai_response}"
```

**Template 2: Cargo Tracking**
```yaml
name: "Cargo Arrival Notification"
trigger:
  type: email
  filter: contains("kargo") AND contains("yaklaştı")
actions:
  - create_task:
      title: "Kargoyu al: {package_name}"
      due: "+2 days"
  - send_notification:
      title: "Kargon yaklaştı!"
```

**Template 3: Overdue Reminder**
```yaml
name: "Overdue Task Reminder"
trigger:
  type: schedule
  cron: "0 10 * * *"
conditions:
  - tasks.due_date < today
  - tasks.status != "done"
actions:
  - send_notification:
      title: "Geciken görevler"
      body: "count: {overdue_count}"
```

#### 12.2 AI Flow Creation
**Natural Language → Template:**

User: "Saat 9'da bana bugünün özetini yaz"

AI Process:
1. Understand intent → Daily summary template
2. Extract parameters:
   - Time: 9:00 AM
   - Action: Create summary
   - Delivery: Notification
3. Fill template:
   ```javascript
   {
     trigger: { cron: "0 9 * * *" },
     actions: [
       { call_ai: "Bugünün özeti" },
       { send_notification: {...} }
     ]
   }
   ```
4. Create flow
5. Confirm: "✓ Her sabah 9'da özet bildirimi gönderilecek"

#### 12.3 Template Catalog
**Common Templates:**
- ⏰ Daily/weekly summaries
- 📦 Package tracking
- ⏰ Deadline reminders
- 📧 Important email alerts
- 🔔 Meeting reminders
- 📊 Weekly reports
- 🎯 Goal tracking
- 🗓️ Calendar sync

#### 12.4 Flexible Template System
- ✅ AI bilir hangi templateler var
- ✅ Template parametrelerini fill eder
- ✅ User custom template ekleyebilir
- ✅ Templates sharable (export/import)

#### 12.5 Flow Designer (Advanced)
**For power users:**
- Visual flow builder (optional)
- Drag-drop nodes
- Test mode
- But: **AI-first approach** (most users won't use designer)

**Priority:** 🔴 P0 - Core differentiation feature

---

### 13. Flow Design UI/UX
**Status:** 🔴 NEEDS UX DESIGN

**Challenge:** Workflow design is complex

**Solution Layers:**

#### 13.1 Layer 1: AI Natural Language (Primary)
```
User: "Her pazartesi 10'da haftalık rapor"
AI: ✓ Flow oluşturuldu
```
- **80% of users** will use this
- No UI needed
- Just conversation

#### 13.2 Layer 2: Template Browser (Secondary)
```
┌─────────────────────────┐
│  Flow Templates         │
│  ◯ Daily Summary        │
│  ◯ Package Tracking     │
│  ◯ Meeting Reminders    │
│  ◯ Weekly Report        │
└─────────────────────────┘
```
- Browse & apply templates
- Simple customization form
- **15% of users**

#### 13.3 Layer 3: Advanced Editor (Power Users)
```
┌─────────────────────────┐
│  Trigger: Schedule      │
│  ├─ Every Monday 10:00  │
│  │                       │
│  Condition: (optional)  │
│  ├─ Tasks > 5           │
│  │                       │
│  Actions:               │
│  ├─ Call AI: "Weekly"   │
│  └─ Send Notification   │
└─────────────────────────┘
```
- Full control
- Debug mode
- **5% of users**

**Design Priority:**
1. AI conversation (must be perfect)
2. Template browser (must be simple)
3. Advanced editor (can be later)

**Priority:** 🔴 P0 - Critical UX decision

---

## ⚠️ IMPORTANT NOTES

### Status of This Document
- ✅ Auto-complete ~98% complete
- ⏳ Gemini'ye gönderilecek
- ⏳ YBIS standards ile homojenize edilecek
- ⏳ Vision ile align edilecek
- ⏳ Daha tartışılacak konular var
- ❌ Agent'lara DAĞITMA - henüz finalize olmadı!

### Next Steps

### Status of This Document
- ✅ Auto-complete devam ediyor
- ⏳ Gemini'ye gönderilecek
- ⏳ YBIS standards ile homojenize edilecek
- ⏳ Vision ile align edilecek
- ⏳ Daha tartışılacak konular var
- ❌ Agent'lara DAĞITMA - henüz finalize olmadı!

### Next Steps
1. **User:** Daha fazla requirement ekle
2. **Claude:** Document'i complete et
3. **Gemini:** YBIS standards check
4. **Team:** Discuss & prioritize
5. **Then:** Agent task assignment

---

## ❓ CLARIFICATION QUESTIONS

### Data Models:
1. Task model doğru mu? Recurring task logic nasıl olsun?
2. Event model yeterli mi? Attendee management detaylı mı olsun?
3. Note tipleri (person, file, meeting) yeterli mi? Başka tip?
4. Conversation model ChatGPT gibi mi olsun? Folder sistemi?
5. Flow model bu kadar kompleks mi olmalı yoksa daha basit mi başlayalım?

### Views:
1. Calendar views: Google Calendar benzeri mi?
2. Task views: Hangi view'lar en önemli?
3. Notes: Folder sistemi mi yoksa sadece tags mi?

### Integrations:
1. Email: Gmail API mi yoksa IMAP mi?
2. Notifications: Hangi permissions gerekli?
3. Priority: Email mi önce yoksa notifications mi?

---

**Last Updated:** 2025-11-25 21:00 by Claude Code

**Next:** User clarifications + Agent task assignment

