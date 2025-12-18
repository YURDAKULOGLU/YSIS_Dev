# Generic Flow Templates - Post-Survey Design

**Date:** 2025-12-02
**Status:** Ready for Implementation
**Context:** Survey results showed student bias. Redesigned templates to be universal and flexible.
**Source:** User Survey Analysis + Generic Design Principles

---

## 🎯 Design Philosophy Shift

### ❌ **Old Approach (Student-Biased)**
```
❌ Sınav Hazırlık Asistanı
❌ Ödev Takip
❌ Ders Özeti Çıkarıcı
❌ İlaç Hatırlatıcı
❌ Fatura Takip
```
→ **Problem:** Too specific, unsustainable, creates template explosion

### ✅ **New Approach (Universal & Flexible)**
```
✅ Smart Reminder & Task Manager (works for: exams, medication, bills, anything)
✅ Time Block Scheduler (works for: study, meetings, exercise, anything)
✅ Content Processor (works for: notes, PDFs, articles, anything)
✅ Periodic Review & Analysis (works for: tasks, habits, budget, anything)
✅ Proactive Assistant (context-aware for any domain)
```
→ **Solution:** Generic templates + customizable parameters = infinite use cases

---

## 📊 Survey Insights (De-biased)

### **Top User Needs (Universal)**
1. **Reminders & Planning** (15+ mentions) → Universal Reminder System
2. **Daily Life Management** (10+ mentions) → Time Block Scheduler
3. **Summarization & Learning** (8+ mentions) → Content Processor
4. **Proactive Support** (mentioned repeatedly) → Proactive Assistant
5. **Analysis & Insights** (implicit in many requests) → Periodic Review

### **Key Requirements**
- ⭐ **Flexibility:** "Bana özel değiştirilebilir"
- ⭐ **Context-Awareness:** "Geçmişten öğrensin" (RAG)
- ⭐ **Proactivity:** Reactive değil, proactive
- ⭐ **Multi-domain:** Students, professionals, everyone

---

## 🎨 Core Generic Templates

### **1. Smart Reminder & Task Manager** ⭐⭐⭐⭐⭐
**Universal Use:** Any recurring activity (medication, homework, bills, workouts, anything)

```yaml
name: Smart Reminder & Task Manager
description: |
  Universal reminder system that works for ANY recurring activity.
  AI learns your patterns and optimizes reminder timing.
category: universal
flexibility: ⭐⭐⭐⭐⭐
rag_powered: true

variables:
  activity_type:
    type: enum
    options: [task, medication, bill, exercise, study, meeting, custom]
    label: "What do you want to track?"
    description: "Choose the type of activity"

  activity_name:
    type: string
    required: true
    label: "Activity Name"
    placeholder: "e.g., 'Take medication', 'Pay rent', 'Study math'"

  frequency:
    type: enum
    options: [daily, weekly, biweekly, monthly, custom]
    label: "How often?"
    default: "daily"

  custom_schedule:
    type: string
    label: "Custom Schedule (cron format)"
    description: "For advanced users: cron expression"
    condition: "frequency == 'custom'"

  time:
    type: time
    label: "Reminder Time"
    default: "09:00"
    description: "When to be reminded"

  remind_before:
    type: enum
    options: ["15min", "1hour", "1day", "2days", "1week"]
    label: "Remind me before"
    default: "1hour"
    multiple: true

  enable_rag:
    type: boolean
    label: "Learn from my behavior?"
    default: true
    description: "AI will analyze when you usually complete this activity"

  auto_reschedule:
    type: boolean
    label: "Auto-reschedule if I miss it?"
    default: false
    description: "Automatically suggest new time if you miss the reminder"

trigger:
  type: schedule
  schedule: "{{frequency}}"
  time: "{{time}}"

steps:
  - id: "analyze_patterns"
    type: queryRAG
    condition: "{{enable_rag}}"
    query: "Analyze user's pattern for activity: {{activity_name}}"
    output: "behavioral_insights"

  - id: "create_task"
    type: createTask
    params:
      title: "{{activity_name}}"
      priority: "{{activity_type == 'medication' ? 'urgent' : 'medium'}}"
      due_date: "{{next_occurrence}}"
      metadata:
        activity_type: "{{activity_type}}"
        schedule: "{{frequency}}"

  - id: "send_notification"
    type: sendNotification
    title: "⏰ {{activity_name}}"
    body: |
      {{remind_before}} remaining
      {{#if behavioral_insights}}
      💡 You usually complete this at {{behavioral_insights.preferred_time}}
      {{/if}}

  - id: "reschedule_if_missed"
    type: conditionalAction
    condition: "{{auto_reschedule && task_not_completed}}"
    action:
      type: queryRAG
      query: "Suggest optimal reschedule time for {{activity_name}}"
      then:
        - type: updateTask
          params:
            id: "{{task_id}}"
            due_date: "{{suggested_time}}"
        - type: sendNotification
          title: "⏰ Rescheduled: {{activity_name}}"
          body: "Moved to {{suggested_time}} based on your patterns"

metadata:
  author: "ybis"
  category: "universal"
  tags: ["reminder", "task", "flexible", "rag"]
  use_cases:
    - "💊 Medication: 'İlaç al' daily at 08:00"
    - "📚 Study: 'Matematik çalış' weekdays at 15:00"
    - "💰 Bills: 'Kira öde' monthly on 1st"
    - "🏋️ Exercise: 'Gym' MWF at 18:00"
    - "📞 Social: 'Annem ara' weekly on Sunday"
```

