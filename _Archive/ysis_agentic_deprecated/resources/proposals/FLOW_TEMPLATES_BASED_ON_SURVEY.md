# Flow Templates - Survey-Based Priority List

**Date:** 2025-12-02  
**Source:** User Survey Results (Turkish + English)  
**Total Respondents:** ~30 users  
**Primary Demographics:** 18-24 age, Students, Professionals

---

## 📊 Survey Analysis

### **Top User Needs (Frequency Analysis)**

1. **Task Reminders & Planning** (15+ mentions)
   - "Hatırlatma/alarm kurması"
   - "Günlük görevlerimi planlaması"
   - "İş önceliğine göre gün planlama"
   - "Remind me about tasks"
   - "Give me reminders"

2. **Daily Life Management** (10+ mentions)
   - "Günlük yaşantımda yapmam gerekenleri bana mesaj atmalı"
   - "Her anımı hatırlatmalı"
   - "Daily life tasks"
   - "Manage everything for me"

3. **Study & Learning Support** (8+ mentions)
   - "Özetleme" (summarization)
   - "Araştırma" (research)
   - "Derslere yardımcı"
   - "Study assistance"
   - "Summarize texts"

4. **Email & Communication** (5+ mentions)
   - "Mail kontrolü"
   - "Google Posta kutumu organize etmesi"
   - "Telefon görüşmesi hatırlatma"

5. **Budget & Finance** (3+ mentions)
   - "Bütçe özeti çıkarma"
   - "Elektrik su kullanımım nasıl yıllık faturaya yansiyacak onu hesaplasın"

6. **Translation** (2+ mentions)
   - "Farklı dillerde tercüme"
   - "Tercüme"

---

## 🎯 Priority Flow Templates (Survey-Based)

### **P0 - CRITICAL (Most Requested - 15+ votes)**

#### **1. Daily Task Reminder & Planning**
**User Quotes:**
- "Günlük görevlerimi planlaması ve bana hatırlatması"
- "İş önceliğine göre gün planlama yapması"
- "Remind me about tasks"
- "Give me reminders"

**Template Structure:**
```yaml
name: Daily Task Reminder & Planning
category: productivity
tags: [daily, planning, reminders, tasks]
variables:
  - name: reminder_time
    type: time
    label: "Reminder Time"
    default: "09:00"
  - name: include_priority_tasks
    type: boolean
    default: true
  - name: include_overdue_tasks
    type: boolean
    default: true

trigger:
  type: schedule
  schedule: "0 {{reminder_time_hour}} * * *" # Daily at user's preferred time

steps:
  - type: searchTasks
    params:
      status: "todo"
      priority: "high"
      due_date: "{{today}}"
  
  - type: createNote
    title: "📋 Daily Tasks - {{today}}"
    content: |
      ## Today's Priorities
      {{#if priority_tasks}}
      - {{priority_tasks}}
      {{/if}}
      
      ## Overdue Tasks
      {{#if overdue_tasks}}
      - {{overdue_tasks}}
      {{/if}}
      
  - type: sendNotification
    title: "📋 Daily Tasks Ready"
    body: "You have {{task_count}} tasks for today"
```

---

#### **2. Smart Daily Planning**
**User Quotes:**
- "Bana özel değiştirilebilir bir program yapması"
- "Durum değerlendirmesi yapması"
- "İş önceliğine göre gün planlama"

**Template Structure:**
```yaml
name: Smart Daily Planning
category: productivity
tags: [daily, planning, smart, personalized]
variables:
  - name: planning_time
    type: time
    default: "08:00"
  - name: work_hours_start
    type: time
    default: "09:00"
  - name: work_hours_end
    type: time
    default: "17:00"

trigger:
  type: schedule
  schedule: "0 {{planning_time_hour}} * * 1-5" # Weekdays

steps:
  - type: queryRAG
    query: "What are my priorities for today based on my notes and tasks?"
    limit: 5
  
  - type: searchTasks
    params:
      status: "todo"
      priority: ["high", "urgent"]
  
  - type: searchEvents
    params:
      start_date: "{{today}}"
      end_date: "{{today}}"
  
  - type: createNote
    title: "📅 Daily Plan - {{today}}"
    content: |
      ## Today's Schedule
      {{events_summary}}
      
      ## Priority Tasks
      {{priority_tasks}}
      
      ## Time Blocks
      - {{work_hours_start}}-12:00: Deep work
      - 12:00-13:00: Lunch
      - 13:00-{{work_hours_end}}: Meetings & tasks
      
  - type: sendNotification
    title: "📅 Daily Plan Ready"
    body: "Your personalized plan for {{today}} is ready!"
```

