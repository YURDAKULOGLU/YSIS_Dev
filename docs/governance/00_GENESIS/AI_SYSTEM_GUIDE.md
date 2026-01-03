# 🤖 AI Development System - Complete Guide

> **Comprehensive guide for AI agents working with specialized development systems**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Agent System](#agent-system)
4. [Workflow System](#workflow-system)
5. [Template System](#template-system)
6. [Command System](#command-system)
7. [Knowledge Base](#knowledge-base)
8. [Practical Usage](#practical-usage)
9. [Quick Reference](#quick-reference)

---

## [TARGET] Overview

This system combines multiple AI-driven development methodologies into a unified workspace:

- **Agent-Based Development**: Specialized AI personas for different roles (PM, Architect, Developer, QA)
- **Workflow Orchestration**: Multi-step processes with handoffs between agents
- **Template-Driven Documentation**: Structured templates for PRDs, specifications, architectures
- **Command Execution**: Slash commands and executable workflows
- **Knowledge Management**: Curated knowledge bases and best practices

### File Organization

```
.YBIS_Dev/Veriler/
├── agents/          -> AI agent definitions (PM, Architect, Dev, QA, etc.)
├── workflows/       -> Multi-step processes (brownfield, greenfield)
├── templates/       -> Document templates (PRD, spec, architecture)
├── Commands/        -> Executable command definitions
├── data/            -> Knowledge bases and reference material
├── checklists/      -> Validation checklists
├── scripts/         -> Automation scripts (if needed)
└── utils/           -> Utility files and helpers

.claude/commands/YBIS/
└── [command].md     -> Claude Code slash commands (point to Veriler/Commands/)
```

**Path Structure Notes:**
- All system files are under `.YBIS_Dev/Veriler/`
- Commands in `.YBIS_Dev/Veriler/Commands/` are executable workflows
- Claude Code commands in `.claude/commands/YBIS/` reference the main commands
- Templates, agents, and data files use relative paths within `.YBIS_Dev/Veriler/`

---

## 3. The YBIS Orchestrator: Intent-Driven Workflows

The YBIS system is not just a collection of agents and commands; it is an orchestrated environment designed to guide development through standardized, repeatable processes. The **YBIS Orchestrator** is not a specific agent, but a core logic that **every agent must follow** when faced with a complex user request.

**Core Principle:** The primary goal is to map a user's *intent* to a predefined, standardized *workflow*, rather than performing ad-hoc tasks. This ensures consistency, quality, and predictability.

### The Orchestrator Workflow

All agents must adhere to the following four-step process when a user's request is not a simple, single-command action:

#### Step 1: Intent Analysis
The agent first analyzes the user's request to understand the underlying goal. Keywords like "add feature", "fix bug", "refactor", "analyze", "create document" are triggers for the Orchestrator logic.

#### Step 2: Workflow Registry Lookup
Instead of acting immediately, the agent consults the central **Workflow Registry**. This registry is the single source of truth for all standardized processes in the project.

**Proposal: `workflow-registry.yaml`**

To formalize this process, we will create a `.YBIS_Dev/Veriler/workflow-registry.yaml` file. This file will explicitly map user intents to corresponding workflows.

*Example `workflow-registry.yaml`:*
```yaml
- intent: "yeni özellik ekle"
  keywords: ["yeni özellik", "ekle", "oluştur", "feature"]
  workflows:
    - name: "Kapsamlı BMad Yolu"
      description: "Detaylı planlama ve story oluşturma için."
      command: "/ybis:create-story"
      file: ".YBIS_Dev/Veriler/workflows/create-story.yaml"
    - name: "Hızlı Implementasyon"
      description: "Mevcut bir görev tanımına göre direkt kodlama için."
      command: "/ybis:implement"
      file: ".YBIS_Dev/Veriler/workflows/feature-development-workflow.yaml"

- intent: "mevcut kodu iyileştir"
  keywords: ["refactor", "iyileştir", "temizle", "optimize et"]
  workflows:
    - name: "Akıllı Refactor"
      description: "Kod kokularını ve teknik borcu azaltmak için."
      command: "/ybis:sc-refactor"
      file: ".YBIS_Dev/Veriler/workflows/code-review.yaml"
```

#### Step 3: Present Options (If Workflow Exists)
If the Orchestrator finds one or more matching workflows in the registry, the agent must present these options to the user, along with their descriptions and triggering commands.

*Agent Response Example:*
> "Yeni bir özellik eklemek istediğinizi anlıyorum. Bunun için birkaç standart yolumuz var:
> 1.  **Kapsamlı BMad Yolu:** Detaylı planlama ve story oluşturma için. (Komut: `/ybis:create-story`)
> 2.  **Hızlı Implementasyon:** Mevcut bir görev tanımına göre direkt kodlama için. (Komut: `/ybis:implement`)
> Nasıl ilerlemek istersiniz?"

#### Step 4: Propose New Workflow (If Gap Is Detected)
If no standard workflow matches the user's intent, the agent **must not improvise**. Instead, it must identify this as a process gap and propose to standardize it.

*Agent Response Example:*
> "Performans testi yapmak için standart bir iş akışımız henüz bulunmuyor.
> **Öneri:** Bu işlemi gelecekte tutarlı bir şekilde yapabilmek için `workflows/performance-testing.yaml` adında yeni bir iş akışı oluşturalım. Bu akış, testin nasıl yapılacağını, hangi metriklerin toplanacağını ve raporun nasıl formatlanacağını tanımlayacak.
> Bu standart iş akışını oluşturmamı onaylıyor musunuz?"

This Orchestrator model is the foundation of the YBIS development methodology. It turns every agent into a guardian of process quality and standardization.

---
## 4. System Architecture

### Two-Phase Development Approach

#### Phase 1: Planning (Document Creation)
- Generate comprehensive specifications
- Create architecture documents
- Define user stories and epics
- Establish technical decisions

#### Phase 2: Implementation (Execution)
- Shard large documents into focused pieces
- Execute story-by-story development
- Implement with specialized agents
- Review and refine code

### Core Philosophy

**You Direct, AI Executes**
- Provide vision and decisions
- Agents handle implementation details
- Structured workflows guide progress
- Clean handoffs ensure focus

**Role Specialization**
- Each agent masters one role
- No context-switching = higher quality
- Persona-driven behavior
- Command-based interaction

---

## 🤖 Agent System

### What Are Agents?

Agents are specialized AI personas with:
- Defined roles and responsibilities
- Specific commands and capabilities
- Associated templates and tasks
- Structured interaction patterns

### Available Agents

#### 📋 **PM (Product Manager)** - `Veriler/agents/pm.md`
**Persona**: Investigative Product Strategist & Market-Savvy PM

**When to Use**:
- Creating PRDs (Product Requirements Documents)
- Product strategy and feature prioritization
- Roadmap planning
- Stakeholder communication

**Key Commands**:
- `*help` - Show available commands
- `*create-prd` - Create PRD using prd-tmpl.yaml
- `*create-brownfield-prd` - Create PRD for existing systems
- `*create-epic` - Create epic for brownfield projects
- `*create-story` - Create user story from requirements
- `*shard-prd` - Break down PRD into manageable pieces
- `*doc-out` - Output full document to destination file

**Core Principles**:
- Deeply understand "Why" - uncover root causes
- Champion the user - focus on value
- Data-informed decisions
- Ruthless prioritization & MVP focus
- Clarity & precision in communication

**Dependencies**:
- Templates: `prd-tmpl.yaml`, `brownfield-prd-tmpl.yaml`
- Tasks: `create-doc.md`, `shard-doc.md`, `brownfield-create-epic.md`
- Checklists: `pm-checklist.md`, `change-checklist.md`

#### 🏗️ **Architect** - `Veriler/agents/architect.md`
**Persona**: Holistic System Architect & Full-Stack Technical Leader

**When to Use**:
- System design and architecture
- Technology selection
- API design
- Infrastructure planning
- Cross-stack optimization

**Key Commands**:
- `*help` - Show available commands
- `*create-backend-architecture` - Backend architecture with architecture-tmpl.yaml
- `*create-brownfield-architecture` - Architecture for existing systems
- `*create-frontend-architecture` - Frontend/UI architecture
- `*document-project` - Comprehensive project documentation

**Core Principles**:
- Holistic System Thinking
- User Experience Drives Architecture
- Pragmatic Technology Selection
- Progressive Complexity
- Cross-Stack Performance Focus
- Developer Experience as First-Class Concern
- Security at Every Layer
- Data-Centric Design

**Dependencies**:
- Templates: `architecture-tmpl.yaml`, `brownfield-architecture-tmpl.yaml`, `front-end-architecture-tmpl.yaml`
- Tasks: `create-doc.md`, `document-project.md`

#### 👨‍💻 **Dev (Developer)** - `Veriler/agents/dev.md`
**Persona**: Implementation-focused developer

**When to Use**:
- Implementing approved stories
- Writing code from specifications
- Creating test implementations
- File operations and real coding

**Key Commands**:
- `*help` - Show available commands
- `*implement-story` - Implement user story
- `*run-tests` - Execute test suite
- `*update-file-list` - Track changed files

**Core Principles**:
- Follow architecture exactly
- Test-driven development
- Clean code practices
- Incremental progress

#### 🎨 **UX Expert** - `Veriler/agents/ux-expert.md`
**Persona**: User experience specialist

**When to Use**:
- UI/UX design
- User flow creation
- Accessibility requirements
- Frontend specifications

**Key Commands**:
- `*help` - Show available commands
- `*create-frontend-spec` - Create UI specification
- `*design-user-flow` - Design user interaction flows

**Dependencies**:
- Templates: `front-end-spec-tmpl.yaml`, `front-end-architecture-tmpl.yaml`

#### [OK] **QA (Quality Assurance)** - `Veriler/agents/qa.md`
**Persona**: Senior developer with review and refactoring ability

**When to Use**:
- Code review
- Refactoring implementations
- Testing validation
- Quality checks

**Key Commands**:
- `*help` - Show available commands
- `*review-story` - Review implementation
- `*qa-gate` - Run quality gate checks
- `*apply-fixes` - Apply QA fixes

**Core Principles**:
- Fix small issues directly
- Leave checklist for complex items
- Focus on quality and maintainability

**Dependencies**:
- Tasks: `review-story.md`, `qa-gate.md`, `apply-qa-fixes.md`
- Templates: `qa-gate-tmpl.yaml`

#### [CHART] **PO (Product Owner)** - `Veriler/agents/po.md`
**Persona**: Validation and oversight specialist

**When to Use**:
- Document validation
- Artifact approval
- Checklist execution
- Quality assurance

**Key Commands**:
- `*help` - Show available commands
- `*validate-artifacts` - Validate all documents
- `*shard-documents` - Break documents into pieces
- `*execute-checklist` - Run validation checklists

**Dependencies**:
- Checklists: `po-master-checklist.md`
- Tasks: `execute-checklist.md`, `shard-doc.md`

#### [DOC] **SM (Scrum Master)** - `Veriler/agents/sm.md`
**Persona**: Story creation and management

**When to Use**:
- Creating user stories
- Story validation
- Sprint planning

**Key Commands**:
- `*help` - Show available commands
- `*create-story` - Create next story from sharded docs
- `*validate-story` - Validate story completeness

**Dependencies**:
- Tasks: `create-next-story.md`, `validate-next-story.md`
- Templates: `story-tmpl.yaml`

#### [SEARCH] **Analyst** - `Veriler/agents/analyst.md`
**Persona**: Research and analysis specialist

**When to Use**:
- Project analysis
- Market research
- Requirement gathering
- Deep research prompts

**Key Commands**:
- `*help` - Show available commands
- `*analyze-project` - Analyze existing project
- `*deep-research` - Create deep research prompt
- `*document-project` - Document project comprehensively

**Dependencies**:
- Tasks: `document-project.md`, `create-deep-research-prompt.md`

### Agent Activation Pattern

All agents follow this activation pattern:

```yaml
activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE - contains complete persona
  - STEP 2: Adopt the persona defined in agent/persona sections
  - STEP 3: Load project configuration if exists
  - STEP 4: Greet user with name/role and run *help
  - DO NOT load other agent files during activation
  - ONLY load dependency files when user requests execution
  - STAY IN CHARACTER!
  - CRITICAL: Greet, show *help, then HALT for user input
```

### Agent File Structure

```yaml
agent:
  name: [Agent Name]
  id: [agent-id]
  title: [Role Title]
  icon: [Emoji]
  whenToUse: [Description of use cases]

persona:
  role: [Role Description]
  style: [Communication style]
  identity: [Core identity]
  focus: [Primary focus]
  core_principles:
    - [Principle 1]
    - [Principle 2]

commands:
  - help: Show numbered list of commands
  - [command]: [description]

dependencies:
  checklists: [list]
  tasks: [list]
  templates: [list]
  data: [list]
```

### Using Agents

**Activation**:
```
@pm        -> Activate Product Manager
@architect -> Activate Architect
@dev       -> Activate Developer
@qa        -> Activate QA
```

**Command Execution**:
```
*help              -> List available commands
*create-prd        -> Execute PRD creation
*shard-doc         -> Shard large document
```

**Best Practices**:
- Use new chat for each agent activation (clean context)
- Let agent greet and show help before proceeding
- Select commands by number or name
- Provide clear input when elicitation is required
- Keep agents in character throughout session

---

## 🔄 Workflow System

### What Are Workflows?

Workflows are multi-step processes that orchestrate multiple agents to complete complex objectives.

**Key Characteristics**:
- Sequential agent handoffs
- Clear input/output artifacts
- Decision points and conditions
- Optional and repeatable steps
- Mermaid flow diagrams

### Workflow Types

#### Brownfield Workflows (Existing Systems)

**`brownfield-service.yaml`** - Service/API Enhancement
- **Use When**: Enhancing existing backend services/APIs
- **Project Types**: service-modernization, api-enhancement, microservice-extraction
- **Flow**: architect -> pm -> architect -> po -> sm -> dev -> qa (loop)
- **Creates**: prd.md, architecture.md, sharded docs, story.md, implementation

**`brownfield-ui.yaml`** - UI Enhancement
- **Use When**: Adding features to existing frontend
- **Project Types**: ui-modernization, ux-improvement, design-system-integration
- **Flow**: ux-expert -> pm -> architect -> po -> sm -> dev -> qa (loop)
- **Creates**: ui-spec.md, prd.md, architecture.md, stories, implementation

**`brownfield-fullstack.yaml`** - Full-Stack Enhancement
- **Use When**: Feature spans frontend + backend
- **Project Types**: feature-expansion, integration-enhancement
- **Flow**: analyst -> pm -> architect -> ux-expert -> po -> sm -> dev -> qa (loop)
- **Creates**: Complete documentation suite, full implementation

#### Greenfield Workflows (New Systems)

**`greenfield-service.yaml`** - New Service/API
- **Use When**: Building new backend service from scratch
- **Project Types**: new-api, new-microservice, data-service
- **Flow**: pm -> architect -> po -> sm -> dev -> qa (loop)
- **Creates**: prd.md, architecture.md, stories, new codebase

**`greenfield-ui.yaml`** - New UI
- **Use When**: Building new frontend application
- **Project Types**: new-web-app, new-mobile-app, design-system
- **Flow**: pm -> ux-expert -> architect -> po -> sm -> dev -> qa (loop)
- **Creates**: prd.md, ui-spec.md, architecture.md, new UI codebase

**`greenfield-fullstack.yaml`** - New Full-Stack Application
- **Use When**: Building complete application from scratch
- **Project Types**: new-saas, new-product, mvp-development
- **Flow**: pm -> architect -> ux-expert -> po -> sm -> dev -> qa (loop)
- **Creates**: Complete application with all documentation

### Workflow Structure

```yaml
workflow:
  id: [unique-id]
  name: [Workflow Name]
  description: [What this workflow does]
  type: brownfield|greenfield
  project_types:
    - [type1]
    - [type2]

  sequence:
    - step: [step-name]
      agent: [agent-id]
      action: [what to do]
      creates: [output artifacts]
      requires: [prerequisites]
      optional: true|false
      condition: [when to execute]
      repeats: [repetition pattern]
      notes: |
        Detailed instructions for this step

  flow_diagram: |
    ```mermaid
    graph TD
        A[Start] --> B[Step 1]
        B --> C[Step 2]
    ```

  decision_guidance:
    when_to_use:
      - [scenario 1]
      - [scenario 2]

  handoff_prompts:
    [agent1]_to_[agent2]: "Handoff message"
```

### Workflow Execution Example

**Brownfield Service Enhancement**:

1. **Architect** analyzes existing service
   - Reviews documentation, codebase, metrics
   - Creates: project analysis documents

2. **PM** creates PRD
   - Requires: existing_service_analysis
   - Uses: brownfield-prd-tmpl.yaml
   - Creates: docs/prd.md

3. **Architect** creates architecture
   - Requires: prd.md
   - Uses: brownfield-architecture-tmpl.yaml
   - Creates: docs/architecture.md

4. **PO** validates artifacts
   - Uses: po-master-checklist
   - May require updates to documents

5. **PO** shards documents
   - Creates: docs/prd/ and docs/architecture/ folders
   - Breaks large docs into focused pieces

6. **SM** creates stories (repeat)
   - Creates: story.md (one at a time)
   - Status: Draft

7. **Analyst/PM** reviews story (optional)
   - Updates: story.md
   - Status: Draft -> Approved

8. **Dev** implements story
   - Creates: implementation files
   - Updates: File List
   - Status: Approved -> Review

9. **QA** reviews implementation (optional)
   - Fixes small issues
   - Leaves checklist for complex items
   - Status: Review -> Done

10. **Dev** addresses QA feedback (if needed)
    - Implements remaining checklist items
    - Returns to QA for approval

11. **Repeat steps 6-10** for all stories

12. **PO** epic retrospective (optional)
    - Validates epic completion
    - Documents learnings

### Using Workflows

**Selection**:
```
Choose workflow based on:
- Project type (brownfield vs greenfield)
- Scope (service, ui, fullstack)
- Existing vs new system
```

**Execution**:
```
1. Select appropriate workflow file
2. Follow sequence steps in order
3. Activate agents as specified (new chat each)
4. Create artifacts as defined
5. Use handoff prompts between agents
6. Execute optional steps based on needs
7. Loop where specified (stories, QA feedback)
```

**Best Practices**:
- Save artifacts to docs/ folder as created
- Use fresh chat for each agent activation
- Validate artifacts before handoff
- Shard documents before story creation
- Keep stories small and focused
- Execute stories sequentially, not parallel

---

## [DOC] Template System

### What Are Templates?

Templates are structured document formats with:
- Predefined sections and headings
- Interactive elicitation workflows
- Validation requirements
- Output specifications

### Template Categories

#### Product Documentation

**`prd-tmpl.yaml`** - Product Requirements Document
- **Sections**: Goals, Background, Requirements (Functional/Non-Functional), UI Goals, Technical Assumptions, Epic List, Epic Details, Checklist Results, Next Steps
- **Workflow**: Interactive with advanced elicitation
- **Output**: docs/prd.md
- **Use With**: PM agent

**`brownfield-prd-tmpl.yaml`** - Brownfield PRD
- **Focus**: Service enhancement with existing system analysis
- **Additional**: Integration strategy, compatibility requirements
- **Use With**: PM agent for existing systems

**`project-brief-tmpl.yaml`** - Project Brief
- **Sections**: Problem statement, target users, success metrics, MVP scope, constraints
- **Recommended**: Create before PRD
- **Use With**: PM agent

#### Architecture Documentation

**`architecture-tmpl.yaml`** - Backend Architecture
- **Sections**: Tech stack, data model, API design, infrastructure, security
- **Output**: docs/architecture.md
- **Use With**: Architect agent

**`brownfield-architecture-tmpl.yaml`** - Brownfield Architecture
- **Focus**: Service integration strategy, API evolution, migration path
- **Use With**: Architect agent for existing systems

**`front-end-architecture-tmpl.yaml`** - Frontend Architecture
- **Sections**: Framework selection, component architecture, state management, routing
- **Output**: docs/front-end-architecture.md
- **Use With**: Architect or UX Expert

**`fullstack-architecture-tmpl.yaml`** - Full-Stack Architecture
- **Sections**: Complete system design, frontend + backend + infrastructure
- **Use With**: Architect agent

#### UI/UX Documentation

**`front-end-spec-tmpl.yaml`** - Frontend Specification
- **Sections**: Component specs, interaction patterns, accessibility, responsive design
- **Output**: docs/front-end-spec.md
- **Use With**: UX Expert

#### Story and Task Documentation

**`story-tmpl.yaml`** - User Story Template
- **Format**: As a [user], I want [action], so that [benefit]
- **Sections**: Acceptance criteria, prerequisites, file list
- **Use With**: SM agent

**`qa-gate-tmpl.yaml`** - QA Gate Template
- **Sections**: Test coverage, code quality, performance, security
- **Use With**: QA agent

#### Research Templates

**`market-research-tmpl.yaml`** - Market Research
- **Sections**: Market analysis, competitor analysis, trends
- **Use With**: PM or Analyst

**`competitor-analysis-tmpl.yaml`** - Competitor Analysis
- **Sections**: Competitor features, strengths/weaknesses, differentiation
- **Use With**: PM or Analyst

**`brainstorming-output-tmpl.yaml`** - Brainstorming Session Output
- **Sections**: Ideas generated, categorization, prioritization
- **Use With**: PM or Analyst

### Template Structure

```yaml
template:
  id: [template-id]
  name: [Template Name]
  version: [version]
  output:
    format: markdown|yaml|json
    filename: [default output path]
    title: "[Document Title]"

workflow:
  mode: interactive|automated
  elicitation: basic|advanced-elicitation

sections:
  - id: [section-id]
    title: [Section Title]
    type: paragraphs|bullet-list|numbered-list|table
    instruction: |
      Instructions for populating this section
    elicit: true|false
    condition: [when to include]
    repeatable: true|false
    examples:
      - "[Example 1]"
      - "[Example 2]"
    choices:
      [field]: [option1, option2, option3]
    sections:
      - [nested sections]
```

### Template Execution

**With Agent**:
```
1. Activate agent (e.g., @pm)
2. Run command that uses template (e.g., *create-prd)
3. Agent loads template
4. Agent follows workflow mode (interactive/automated)
5. If elicit=true, agent asks questions
6. Agent populates sections based on responses
7. Agent validates against template requirements
8. Agent outputs to specified filename
```

**Template Features**:

**Interactive Elicitation** (`elicit: true`):
- Agent asks targeted questions
- User provides answers
- Agent integrates responses into document
- One section at a time or complete document review

**Advanced Elicitation** (`elicitation: advanced-elicitation`):
- Pre-fill sections with educated guesses
- Present complete section for review
- Indicate assumptions made
- Ask targeted questions for unclear elements
- Iterative refinement

**Conditional Sections** (`condition: ...`):
- Only include if condition met
- Example: UI Goals only if PRD has UX requirements

**Repeatable Sections** (`repeatable: true`):
- Epic Details repeat for each epic
- Story sections repeat for each story
- Acceptance criteria repeat as needed

**Validation**:
- Required sections must be present
- Elicit fields must be completed
- Format requirements enforced
- References validated

---

## ⚙️ Command System

### Command Types

#### Slash Commands (Claude Code Integration)

Located in `.claude/commands/YBIS/` - these integrate with Claude Code's native command system.

##### Core Workflow Commands

**`/specify`** - Create Feature Specification
- **Location**: `.claude/commands/YBIS/specify.md`
- **Usage**: `/specify [feature description]`
- **Execution**: See `.YBIS_Dev/Veriler/commands/specify.md`
- **Output**: Feature specification in new branch

**`/plan`** - Implementation Planning
- **Location**: `.claude/commands/YBIS/plan.md`
- **Usage**: `/plan [implementation details]`
- **Execution**: See `.YBIS_Dev/Veriler/commands/plan.md`
- **Output**: Complete implementation plan with artifacts

**`/tasks`** - Generate Task List
- **Location**: `.claude/commands/YBIS/tasks.md`
- **Usage**: `/tasks`
- **Execution**: See `.YBIS_Dev/Veriler/commands/tasks.md`
- **Output**: tasks.md with ordered implementation tasks

**`/clarify`** - Specification Clarification
- **Location**: `.claude/commands/YBIS/clarify.md`
- **Usage**: `/clarify`
- **Execution**: See `.YBIS_Dev/Veriler/commands/clarify.md`
- **Output**: Updated spec with Clarifications section

**`/analyze`** - Cross-Artifact Analysis
- **Location**: `.claude/commands/YBIS/analyze.md`
- **Usage**: `/analyze`
- **Execution**: See `.YBIS_Dev/Veriler/commands/analyze.md`
- **Output**: Analysis report

**`/implement`** - Execute Implementation
- **Location**: `.claude/commands/YBIS/implement.md`
- **Usage**: `/implement`
- **Execution**: See `.YBIS_Dev/Veriler/commands/implement.md`
- **Output**: Implementation with task completion

##### Expert Development Commands

**`/context-implement`** - Context-Aware Implementation
- **Location**: `.claude/commands/YBIS/context-implement.md`
- **Usage**: `/context-implement`
- **Execution**: See `.YBIS_Dev/Veriler/commands/context-implement.md`
- **Output**: Implementation using full conversation context

**`/expert-debug`** - Multi-Agent Debugging
- **Location**: `.claude/commands/YBIS/expert-debug.md`
- **Usage**: `/expert-debug`
- **Execution**: See `.YBIS_Dev/Veriler/commands/expert-debug.md`
- **Output**: Root cause analysis and fixes

**`/deep-review`** - Comprehensive Code Review
- **Location**: `.claude/commands/YBIS/deep-review.md`
- **Usage**: `/deep-review`
- **Execution**: See `.YBIS_Dev/Veriler/commands/deep-review.md`
- **Output**: Security, performance, and architecture review

**`/full-context`** - Load Project Architecture
- **Location**: `.claude/commands/YBIS/full-context.md`
- **Usage**: `/full-context`
- **Execution**: See `.YBIS_Dev/Veriler/commands/full-context.md`
- **Output**: Complete project context loaded

**`/update-docs`** - Auto-Update Documentation
- **Location**: `.claude/commands/YBIS/update-docs.md`
- **Usage**: `/update-docs`
- **Execution**: See `.YBIS_Dev/Veriler/commands/update-docs.md`
- **Output**: Updated documentation for modified code

##### Specialized Code Operations

**`/sc-troubleshoot`** - Domain-Specific Troubleshooting
- **Location**: `.claude/commands/YBIS/sc-troubleshoot.md`
- **Usage**: `/sc-troubleshoot`
- **Execution**: See `.YBIS_Dev/Veriler/commands/sc-troubleshoot.md`
- **Output**: Troubleshooting analysis and fixes

**`/sc-improve`** - Apply Optimization Patterns
- **Location**: `.claude/commands/YBIS/sc-improve.md`
- **Usage**: `/sc-improve`
- **Execution**: See `.YBIS_Dev/Veriler/commands/sc-improve.md`
- **Output**: Optimized code using established patterns

**`/sc-document`** - Generate Comprehensive Documentation
- **Location**: `.claude/commands/YBIS/sc-document.md`
- **Usage**: `/sc-document`
- **Execution**: See `.YBIS_Dev/Veriler/commands/sc-document.md`
- **Output**: API docs, READMEs, architecture documentation

**`/sc-refactor`** - Intelligent Refactoring Engine
- **Location**: `.claude/commands/YBIS/sc-refactor.md`
- **Usage**: `/sc-refactor`
- **Execution**: See `.YBIS_Dev/Veriler/commands/sc-refactor.md`
- **Output**: Systematically restructured code with intelligent patterns

#### Agent Commands (Star Prefix)

Located in `Veriler/commands/` - these are agent-specific executable workflows.

**Structure**:
```markdown
# Command Name

## Description
[What this command does]

## Input
- [Input 1]
- [Input 2]

## Execution Steps
1. Step 1
2. Step 2
3. Step 3

## Output
[Expected output]

## Usage
agent-id -> *command-name
```

**Examples**:
- `create-doc.md` - Create document from template
- `shard-doc.md` - Break document into pieces
- `create-next-story.md` - Create next user story
- `review-story.md` - Review story implementation
- `document-project.md` - Comprehensive project documentation

### Command Execution Patterns

**Slash Command Workflow**:
```
User types: /specify Add user authentication
  ↓
Claude Code activates command
  ↓
Command runs script (create-new-feature.ps1)
  ↓
AI follows execution steps
  ↓
Output created (spec.md in new branch)
  ↓
AI reports completion
```

**Agent Command Workflow**:
```
Agent activated: @pm
  ↓
User selects: *create-prd
  ↓
Agent loads: create-doc.md task
  ↓
Agent loads: prd-tmpl.yaml template
  ↓
Agent executes: interactive elicitation
  ↓
Agent creates: docs/prd.md
  ↓
Agent reports: completion
```

### Creating New Commands

**Slash Command** (`.claude/commands/`):
```markdown
---
description: Brief description of command
---

Command explanation and context.

User input:
$ARGUMENTS

Execution steps:

1. **Step 1** -> Description
   - Detail 1
   - Detail 2

2. **Step 2** -> Description
   - Detail 1
   - Detail 2

Output: What gets created/returned
```

**Agent Command** (`Veriler/Commands/`):
```markdown
# Command Name

Brief description of what this command does.

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]

## Inputs
- input1: Description
- input2: Description

## Execution

### Step 1: [Step Name]
Description and details

### Step 2: [Step Name]
Description and details

## Output
Description of output artifacts

## Usage
@agent-name -> *command-name [arguments]
```

---

## 📚 Knowledge Base

### Data Files

Located in `Veriler/data/` - curated knowledge and reference material.

**`bmad-kb.md`** - Core methodology knowledge base
- Overview of agent-based development
- How the method works
- Two-phase approach (planning vs implementation)
- Development loop patterns
- Best practices and workflows

**`technical-preferences.md`** - Technical decision defaults
- Language preferences
- Framework choices
- Architecture patterns
- Deployment targets
- Testing strategies

**`brainstorming-techniques.md`** - Brainstorming methods
- Techniques for idea generation
- Facilitation patterns
- Session structures

**`elicitation-methods.md`** - Requirement gathering techniques
- Interview patterns
- Question frameworks
- User story extraction

**`test-levels-framework.md`** - Testing strategy
- Unit testing
- Integration testing
- E2E testing
- Manual testing

**`test-priorities-matrix.md`** - Test prioritization
- Critical path testing
- Risk-based testing
- Coverage strategies

### Using Knowledge Base

**During Agent Activation**:
```
Some agents auto-load KB files:
- Architect loads technical-preferences.md
- PM loads brainstorming-techniques.md
- QA loads test-levels-framework.md
```

**Manual Reference**:
```
Ask agent to consult KB:
"@pm review brainstorming-techniques.md and facilitate session"
"@architect check technical-preferences.md for framework choice"
```

**Template Integration**:
```
Templates reference KB files:
prd-tmpl.yaml -> checks technical-preferences.md
architecture-tmpl.yaml -> references technical-preferences.md
```

---

## [LAUNCH] Practical Usage

### Complete Workflow Example: Brownfield API Enhancement

**Scenario**: Add authentication feature to existing API

#### Phase 1: Planning (Document Creation)

**Step 1: Analyze Existing System**
```
Activate: @architect

Architect greeting and *help

User: "Analyze our existing API for adding authentication"

Architect executes: document-project task
  - Reviews codebase
  - Identifies integration points
  - Documents current architecture

Creates: docs/existing-system-analysis.md
```

**Step 2: Create PRD**
```
New Chat -> Activate: @pm

PM greeting and *help

User: "Create brownfield PRD for adding JWT authentication to our API"

PM executes: *create-brownfield-prd
  - Loads brownfield-prd-tmpl.yaml
  - Asks about goals (secure API, user management)
  - Elicits requirements (FR: JWT tokens, refresh tokens, role-based access)
  - Gathers technical assumptions (Node.js, Express, PostgreSQL)
  - Creates epic list (Epic 1: Auth Infrastructure, Epic 2: User Management)
  - Details stories with acceptance criteria

Creates: docs/prd.md
```

**Step 3: Create Architecture**
```
New Chat -> Activate: @architect

Architect greeting and *help

User: "Create brownfield architecture for authentication, here's the PRD: docs/prd.md"

Architect executes: *create-brownfield-architecture
  - Reads docs/prd.md
  - Loads brownfield-architecture-tmpl.yaml
  - Designs integration strategy (middleware, routes, database schema)
  - Plans API evolution (backward compatible endpoints)
  - Documents security approach (password hashing, token signing)

Creates: docs/architecture.md
```

**Step 4: Validate Artifacts**
```
New Chat -> Activate: @po

PO greeting and *help

User: "Validate artifacts in docs/ folder"

PO executes: *validate-artifacts
  - Loads po-master-checklist
  - Checks docs/prd.md (requirements clarity, epic sequencing)
  - Checks docs/architecture.md (technical feasibility, security)
  - Identifies issues if any

If issues found:
  - Return to @pm or @architect to fix
  - Re-validate

If clean:
  - Proceed to sharding
```

**Step 5: Shard Documents**
```
Same PO chat

User: "Shard docs/prd.md"

PO executes: *shard-doc
  - Breaks docs/prd.md into focused pieces
  - Creates docs/prd/epic-1.md, docs/prd/epic-2.md
  - Creates docs/prd/story-1.1.md, docs/prd/story-1.2.md, etc.

Creates: docs/prd/ directory with sharded content
```

#### Phase 2: Implementation (Story-by-Story)

**Step 6: Create First Story**
```
New Chat -> Activate: @sm

SM greeting and *help

User: "Create next story from sharded docs"

SM executes: *create-story
  - Reads docs/prd/story-1.1.md
  - Loads story-tmpl.yaml
  - Formats user story
  - Adds acceptance criteria
  - Sets status: Draft

Creates: story.md
```

**Step 7: Review Story (Optional)**
```
New Chat -> Activate: @analyst

Analyst greeting and *help

User: "Review story.md for completeness"

Analyst reviews:
  - Story clarity
  - Acceptance criteria coverage
  - Alignment with architecture
  - Updates status: Draft -> Approved
```

**Step 8: Implement Story**
```
New Chat -> Activate: @dev

Dev greeting and *help

User: "Implement story.md"

Dev executes: *implement-story
  - Reads story.md and docs/architecture.md
  - Creates middleware/auth.js
  - Creates routes/auth.js
  - Creates database migration
  - Writes unit tests
  - Updates File List

Marks story: Approved -> Review

Creates: Implementation files
```

**Step 9: QA Review (Optional)**
```
New Chat -> Activate: @qa

QA greeting and *help

User: "Review implementation for story.md"

QA executes: *review-story
  - Reviews code quality
  - Checks test coverage
  - Validates security practices
  - Fixes small issues directly
  - Leaves checklist for complex items

If checklist has items:
  - Return to @dev to address
  - Re-submit to QA
Else:
  - Mark story: Review -> Done
```

**Step 10: Repeat for All Stories**
```
For each remaining story:
  SM -> create story
  Analyst -> review (optional)
  Dev -> implement
  QA -> review (optional)

Continue until all epics complete
```

**Step 11: Epic Retrospective (Optional)**
```
New Chat -> Activate: @po

PO greeting and *help

User: "Run epic retrospective for Epic 1"

PO executes:
  - Validates epic completion
  - Documents learnings
  - Identifies improvements

Creates: docs/epic-1-retrospective.md
```

### Quick Start Patterns

#### Pattern 1: New Feature Spec (Specify Method)
```
1. /specify Add user profile management
   -> Creates spec in new branch

2. /clarify
   -> Identifies ambiguities, asks questions, updates spec

3. /plan Use PostgreSQL for user data
   -> Creates implementation plan with artifacts

4. /tasks
   -> Generates ordered task list

5. /implement
   -> Executes tasks, tracks progress
```

#### Pattern 2: Greenfield Full-Stack App
```
1. @pm -> *create-prd
   -> Interactive PRD creation for new app

2. @architect -> *create-architecture
   -> System design for full stack

3. @ux-expert -> *create-frontend-spec
   -> UI/UX specification

4. @po -> *validate-artifacts
   -> Check all docs

5. @po -> *shard-documents
   -> Break into focused pieces

6. Loop: @sm -> @dev -> @qa
   -> Story-by-story implementation
```

#### Pattern 3: Quick Document Creation
```
@pm -> *create-prd
  -> Specify use prd-tmpl.yaml
  -> Answer elicitation questions
  -> Review output
  -> Save to docs/prd.md
```

### Common Scenarios

**Scenario: Generate PRD for Existing System Enhancement**
```
Agent: @pm
Command: *create-brownfield-prd
Template: brownfield-prd-tmpl.yaml
Input: Feature description, existing system context
Output: docs/prd.md with integration strategy
```

**Scenario: Design Architecture for New API**
```
Agent: @architect
Command: *create-backend-architecture
Template: architecture-tmpl.yaml
Input: PRD (docs/prd.md)
Output: docs/architecture.md with tech stack, data model, API design
```

**Scenario: Break Large PRD into Stories**
```
Agent: @po
Command: *shard-doc
Input: docs/prd.md
Output: docs/prd/epic-1.md, docs/prd/story-1.1.md, etc.
```

**Scenario: Implement User Story**
```
Agent: @dev
Command: *implement-story
Input: story.md, docs/architecture.md
Output: Implementation files, tests, updated File List
```

**Scenario: Review Code Quality**
```
Agent: @qa
Command: *review-story
Input: Implementation files, story.md
Output: Fixed issues, remaining checklist, updated story status
```

---

## 📖 Quick Reference

### Agent Quick List

| Agent | Icon | ID | Primary Use |
|-------|------|------|-------------|
| Product Manager | 📋 | pm | PRDs, product strategy |
| Architect | 🏗️ | architect | System design, tech selection |
| Developer | 👨‍💻 | dev | Implementation, coding |
| UX Expert | 🎨 | ux-expert | UI/UX design, frontend spec |
| QA | [OK] | qa | Code review, quality checks |
| Product Owner | [CHART] | po | Validation, approval |
| Scrum Master | [DOC] | sm | Story creation, management |
| Analyst | [SEARCH] | analyst | Research, analysis |

### Command Quick List

#### Slash Commands

##### Core Workflow
| Command | Purpose | Output |
|---------|---------|--------|
| /specify | Create feature spec | spec.md |
| /plan | Implementation planning | plan.md + artifacts |
| /tasks | Generate task list | tasks.md |
| /clarify | Clarify ambiguities | Updated spec |
| /analyze | Cross-artifact analysis | Analysis report |
| /implement | Execute implementation | Code + completion |

##### Expert Development
| Command | Purpose | Output |
|---------|---------|--------|
| /context-implement | Context-aware implementation | Implementation with full context |
| /expert-debug | Multi-agent debugging | Root cause analysis + fixes |
| /deep-review | Comprehensive review | Security, performance, architecture review |
| /full-context | Load project architecture | Complete project context |
| /update-docs | Auto-update documentation | Updated docs for code changes |

##### Specialized Code Operations
| Command | Purpose | Output |
|---------|---------|--------|
| /sc-troubleshoot | Domain-specific troubleshooting | Analysis + fixes |
| /sc-improve | Apply optimization patterns | Optimized code |
| /sc-document | Generate documentation | API docs, READMEs, architecture |
| /sc-refactor | Intelligent refactoring engine | Restructured code with patterns |

#### Agent Commands (*)
| Command | Agent | Purpose |
|---------|-------|---------|
| *create-prd | pm | Create PRD |
| *create-brownfield-prd | pm | PRD for existing system |
| *shard-prd | pm | Break PRD into pieces |
| *create-backend-architecture | architect | Backend architecture |
| *create-brownfield-architecture | architect | Architecture for existing system |
| *create-frontend-spec | ux-expert | Frontend specification |
| *implement-story | dev | Implement user story |
| *review-story | qa | Review implementation |
| *validate-artifacts | po | Validate documents |
| *shard-documents | po | Shard any document |
| *create-story | sm | Create user story |

### Template Quick List

| Template | Use For | Output |
|----------|---------|--------|
| prd-tmpl.yaml | Product requirements | docs/prd.md |
| brownfield-prd-tmpl.yaml | Existing system PRD | docs/prd.md |
| architecture-tmpl.yaml | Backend architecture | docs/architecture.md |
| brownfield-architecture-tmpl.yaml | Existing system arch | docs/architecture.md |
| front-end-spec-tmpl.yaml | Frontend specification | docs/front-end-spec.md |
| front-end-architecture-tmpl.yaml | Frontend architecture | docs/front-end-architecture.md |
| story-tmpl.yaml | User story | story.md |
| qa-gate-tmpl.yaml | QA validation | qa-gate.md |

### Workflow Quick List

| Workflow | Type | Use When |
|----------|------|----------|
| brownfield-service.yaml | Brownfield | Enhance existing API/service |
| brownfield-ui.yaml | Brownfield | Enhance existing UI |
| brownfield-fullstack.yaml | Brownfield | Enhance full-stack app |
| greenfield-service.yaml | Greenfield | New API/service |
| greenfield-ui.yaml | Greenfield | New UI application |
| greenfield-fullstack.yaml | Greenfield | New full-stack app |

### File Path Quick Reference

```
Veriler/
├── agents/           -> Agent definitions (@pm, @architect, etc.)
├── workflows/        -> Multi-step process definitions
├── templates/        -> Document templates (PRD, architecture, etc.)
├── Commands/         -> Executable command definitions (*create-prd, etc.)
├── data/             -> Knowledge bases (bmad-kb.md, technical-preferences.md)
├── scripts/          -> Automation scripts
├── tasks/            -> Task definitions
└── utils/            -> Utility files

.claude/commands/     -> Slash commands (/specify, /plan, /tasks)
```

### Best Practices Checklist

**Agent Usage**:
- [OK] Use new chat for each agent activation
- [OK] Let agent greet and show *help before proceeding
- [OK] Keep agents in character throughout session
- [OK] Save artifacts immediately after creation
- [OK] Use handoff prompts between agents

**Workflow Execution**:
- [OK] Select appropriate workflow (brownfield vs greenfield)
- [OK] Follow sequence steps in order
- [OK] Validate artifacts before handoff
- [OK] Shard documents before story creation
- [OK] Execute stories sequentially

**Document Creation**:
- [OK] Create Project Brief before PRD
- [OK] Use appropriate template for context
- [OK] Answer elicitation questions completely
- [OK] Review output before saving
- [OK] Validate with PO agent

**Story Implementation**:
- [OK] Keep stories small and focused
- [OK] One story per dev session
- [OK] Update File List during implementation
- [OK] Write tests with code
- [OK] QA review before marking done

### Common Pitfalls to Avoid

[FAIL] Activating multiple agents in same chat (context pollution)
[FAIL] Skipping PO validation step (quality issues)
[FAIL] Creating large stories (context overflow)
[FAIL] Implementing stories in parallel (dependency issues)
[FAIL] Skipping elicitation questions (incomplete specs)
[FAIL] Not sharding documents (context management)
[FAIL] Missing architecture before implementation (technical debt)
[FAIL] Bypassing QA review (quality shortcuts)

---

## 🎓 Advanced Topics

### Custom Agent Creation

To create a custom agent:

1. Copy existing agent file as template
2. Modify agent metadata (name, id, title, icon)
3. Define persona (role, style, identity, principles)
4. List commands specific to role
5. Specify dependencies (tasks, templates, checklists, data)
6. Save to `Veriler/agents/[agent-name].md`

### Custom Workflow Design

To create a custom workflow:

1. Identify project type and scope
2. Map agent sequence with handoffs
3. Define artifacts created at each step
4. Specify prerequisites and conditions
5. Add decision guidance
6. Create Mermaid flow diagram
7. Save to `Veriler/workflows/[workflow-name].yaml`

### Custom Template Creation

To create a custom template:

1. Define output format and filename
2. Specify workflow mode (interactive/automated)
3. List sections with types (paragraphs, lists, tables)
4. Add instructions for each section
5. Include examples and choices
6. Mark elicitation points
7. Save to `Veriler/templates/[template-name].yaml`

### Integration with Claude Code

Commands in `.claude/commands/` automatically integrate:

1. Create `.md` file in `.claude/commands/`
2. Add frontmatter with description
3. Include execution steps
4. Reference `Veriler/` files as needed
5. Claude Code will list in `/` autocomplete

**Example**:
```markdown
---
description: Create architecture document
---

User input: $ARGUMENTS

Execution:
1. Load Veriler/agents/architect.md
2. Execute *create-backend-architecture
3. Use Veriler/templates/architecture-tmpl.yaml
4. Output to docs/architecture.md
```

---

## 📞 Support and Troubleshooting

### Common Issues

**Issue: Agent not staying in character**
- Solution: Use fresh chat for activation, let agent complete greeting and *help

**Issue: Command not found**
- Solution: Verify command exists in agent's commands list, use * prefix for agent commands

**Issue: Template elicitation skipped**
- Solution: Ensure template has `elicit: true`, agent follows interactive workflow mode

**Issue: Workflow step unclear**
- Solution: Reference workflow's handoff_prompts, check notes for detailed instructions

**Issue: Story too large**
- Solution: Break into smaller stories, focus on single vertical slice

**Issue: Context overflow during implementation**
- Solution: Shard documents, create smaller stories, use fresh dev chat

### Getting Help

**Documentation**:
- This guide: `AI_SYSTEM_GUIDE.md`
- Knowledge base: `Veriler/data/bmad-kb.md`
- Agent files: `Veriler/agents/[agent].md`
- Workflow files: `Veriler/workflows/[workflow].yaml`
- Template files: `Veriler/templates/[template].yaml`

**Agent Help**:
```
@[agent] -> *help
  -> Shows available commands for that agent
```

**File Inspection**:
```
Read agent file directly to see:
- Full persona definition
- All available commands
- Complete dependencies list
- Activation instructions
```

---

*Last Updated: 2025-10-05*
*Version: 1.0*
*System: AI Development Framework*

---

## 📂 Path Reference Guide

### System Path Structure

All YBIS system files are located under `.YBIS_Dev/Veriler/`:

```
.YBIS_Dev/Veriler/
├── agents/              -> Agent definitions
├── workflows/           -> Workflow orchestrations
├── templates/           -> Document templates
├── commands/            -> Executable commands
├── data/                -> Knowledge bases
├── checklists/          -> Validation checklists
├── YBIS_PROJE_ANAYASASI.md -> Project constitution
└── core-config.yaml     -> Core configuration (if exists)
```

### Common File References

**Templates:**
- `.YBIS_Dev/Veriler/templates/spec-template.md`
- `.YBIS_Dev/Veriler/templates/plan-template.md`
- `.YBIS_Dev/Veriler/templates/tasks-template.md`
- `.YBIS_Dev/Veriler/templates/prd-tmpl.yaml`
- `.YBIS_Dev/Veriler/templates/architecture-tmpl.yaml`

**Commands:**
- `.YBIS_Dev/Veriler/commands/create-doc.md`
- `.YBIS_Dev/Veriler/commands/shard-doc.md`
- `.YBIS_Dev/Veriler/commands/execute-checklist.md`

**Data/Knowledge:**
- `.YBIS_Dev/Veriler/data/bmad-kb.md`
- `.YBIS_Dev/Veriler/data/technical-preferences.md`
- `.YBIS_Dev/Veriler/data/elicitation-methods.md`

**Checklists:**
- `.YBIS_Dev/Veriler/checklists/change-checklist.md`
- `.YBIS_Dev/Veriler/checklists/story-draft-checklist.md`
- `.YBIS_Dev/Veriler/checklists/pm-checklist.md`

### Output Locations

**Generated Specs and Plans:**
- `specs/[feature-name]-spec.md` -> Feature specifications
- `specs/[feature-name]-plan.md` -> Implementation plans
- `specs/tasks.md` -> Task lists
- `specs/research.md`, `specs/data-model.md` -> Design artifacts

**Generated Documentation:**
- `docs/prd.md` -> Product Requirements Document
- `docs/architecture.md` -> Architecture Document
- `docs/prd/` -> Sharded PRD pieces
- `docs/architecture/` -> Sharded architecture pieces

**Stories:**
- Location varies by project configuration
- Default: `stories/[epic].[story].story.md`
- Check `core-config.yaml` for `devStoryLocation`

---
