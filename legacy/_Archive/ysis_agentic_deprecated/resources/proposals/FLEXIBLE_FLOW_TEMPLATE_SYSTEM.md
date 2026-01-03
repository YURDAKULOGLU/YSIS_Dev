# Flexible Flow Template System - Design Proposal

**Date:** 2025-12-02
**Status:** Proposal - Awaiting User Feedback
**Context:** User wants "aşırı flexible" flow template system that can handle diverse user needs

---

## 🎯 Core Philosophy

> **"Templates should be starting points, not limitations"**

Users should be able to:
- Start from templates but customize everything
- Create flows via natural language (AI)
- Combine multiple templates
- Share and discover templates
- Use templates as "recipes" they can modify

---

## 📋 Template Categories (Flexible Organization)

Instead of fixed 5 templates, organize by **use cases** and **user personas**:

### **1. Productivity & Planning**
- Morning Routine (8 AM daily)
- Daily Planning (9 AM weekdays)
- Weekly Review (Sunday 6 PM)
- End-of-Day Reflection (6 PM daily)
- Monthly Goals (1st of month)

### **2. Project Management**
- Project Kickoff (manual with variables)
- Sprint Planning (bi-weekly)
- Project Retrospective (end of sprint)
- Milestone Celebration (on milestone completion)

### **3. Health & Wellness**
- Morning Workout Reminder (6 AM weekdays)
- Water Break Reminder (every 2 hours)
- Meditation Session (8 PM daily)
- Sleep Preparation (10 PM daily)
- Weekly Health Check-in (Sunday 9 AM)

### **4. Learning & Growth**
- Daily Learning Goal (9 AM daily)
- Weekly Skill Review (Saturday 10 AM)
- Book Reading Session (7 PM daily)
- Course Progress Check (Monday 8 AM)

### **5. Social & Relationships**
- Weekly Family Call (Sunday 4 PM)
- Friend Check-in (bi-weekly)
- Birthday Reminder (1 day before)
- Relationship Appreciation (Friday 6 PM)

### **6. Finance & Budget**
- Weekly Expense Review (Sunday 7 PM)
- Monthly Budget Planning (1st of month)
- Bill Payment Reminder (3 days before due)
- Savings Goal Check (monthly)

### **7. Creative & Hobbies**
- Daily Writing Session (7 AM daily)
- Weekly Creative Project (Saturday 2 PM)
- Photo Organization (monthly)
- Music Practice (daily, customizable time)

### **8. Work & Career**
- Daily Standup Prep (9 AM weekdays)
- Weekly Team Sync (Monday 10 AM)
- Performance Review Prep (quarterly)
- Skill Development (weekly)

---

## 🔧 Flexible Template System Architecture

### **Template Structure (Enhanced)**

```typescript
interface FlowTemplate {
  id: string;
  name: string;
  description: string;
  category: string; // 'productivity' | 'health' | 'work' | 'personal' | etc.
  tags: string[]; // ['morning', 'planning', 'automation']
  icon: string; // emoji or icon name

  // Flexible configuration
  config: {
    trigger: {
      type: 'manual' | 'schedule' | 'event' | 'ai_suggested';
      schedule?: string; // cron expression
      event?: string; // future: 'task_completed', 'note_created', etc.
    };

    // Variable inputs (user can customize)
    variables: Array<{
      name: string; // 'project_name', 'workout_duration', etc.
      type: 'string' | 'number' | 'date' | 'time' | 'enum';
      label: string; // User-friendly label
      description: string;
      required: boolean;
      default?: unknown;
      options?: string[]; // for enum type
      validation?: {
        min?: number;
        max?: number;
        pattern?: string;
      };
    }>;

    steps: FlowStep[];

    // Conditional logic (future)
    conditions?: Array<{
      if: string; // '{{task_count}} > 5'
      then: string[]; // step IDs to execute
      else?: string[]; // step IDs if condition false
    }>;
  };

  // Metadata
  author?: string; // 'ybis' | 'community' | user_id
  popularity?: number; // usage count
  rating?: number; // user ratings
  usage_count?: number;

  // AI Integration
  ai_prompts?: {
    creation: string; // "Create a flow for {{user_input}}"
    customization: string; // "Modify this flow to {{user_request}}"
  };
}
```

### **Template Variables System**

Templates should support rich variable substitution:

```typescript
// Built-in variables (always available)
const BUILT_IN_VARIABLES = {
  '{{today}}': () => new Date().toISOString().split('T')[0],
  '{{now}}': () => new Date().toISOString(),
  '{{week_number}}': () => getWeekNumber(new Date()),
  '{{user.name}}': (context) => context.user?.name,
  '{{workspace.name}}': (context) => context.workspace?.name,
  '{{time}}': () => new Date().toLocaleTimeString('tr-TR'),
  '{{date}}': () => new Date().toLocaleDateString('tr-TR'),
  '{{day_of_week}}': () => ['Pazar', 'Pazartesi', ...][new Date().getDay()],
  '{{month_name}}': () => ['Ocak', 'Şubat', ...][new Date().getMonth()],
};

// User-provided variables (from template.variables)
// Example: {{project_name}}, {{workout_duration}}, {{meeting_time}}
```

### **AI-Powered Flow Creation**

Users should be able to create flows via natural language:

```
User: "Her pazartesi sabah 10'da haftalık rapor oluştur"
AI: Recognizes intent → Finds/clones "Weekly Review" template →
    Adjusts schedule to Monday 10 AM → Creates flow → Confirms
```

**Implementation:**
- Add `proposeFlowCreation` AI tool
- AI analyzes user intent
- Matches to existing template or creates new
- Fills in variables from conversation
- Confirms with user before creating

---

## 🎨 Template Examples (Flexible & Customizable)

### **Example 1: Morning Routine (Highly Customizable)**

```yaml
name: Morning Routine
category: productivity
tags: [morning, routine, planning]
variables:
  - name: wake_up_time
    type: time
    label: "Wake Up Time"
    default: "08:00"
  - name: include_workout
    type: enum
    options: [yes, no]
    default: "no"
  - name: workout_duration
    type: number
    label: "Workout Duration (minutes)"
    default: 30
    condition: include_workout == "yes"

steps:
  - type: createNote
    title: "🌅 Morning Brief - {{today}}"
    content: |
      Good morning! Today is {{day_of_week}}.
      Wake up time: {{wake_up_time}}

      {{#if include_workout}}
      Workout planned: {{workout_duration}} minutes
      {{/if}}

      Today's priorities:
      - [ ] Top priority task
      - [ ] Second priority

  - type: createTask
    title: "Morning routine completed"
    priority: "low"

  {{#if include_workout}}
  - type: sendNotification
    title: "Workout Time!"
    body: "Time for {{workout_duration}} minute workout"
    delay: "{{wake_up_time}}"
  {{/if}}
```

### **Example 2: Project Kickoff (Variable-Rich)**

```yaml
name: Project Kickoff
category: project_management
tags: [project, setup, planning]
variables:
  - name: project_name
    type: string
    required: true
    label: "Project Name"
  - name: deadline
    type: date
    label: "Deadline"
  - name: team_size
    type: number
    label: "Team Size"
    default: 1
  - name: priority
    type: enum
    options: [low, medium, high, urgent]
    default: "medium"

steps:
  - type: createNote
    title: "📁 {{project_name}} - Project Plan"
    content: |
      ## Project: {{project_name}}
      Deadline: {{deadline}}
      Team Size: {{team_size}}
      Priority: {{priority}}

      ## Phases
      1. Planning
      2. Execution
      3. Review

  - type: createTask
    title: "Define {{project_name}} requirements"
    priority: "{{priority}}"

  - type: createTask
    title: "Create {{project_name}} timeline"
    priority: "medium"

  {{#if team_size > 1}}
  - type: createCalendarEvent
    title: "{{project_name}} - Team Kickoff Meeting"
    date: "{{today}}"
    start_time: "10:00"
    end_time: "11:00"
  {{/if}}
```

### **Example 3: Focus Mode (Time-Based)**

```yaml
name: Focus Mode
category: productivity
tags: [focus, deep-work, pomodoro]
variables:
  - name: duration
    type: number
    label: "Focus Duration (minutes)"
    default: 90
    validation:
      min: 15
      max: 240
  - name: focus_goal
    type: string
    label: "What are you focusing on?"
    default: "Deep work session"

steps:
  - type: sendNotification
    title: "Focus Mode Activated"
    body: "{{duration}} minute focus session starting"

  - type: createNote
    title: "🎯 Focus Session - {{now}}"
    content: |
      ## Focus Goal
      {{focus_goal}}

      Duration: {{duration}} minutes
      Start: {{now}}
      End: {{end_time}} (calculated)

  - type: delay
    duration: "{{duration}}"
    unit: "minutes"

  - type: sendNotification
    title: "Focus Mode Ended"
    body: "Great work! Time for a break."

  - type: createNote
    title: "✅ Focus Session Complete"
    content: |
      Completed: {{focus_goal}}
      Duration: {{duration}} minutes
      Completed at: {{now}}
```