---

#### **3. Study Session Planner**
**User Quotes:**
- "Derslere yardımcı"
- "Study assistance"
- "Summarize texts"
- "Özetleme"

**Template Structure:**
```yaml
name: Study Session Planner
category: learning
tags: [study, learning, education, students]
variables:
  - name: study_subject
    type: string
    required: true
    label: "Study Subject"
  - name: study_duration
    type: number
    default: 90
    label: "Study Duration (minutes)"
  - name: include_break
    type: boolean
    default: true

trigger:
  type: manual

steps:
  - type: createNote
    title: "📚 Study Session - {{study_subject}}"
    content: |
      ## Study Plan: {{study_subject}}
      Duration: {{study_duration}} minutes
      Start: {{now}}
      
      ## Goals
      - [ ] Understand key concepts
      - [ ] Take notes
      - [ ] Review previous material
      
  - type: createTask
    title: "Complete {{study_subject}} study session"
    priority: "high"
    due_date: "{{today}}"
  
  {{#if include_break}}
  - type: delay
    duration: "{{study_duration / 2}}"
    unit: "minutes"
  
  - type: sendNotification
    title: "⏸️ Break Time!"
    body: "Take a 10-minute break"
  {{/if}}
  
  - type: delay
    duration: "{{study_duration}}"
    unit: "minutes"
  
  - type: sendNotification
    title: "✅ Study Session Complete"
    body: "Great work on {{study_subject}}!"
```

---

### **P1 - HIGH PRIORITY (8-14 votes)**

#### **4. Weekly Review & Planning**
**User Quotes:**
- "Haftalık rapor"
- "Weekly review"
- "Durum değerlendirmesi"

**Template Structure:**
```yaml
name: Weekly Review & Planning
category: productivity
tags: [weekly, review, planning, reflection]
variables:
  - name: review_day
    type: enum
    options: [sunday, monday]
    default: "sunday"
  - name: review_time
    type: time
    default: "18:00"

trigger:
  type: schedule
  schedule: "0 {{review_time_hour}} * * 0" # Sunday

steps:
  - type: searchTasks
    params:
      status: "done"
      created_at: "{{last_week_start}}"
  
  - type: searchNotes
    query: "weekly summary"
  
  - type: createNote
    title: "📊 Weekly Review - Week {{week_number}}"
    content: |
      ## Completed This Week
      {{completed_tasks_summary}}
      
      ## Achievements
      - [List achievements]
      
      ## Next Week's Goals
      - [ ] Goal 1
      - [ ] Goal 2
      
  - type: sendNotification
    title: "📊 Weekly Review Ready"
    body: "Time to reflect and plan!"
```

---

#### **5. Email Organization & Reminders**
**User Quotes:**
- "Mail kontrolü"
- "Google Posta kutumu organize etmesi"
- "Telefon görüşmesi hatırlatma"

**Template Structure:**
```yaml
name: Email Organization & Reminders
category: communication
tags: [email, organization, reminders]
variables:
  - name: check_frequency
    type: enum
    options: [daily, twice_daily, hourly]
    default: "twice_daily"
  - name: reminder_types
    type: multi_select
    options: [calls, meetings, deadlines, bills]
    default: [calls, meetings]

trigger:
  type: schedule
  schedule: "0 9,17 * * *" # 9 AM and 5 PM

steps:
  - type: createNote
    title: "📧 Email Check - {{now}}"
    content: |
      ## Email Summary
      Check your inbox for:
      - Important messages
      - Meeting requests
      - Deadlines
      
  - type: sendNotification
    title: "📧 Check Your Email"
    body: "You have new messages to review"
  
  {{#if reminder_types includes "calls"}}
  - type: createTask
    title: "Return important calls"
    priority: "medium"
  {{/if}}
```

---