---

### **2. Time Block Scheduler** ⭐⭐⭐⭐⭐
**Universal Use:** Schedule any activity in calendar (study, meetings, workouts, personal time)

```yaml
name: Time Block Scheduler
description: |
  AI-powered time blocking for ANY activity.
  Automatically finds optimal time slots based on your calendar and patterns.
category: universal
flexibility: ⭐⭐⭐⭐⭐
rag_powered: true

variables:
  block_type:
    type: enum
    options: [deep_work, meeting, study, exercise, personal, creative, admin, custom]
    label: "Activity Type"

  block_name:
    type: string
    required: true
    label: "Activity Name"
    placeholder: "e.g., 'Deep work', 'Gym', 'Team standup'"

  duration:
    type: number
    label: "Duration (minutes)"
    default: 60
    validation:
      min: 15
      max: 480

  preferred_time:
    type: enum
    options: [morning, afternoon, evening, flexible, specific]
    label: "Preferred Time"
    default: "flexible"

  specific_time:
    type: time
    label: "Specific Time"
    condition: "preferred_time == 'specific'"

  frequency:
    type: enum
    options: [once, daily, MWF, TTh, weekdays, weekends, custom]
    label: "How often?"
    default: "once"

  auto_reschedule_on_conflict:
    type: boolean
    label: "Auto-reschedule if conflict?"
    default: true

  buffer_before:
    type: number
    label: "Buffer before (minutes)"
    default: 0
    description: "Add empty time before activity"

  buffer_after:
    type: number
    label: "Buffer after (minutes)"
    default: 0

  enable_ai_optimization:
    type: boolean
    label: "Let AI find optimal time?"
    default: true
    description: "AI analyzes when you're most productive for this activity"

trigger:
  type: schedule
  schedule: "0 8 * * *"  # Daily at 8 AM
  description: "Runs every morning to plan the day"

steps:
  - id: "get_calendar"
    type: getCalendarEvents
    params:
      date: "{{today}}"

  - id: "analyze_productivity"
    type: queryRAG
    condition: "{{enable_ai_optimization}}"
    query: |
      When is user most productive for {{block_type}}?
      Consider: past performance, energy levels, context
    output: "optimal_time_slot"

  - id: "find_slot"
    type: aiDecision
    prompt: |
      Find optimal time slot for:
      - Activity: {{block_name}} ({{duration}} min)
      - Type: {{block_type}}
      - Preference: {{preferred_time}}
      - AI suggestion: {{optimal_time_slot}}
      - Existing events: {{calendar_events}}
      - Buffers: {{buffer_before}}min before, {{buffer_after}}min after

  - id: "create_event"
    type: createCalendarEvent
    params:
      title: "{{block_name}}"
      start_time: "{{calculated_start_time}}"
      end_time: "{{calculated_end_time}}"
      category: "{{block_type}}"
      description: |
        Duration: {{duration}} minutes
        {{#if optimal_time_slot}}
        💡 AI-optimized timing based on your patterns
        {{/if}}

  - id: "create_prep_task"
    type: createTask
    condition: "{{buffer_before > 0}}"
    params:
      title: "Prep: {{block_name}}"
      due_date: "{{start_time_minus_buffer}}"
      priority: "medium"

  - id: "notify"
    type: sendNotification
    title: "📅 Scheduled: {{block_name}}"
    body: |
      {{calculated_start_time}} - {{calculated_end_time}} ({{duration}} min)
      {{#if optimal_time_slot}}
      💡 Best time based on your productivity patterns
      {{/if}}

metadata:
  use_cases:
    - "📚 Student: 'Fizik çalış' 2h, afternoon, MWF"
    - "💼 Professional: 'Deep work' 3h, morning, daily"
    - "🏋️ Fitness: 'Gym' 1h, evening, MTWTh"
    - "👥 Manager: 'Team standup' 15min, 10:00, daily"
    - "🎨 Creative: 'Design work' 2h, morning, flexible"
```

