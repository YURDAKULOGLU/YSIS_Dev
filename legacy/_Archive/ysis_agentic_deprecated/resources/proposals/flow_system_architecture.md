# Architecture Proposal: Rule-Based Automation System (Observe-Classify-Act)

**Date:** 2025-11-30
**Author:** Antigravity (@Strategist)
**Task:** T-007

## 1. Overview

This document proposes the architecture for a rule-based automation system that extends the existing `FlowEngine`. The system follows the **Observe -> Classify -> Act** pattern to enable dynamic, event-driven workflows.

## 2. Core Components

### 2.1. The Observer (The Eye)
Responsible for capturing events from various sources and normalizing them into a standard `Event` object.

**Event Structure:**
```typescript
interface Event {
  id: string;
  source: 'database' | 'webhook' | 'time' | 'app';
  type: string; // e.g., 'INSERT', 'UPDATE', 'webhook_received'
  resource: string; // e.g., 'tasks', 'notes', 'stripe'
  payload: Record<string, any>;
  timestamp: string;
}
```

**Observer Types:**
1.  **Database Observer:** Uses Supabase Realtime to listen for changes in specific tables (`tasks`, `notes`, etc.).
2.  **Webhook Observer:** A dedicated Edge Function (`/api/webhooks/:source`) that accepts external payloads.
3.  **Time Observer:** The existing Cron/Scheduler system that generates 'tick' events.
4.  **App Observer:** Internal events triggered by the application logic (e.g., "User Logged In").

### 2.2. The Classifier (The Brain)
Responsible for evaluating if an observed `Event` matches a set of defined **Rules**.

**Rule Structure:**
```typescript
interface Rule {
  id: string;
  name: string;
  description?: string;
  trigger_source: string; // Filter by source
  trigger_resource: string; // Filter by resource
  conditions: ConditionGroup; // Logical evaluation
  action_flow_id: string; // Flow to execute if matched
  is_active: boolean;
}

interface ConditionGroup {
  operator: 'AND' | 'OR';
  conditions: (Condition | ConditionGroup)[];
}

interface Condition {
  field: string; // JSON path in payload, e.g., 'new.status'
  operator: 'equals' | 'not_equals' | 'contains' | 'gt' | 'lt';
  value: any;
}
```

**Classification Logic:**
1.  Observer emits an `Event`.
2.  Classifier fetches active `Rules` matching the event's `source` and `resource`.
3.  For each Rule, the `ConditionGroup` is evaluated against the `Event.payload`.
4.  If true, the Rule is considered a "Match".

### 2.3. The Actor (The Hand)
Responsible for executing the action defined in the matched Rule. In this architecture, the primary action is **triggering a Flow**.

**Execution Flow:**
1.  Classifier identifies a Match (Rule + Event).
2.  Actor creates a `FlowExecution` for the `action_flow_id`.
3.  **Context Injection:** The `Event.payload` is injected into the Flow's context as variables (e.g., `{{event.new.title}}`).
4.  The existing `FlowEngine` takes over to execute the steps.

## 3. Database Schema Extensions

To support this architecture, we need to introduce `rules` and `rule_conditions` tables (or a JSONB structure for conditions).

```sql
CREATE TABLE automation_rules (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  workspace_id UUID REFERENCES workspaces(id),
  name TEXT NOT NULL,
  trigger_source TEXT NOT NULL, -- 'database', 'webhook'
  trigger_resource TEXT NOT NULL, -- 'tasks', 'users'
  conditions JSONB DEFAULT '{}'::jsonb, -- Structured ConditionGroup
  action_flow_id UUID REFERENCES flows(id),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 4. Integration with Flow Engine

The `FlowEngine` needs to be updated to accept an initial `context` populated from the Event.

**FlowEngine.ts Update:**
```typescript
// Current
async executeFlow(flow: Flow, context: Record<string, unknown> = {}): Promise<FlowExecution>

// Usage by Actor
const eventContext = {
  event: {
    source: 'database',
    payload: { ... }
  }
};
await flowEngine.executeFlow(matchedRule.flow, eventContext);
```

## 5. Reliability & Observability

### 5.1. Error Handling & Retries
Automation is critical infrastructure; failures must be handled gracefully.
-   **Retry Policy:** Flows triggered by rules should have a configurable retry policy (e.g., exponential backoff, max 3 attempts).
-   **Dead Letter Queue:** Events that fail to process after retries should be logged to a `failed_events` table for manual inspection.
-   **Alerting:** Critical failures should trigger system alerts to workspace admins.

### 5.2. Execution Logs
We need a dedicated log to trace *why* a flow ran.
```sql
CREATE TABLE automation_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  rule_id UUID REFERENCES automation_rules(id),
  event_id TEXT, -- External ID if available
  flow_execution_id UUID REFERENCES flow_executions(id),
  status TEXT, -- 'success', 'failed', 'skipped'
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 6. Security & Permissions

### 6.1. Execution Context
When a Flow is triggered by an automation rule, it runs in a specific security context.
-   **System Context:** By default, automations run with "System" privileges but scoped to the `workspace_id`.
-   **User Impersonation:** (Future) Option to run "as the user who triggered the event" (if applicable).

### 6.2. Rate Limiting & Quotas
-   **Per-Workspace Limits:** Enforce limits on "Automations per month" based on the subscription plan.
-   **Loop Prevention:** Detect and block infinite loops (e.g., Flow A updates Task -> triggers Rule B -> triggers Flow A).

## 7. Implementation Phases

1.  **Phase 1: Foundation (Database Observer)**
    -   Implement `automation_rules` table.
    -   Implement `RuleEngine` logic.
    -   Set up Supabase Database Webhooks or Edge Function to listen to table changes and call the Rule Engine.

2.  **Phase 2: Context Injection**
    -   Update `FlowEngine` to support dynamic variables from context (e.g., `{{event.data.id}}`).

3.  **Phase 3: Advanced Triggers**
    -   Implement Webhook Observers for external integrations.

## 6. Security & Performance

-   **RLS:** Rules must be scoped to `workspace_id`.
-   **Performance:** Rule evaluation should happen in an Edge Function to minimize latency.
-   **Limits:** Limit the number of active rules per workspace to prevent abuse.