---

## 🤖 AI Integration Strategy

### **1. Natural Language Flow Creation**

**User Input Examples:**
- "Her pazartesi 10'da haftalık rapor"
- "Her gün sabah 8'de workout hatırlatması"
- "Proje başladığında otomatik not oluştur"
- "Her ayın 1'inde bütçe planlaması yap"

**AI Processing:**
1. Intent recognition (schedule, action, variables)
2. Template matching (find closest template)
3. Variable extraction (time, frequency, etc.)
4. Flow creation with confirmation

### **2. Template Suggestion System**

AI can suggest templates based on:
- User behavior patterns
- Time of day/week
- Current tasks/notes
- User goals

**Example:**
```
AI: "I noticed you create daily planning notes every morning.
     Would you like me to set up an automated 'Daily Planning' flow?"
```

### **3. Flow Customization via Chat**

Users can modify flows via conversation:
```
User: "Morning routine'a workout ekle, 30 dakika"
AI: Updates flow → Adds workout step → Confirms
```

---

## 📊 Template Discovery & Organization

### **Template Gallery UI**

```
┌─────────────────────────────────────┐
│  Flow Templates                     │
├─────────────────────────────────────┤
│  [Search: "morning routine"]        │
│  [Categories: All ▼]                │
│  [Sort: Popular ▼]                   │
├─────────────────────────────────────┤
│  🌅 Morning Routine                 │
│  Productivity • 1.2k uses           │
│  Creates daily planning note...      │
│  [Preview] [Use Template]            │
├─────────────────────────────────────┤
│  🏋️ Workout Reminder                │
│  Health • 856 uses                  │
│  Sends workout notifications...     │
│  [Preview] [Use Template]           │
└─────────────────────────────────────┘
```

### **Template Features**

- **Preview:** See what the flow does before using
- **Customize:** Adjust variables before creating
- **Clone & Edit:** Start from template, modify freely
- **Share:** Share custom templates (future)
- **Rate:** Rate templates for quality

---

## 🎯 Recommended Initial Template Set (Flexible)

Based on common productivity needs, start with **10-15 templates** across categories:

### **Must-Have (P0):**
1. **Morning Routine** - Customizable wake time, workout option
2. **Daily Planning** - Weekday schedule, customizable priorities
3. **Weekly Review** - Sunday evening, customizable time
4. **Project Kickoff** - Manual, rich variables
5. **Focus Mode** - Manual, customizable duration

### **High-Value (P1):**
6. **End-of-Day Reflection** - Daily 6 PM
7. **Weekly Health Check-in** - Sunday morning
8. **Monthly Goals** - 1st of month
9. **Bill Payment Reminder** - 3 days before (variable)
10. **Daily Learning** - Customizable time

### **Nice-to-Have (P2):**
11. **Workout Reminder** - Customizable schedule
12. **Water Break Reminder** - Every 2 hours
13. **Family Check-in** - Weekly/bi-weekly
14. **Expense Review** - Weekly
15. **Creative Session** - Customizable

---

## 🔄 Template Evolution Path

### **Phase 1: Closed Beta (Current)**
- 10-15 pre-built templates
- Basic variables (time, date, string)
- Manual + Scheduled triggers
- AI can suggest templates

### **Phase 2: Open Beta**
- User-created templates
- Template marketplace
- Template sharing
- Advanced variables (conditions, loops)

### **Phase 3: MVP**
- Visual flow builder
- Conditional logic
- Event-based triggers
- Template analytics

---

## 💡 Key Flexibility Features

1. **Variable System:** Every template should have customizable variables
2. **Step Composition:** Users can add/remove steps from templates
3. **AI Assistance:** Natural language flow creation
4. **Template Cloning:** Start from template, modify freely
5. **Category Organization:** Easy discovery by use case
6. **Tag System:** Multiple tags for better search
7. **Preview Mode:** See what flow does before activating

---

## 📝 Next Steps

1. **Wait for user survey results** - Understand real user needs
2. **Prioritize template categories** - Based on survey
3. **Design variable system** - Flexible input handling
4. **Implement AI flow creation** - Natural language → Flow
5. **Build template gallery** - Discovery and organization

---

**Awaiting:** User survey results to refine template priorities and categories.