---

### **3. Content Processor** ⭐⭐⭐⭐⭐
**Universal Use:** Process any content (PDFs, notes, articles, recordings)

```yaml
name: Content Processor
description: |
  Universal content processing system.
  Summarize, extract, analyze, translate ANY content.
category: universal
flexibility: ⭐⭐⭐⭐⭐
rag_powered: true

variables:
  content_source:
    type: enum
    options: [note, pdf, webpage, text, voice_recording, image]
    label: "Content Type"

  content_input:
    type: text
    label: "Content or URL"
    description: "Paste text, URL, or upload file"

  processing_actions:
    type: multi_select
    options:
      - summarize
      - extract_tasks
      - create_flashcards
      - translate
      - analyze_sentiment
      - extract_key_points
      - generate_questions
      - find_action_items
    label: "What to do with content?"
    default: ["summarize"]

  output_format:
    type: enum
    options: [note, task_list, flashcards, bullet_points, markdown, structured]
    label: "Output Format"
    default: "note"

  target_language:
    type: enum
    options: [auto, tr, en, de, fr, es, ar]
    label: "Target Language (for translation)"
    default: "auto"

  detail_level:
    type: enum
    options: [brief, moderate, detailed]
    label: "Summary Detail Level"
    default: "moderate"

  enable_context_search:
    type: boolean
    label: "Search for related content?"
    default: true
    description: "Use RAG to find related notes/documents"

trigger:
  type: manual

steps:
  - id: "search_context"
    type: queryRAG
    condition: "{{enable_context_search}}"
    query: "Find related content to: {{content_title or first_100_chars}}"
    output: "related_content"

  - id: "process_content"
    type: aiAction
    action: "{{processing_actions}}"
    params:
      content: "{{content_input}}"
      format: "{{output_format}}"
      detail: "{{detail_level}}"
      language: "{{target_language}}"
      context: "{{related_content}}"

  - id: "create_output_note"
    type: createNote
    condition: "{{output_format == 'note' || output_format == 'markdown'}}"
    params:
      title: "📄 {{processing_actions[0]}} - {{content_title}}"
      content: |
        ## Source
        Type: {{content_source}}
        Processed: {{now}}

        {{#if related_content}}
        ## Related Content
        {{related_content}}
        {{/if}}

        ## Processed Output
        {{processed_content}}

  - id: "create_tasks"
    type: createTasks
    condition: "{{processing_actions includes 'extract_tasks' || processing_actions includes 'find_action_items'}}"
    params:
      tasks: "{{extracted_tasks}}"

  - id: "create_flashcards"
    type: createNotes
    condition: "{{processing_actions includes 'create_flashcards'}}"
    params:
      notes: "{{flashcards}}"
      tag: "flashcard"

  - id: "notify"
    type: sendNotification
    title: "✅ Content Processed"
    body: "{{processing_actions.length}} actions completed"

metadata:
  use_cases:
    - "📚 Student: PDF → Summary + Flashcards"
    - "💼 Professional: Meeting notes → Task list"
    - "📰 Researcher: Article → Translation + Key points"
    - "🎓 Learner: Video transcript → Q&A"
    - "📝 Writer: Draft → Sentiment analysis"
```

---

### **4. Periodic Review & Analysis** ⭐⭐⭐⭐⭐
**Universal Use:** Review any aspect of life (tasks, habits, budget, health, learning)