#### **6. Budget & Expense Tracking**
**User Quotes:**
- "Bütçe özeti çıkarma"
- "Elektrik su kullanımım nasıl yıllık faturaya yansiyacak onu hesaplasın"

**Template Structure:**
```yaml
name: Budget & Expense Tracking
category: finance
tags: [budget, finance, expenses, tracking]
variables:
  - name: tracking_frequency
    type: enum
    options: [daily, weekly, monthly]
    default: "weekly"
  - name: budget_categories
    type: multi_select
    options: [utilities, food, transport, entertainment]
    default: [utilities, food]

trigger:
  type: schedule
  schedule: "0 20 * * 0" # Sunday 8 PM

steps:
  - type: createNote
    title: "💰 Weekly Budget Review - {{week_number}}"
    content: |
      ## Expenses This Week
      {{#each budget_categories}}
      - {{category}}: {{amount}}
      {{/each}}
      
      ## Projections
      - Monthly estimate: {{monthly_estimate}}
      - Yearly estimate: {{yearly_estimate}}
      
  - type: sendNotification
    title: "💰 Budget Review"
    body: "Your weekly expense summary is ready"
```

---

#### **7. Translation & Language Support**
**User Quotes:**
- "Farklı dillerde tercüme"
- "Tercüme"
- "Translation"

**Template Structure:**
```yaml
name: Translation Assistant
category: communication
tags: [translation, language, multilingual]
variables:
  - name: source_language
    type: enum
    options: [auto, tr, en, de, fr, es]
    default: "auto"
  - name: target_language
    type: enum
    options: [tr, en, de, fr, es]
    required: true
  - name: translation_type
    type: enum
    options: [text, document, note]
    default: "text"

trigger:
  type: manual

steps:
  - type: aiAction
    action: "translate"
    params:
      source: "{{source_language}}"
      target: "{{target_language}}"
      content: "{{user_input}}"
  
  - type: createNote
    title: "🌐 Translation - {{target_language}}"
    content: "{{translated_content}}"
  
  - type: sendNotification
    title: "🌐 Translation Complete"
    body: "Translated to {{target_language}}"
```

---

### **P2 - NICE TO HAVE (3-7 votes)**

#### **8. Morning Routine (Enhanced)**
**User Quotes:**
- "Morning routine"
- "Daily planning"

#### **9. Focus Mode (Enhanced)**
**User Quotes:**
- "Deep work"
- "Focus session"

#### **10. Health & Wellness Reminders**
**User Quotes:**
- "Water break reminder"
- "Health check-in"

---

## 🎨 Template Categories (Final Priority)

### **1. Productivity & Planning** (P0)
- ✅ Daily Task Reminder & Planning
- ✅ Smart Daily Planning
- ✅ Weekly Review & Planning
- Morning Routine
- Focus Mode

### **2. Learning & Education** (P0)
- ✅ Study Session Planner
- Document Summarization
- Research Assistant

### **3. Communication** (P1)
- ✅ Email Organization & Reminders
- ✅ Translation Assistant
- Call Reminders

### **4. Finance** (P1)
- ✅ Budget & Expense Tracking
- Bill Payment Reminders

### **5. Health & Wellness** (P2)
- Water Break Reminder
- Exercise Reminder
- Sleep Preparation

---

## 🔧 Implementation Priority

### **Phase 1: MVP (Closed Beta)**
1. Daily Task Reminder & Planning
2. Smart Daily Planning
3. Study Session Planner
4. Weekly Review & Planning

### **Phase 2: Enhanced (Post-Beta)**
5. Email Organization & Reminders
6. Budget & Expense Tracking
7. Translation Assistant

### **Phase 3: Advanced**
8. Health & Wellness
9. Advanced automation
10. AI-powered suggestions

---

## 💡 Key Insights from Survey

1. **Reminders are #1 priority** - Users want proactive notifications
2. **Personalization is critical** - "Bana özel değiştirilebilir"
3. **Daily planning is essential** - Most requested feature
4. **Students need study support** - Large user base
5. **Multi-language support** - Translation needed
6. **Email management** - Organization and reminders
7. **Budget tracking** - Financial awareness

---

**Next Steps:**
1. Implement P0 templates (4 templates)
2. Add reminder/notification system
3. Add variable customization UI
4. Test with beta users
5. Iterate based on feedback