```yaml
name: Periodic Review & Analysis
description: |
  Universal review system that analyzes ANY aspect of your life.
  AI identifies patterns, trends, and provides actionable insights.
category: universal
flexibility: ⭐⭐⭐⭐⭐
rag_powered: true

variables:
  review_area:
    type: enum
    options: [tasks, habits, budget, health, learning, relationships, work, custom]
    label: "What to review?"

  custom_area:
    type: string
    label: "Custom Review Area"
    condition: "review_area == 'custom'"

  review_frequency:
    type: enum
    options: [daily, weekly, biweekly, monthly, quarterly, yearly]
    label: "Review Frequency"
    default: "weekly"

  metrics_to_track:
    type: multi_select
    options:
      - completion_rate
      - time_spent
      - patterns
      - trends
      - anomalies
      - progress_vs_goals
      - strengths
      - weaknesses
    label: "What metrics to track?"
    default: ["completion_rate", "patterns", "trends"]

  comparison_period:
    type: enum
    options: [previous_period, last_month, last_quarter, last_year]
    label: "Compare with?"
    default: "previous_period"

  enable_ai_insights:
    type: boolean
    label: "Generate AI insights?"
    default: true

  enable_recommendations:
    type: boolean
    label: "Get improvement recommendations?"
    default: true

  detail_level:
    type: enum
    options: [summary, moderate, comprehensive]
    default: "moderate"

trigger:
  type: schedule
  schedule: "{{review_frequency}}"

steps:
  - id: "collect_data"
    type: queryRAG
    query: |
      Analyze {{review_area}} for period: {{period}}
      Metrics: {{metrics_to_track}}
      Compare with: {{comparison_period}}
    output: "analysis_data"

  - id: "generate_insights"
    type: aiAction
    condition: "{{enable_ai_insights}}"
    action: "analyze"
    params:
      data: "{{analysis_data}}"
      focus: "{{metrics_to_track}}"
      depth: "{{detail_level}}"
    output: "insights"

  - id: "generate_recommendations"
    type: aiAction
    condition: "{{enable_recommendations}}"
    action: "recommend"
    params:
      insights: "{{insights}}"
      area: "{{review_area}}"
    output: "recommendations"

  - id: "create_review_note"
    type: createNote
    params:
      title: "📊 {{review_area}} Review - {{period}}"
      content: |
        # {{review_area}} Review
        **Period:** {{period}}
        **Generated:** {{now}}

        ## Summary Statistics
        {{statistics}}

        {{#if comparison_period}}
        ## Comparison with {{comparison_period}}
        {{comparison_data}}
        {{/if}}

        ## Key Insights ⭐
        {{insights}}

        ## Patterns Detected
        {{patterns}}

        {{#if anomalies}}
        ## ⚠️ Anomalies
        {{anomalies}}
        {{/if}}

        {{#if recommendations}}
        ## 💡 Recommendations
        {{recommendations}}
        {{/if}}

        ## Next Period Goals
        {{suggested_goals}}

  - id: "create_follow_up_tasks"
    type: createTasks
    condition: "{{recommendations.length > 0}}"
    params:
      tasks: "{{recommendations_as_tasks}}"

  - id: "notify"
    type: sendNotification
    title: "📊 {{review_area}} Review Ready"
    body: |
      {{period}} review complete
      {{insights.count}} insights • {{recommendations.count}} recommendations

metadata:
  use_cases:
    - "📚 Student: 'Çalışma' weekly → 'Cumartesi %80 başarısız'"
    - "💼 Professional: 'Tasks' weekly → 'En verimli gün Salı'"
    - "💰 Finance: 'Budget' monthly → 'Kafe harcaması %40 arttı'"
    - "🏋️ Health: 'Exercise' weekly → 'Consistency improving'"
    - "📖 Learning: 'Reading' monthly → '5 books completed'"
```

---

### **5. Proactive Assistant** ⭐⭐⭐⭐⭐
**Universal Use:** Context-aware proactive suggestions for anything

```yaml
name: Proactive Assistant
description: |
  AI continuously monitors your context and proactively suggests actions.
  Works across all domains: work, study, health, relationships, etc.
category: advanced
flexibility: ⭐⭐⭐⭐⭐
rag_powered: true

variables:
  monitoring_areas:
    type: multi_select
    options:
      - calendar
      - tasks
      - notes
      - habits
      - weather
      - location
      - time_of_day
      - energy_level
    label: "What to monitor?"
    default: ["calendar", "tasks"]

  notification_style:
    type: enum
    options: [minimal, moderate, verbose]
    label: "Notification Style"
    default: "moderate"

  proactive_level:
    type: enum
    options: [suggestions_only, auto_create_tasks, full_automation]
    label: "Proactivity Level"
    default: "suggestions_only"
    description: |
      - suggestions_only: Just notify
      - auto_create_tasks: Create tasks automatically
      - full_automation: Take actions automatically

  quiet_hours:
    type: time_range
    label: "Quiet Hours (no notifications)"
    default: "22:00-08:00"

  context_window:
    type: enum
    options: ["1hour", "4hours", "1day", "3days", "1week"]
    label: "How far ahead to look?"
    default: "1day"

trigger:
  type: continuous
  check_interval: "1 hour"
  description: "Runs in background continuously"

steps:
  - id: "analyze_context"
    type: queryRAG
    query: |
      Analyze current context:
      Areas: {{monitoring_areas}}
      Window: {{context_window}}

      Check:
      - Upcoming events (calendar)
      - Overdue/urgent tasks
      - Behavioral patterns
      - External factors (weather, time, etc.)
    output: "context_analysis"

  - id: "make_decision"
    type: aiDecision
    prompt: |
      Based on context analysis: {{context_analysis}}

      Should I:
      1. Create a reminder?
      2. Reschedule something?
      3. Suggest a task?
      4. Just notify?
      5. Do nothing?

      Consider:
      - User's current state
      - Priority levels
      - Quiet hours
      - Past reactions to suggestions
    output: "decision"

  - id: "take_action"
    type: conditionalAction
    condition: "{{decision != 'do_nothing'}}"
    actions:
      - type: createTask
        condition: "{{proactive_level includes 'auto_create' && decision == 'create_task'}}"
        params:
          title: "{{suggested_task}}"
          priority: "{{calculated_priority}}"

      - type: rescheduleEvent
        condition: "{{proactive_level == 'full_automation' && decision == 'reschedule'}}"
        params:
          event_id: "{{event_to_reschedule}}"
          new_time: "{{suggested_time}}"

      - type: sendNotification
        params:
          title: "{{notification_title}}"
          body: "{{notification_body}}"
          style: "{{notification_style}}"

metadata:
  use_cases:
    - "📅 'Yarın toplantı var, hazırlık yaptın mı?'"
    - "🏃 '2 gündür hareketsizsin, yürüyüş yapalım mı?'"
    - "📚 'Bu ödev 3 gün gecikmiş, bugün bitirmeliyiz'"
    - "☕ 'Her salı 14:00'te kahve molası veriyorsun'"
    - "💤 'Yorgun görünüyorsun, bugün hafif plan yapalım?'"
```

---

## 📋 Template Comparison

| Template | Flexibility | RAG | Use Cases | Complexity |
|----------|-------------|-----|-----------|------------|
| **Smart Reminder** | ⭐⭐⭐⭐⭐ | Yes | Medication, homework, bills, workouts | Low |
| **Time Block** | ⭐⭐⭐⭐⭐ | Yes | Study, meetings, exercise, deep work | Medium |
| **Content Processor** | ⭐⭐⭐⭐⭐ | Yes | PDFs, articles, notes, recordings | Medium |
| **Periodic Review** | ⭐⭐⭐⭐⭐ | Yes | Tasks, habits, budget, health | Medium |
| **Proactive Assistant** | ⭐⭐⭐⭐⭐ | Yes | Everything (context-aware) | High |

---

## 🎯 Implementation Priority

### **Phase 1: MVP (Essential)**
1. **Smart Reminder & Task Manager** - Most requested feature
2. **Time Block Scheduler** - Calendar integration complete
3. **Content Processor** - RAG integration needed

### **Phase 2: Enhanced**
4. **Periodic Review & Analysis** - Requires data collection
5. **Proactive Assistant** - Most complex, requires all above

---

## 💡 Key Design Principles

1. **ONE template, INFINITE use cases** - Parameters create variations
2. **RAG by default** - All templates learn from user behavior
3. **Progressive disclosure** - Simple by default, advanced if needed
4. **AI-first** - Natural language → Flow creation
5. **No domain lock-in** - Students, professionals, everyone

---

## 🔄 Migration from Survey Templates

### Old (Specific) → New (Generic)

| Survey Template | Generic Template | How |
|----------------|------------------|-----|
| Daily Task Reminder | Smart Reminder | `activity_type: task` |
| Study Session Planner | Time Block Scheduler | `block_type: study` |
| Email Organization | Smart Reminder | `activity_type: custom, "Check email"` |
| Budget Tracking | Periodic Review | `review_area: budget` |
| Translation Assistant | Content Processor | `processing_actions: translate` |
| Weekly Review | Periodic Review | `review_area: tasks, frequency: weekly` |

**Result:** 7 specific templates → 5 generic templates with more flexibility

---

## 📝 Next Steps

1. ✅ Document generic template design
2. ⏳ Implement template variable system
3. ⏳ Add RAG integration to all templates
4. ⏳ Create template preview UI
5. ⏳ Add AI flow creation tool (`createFlow`)
6. ⏳ User testing with generic templates

---

**Status:** Ready for implementation. Generic templates provide maximum flexibility while maintaining simplicity.
