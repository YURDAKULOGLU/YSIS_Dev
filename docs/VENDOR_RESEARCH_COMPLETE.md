# Vendor Research & Recommendations

**Date:** 2026-01-09  
**Status:** Research Complete

---

## ✅ Already in Vendors

Aşağıdaki projeler **zaten vendors klasöründe mevcut**:

1. ✅ **gpt-pilot** - Code generation (zaten var)
2. ✅ **chatdev** - Multi-agent development (zaten var)
3. ✅ **promptfoo** - LLM evaluation (zaten var)
4. ✅ **trulens** - LLM observability (zaten var)

---

## 🔍 Recommended Additional Vendors

### High Priority Additions

#### 1. **swe-agent** (SWE-bench solver)
- **GitHub:** `princeton-nlp/SWE-agent`
- **Description:** AI agent that solves software engineering problems from SWE-bench
- **Why:** Advanced code generation and problem-solving capabilities
- **Integration:** Could complement gpt-pilot for complex code generation
- **Status:** ⏭️ **RECOMMENDED TO ADD**

#### 2. **aider** (AI pair programming)
- **GitHub:** `Aider-AI/aider`
- **Description:** AI pair programmer in your terminal
- **Why:** Terminal-based, lightweight, fast code generation
- **Integration:** Alternative/complement to gpt-pilot
- **Status:** ⏭️ **RECOMMENDED TO ADD**

#### 3. **v0** (Vercel AI UI generation)
- **GitHub:** Repository not found (may be private or different name)
- **Description:** AI-powered UI component generation
- **Why:** Frontend UI generation, complements backend code generation
- **Integration:** UI generation pipeline
- **Status:** ⚠️ **REPOSITORY NOT FOUND** - Need to find correct repo or alternative
- **Alternative:** Consider `shadcn/ui` or other UI generation tools

#### 4. **codeium** (AI coding assistant)
- **GitHub:** `codeium/codeium`
- **Description:** Free AI coding assistant
- **Why:** Alternative to GitHub Copilot, open-source
- **Integration:** Code completion and generation
- **Status:** ⏭️ **OPTIONAL**

### Medium Priority Additions

#### 5. **sweep** (AI codebase agent)
- **GitHub:** `sweepai/sweep`
- **Description:** AI-powered codebase refactoring and feature addition
- **Why:** Automated codebase improvements
- **Integration:** Code maintenance and refactoring
- **Status:** ⏭️ **OPTIONAL**

#### 6. **continue** (VS Code AI extension)
- **GitHub:** `continuedev/continue`
- **Description:** Open-source VS Code AI extension
- **Why:** IDE integration for AI coding
- **Integration:** Development environment integration
- **Status:** ⏭️ **OPTIONAL** (if VS Code integration needed)

#### 7. **cursor-rules** (Cursor IDE rules)
- **GitHub:** `getcursor/cursor`
- **Description:** Cursor IDE (AI-powered editor)
- **Why:** Full IDE with AI, not just extension
- **Integration:** Development environment
- **Status:** ⏭️ **OPTIONAL** (if full IDE needed)

### Low Priority / Research Phase

#### 8. **claude-code** (Anthropic's coding tool)
- **Status:** Commercial, not open-source
- **Note:** Already supported via spec-kit's agent config
- **Action:** ✅ **INTEGRATION PLAN CREATED** - See `docs/COMMERCIAL_TOOLS_INTEGRATION_PLAN.md`
- **Integration:** Via adapter pattern (not vendor cloning)

#### 9. **google-antigravity** (Google's AI IDE)
- **Status:** Commercial, not open-source
- **Action:** ✅ **INTEGRATION PLAN CREATED** - See `docs/COMMERCIAL_TOOLS_INTEGRATION_PLAN.md`
- **Integration:** Via adapter pattern (requires API research)

#### 10. **aws-kiro** (AWS AI IDE)
- **Status:** Commercial, not open-source
- **Action:** ✅ **INTEGRATION PLAN CREATED** - See `docs/COMMERCIAL_TOOLS_INTEGRATION_PLAN.md`
- **Integration:** Via adapter pattern (requires API research)

---

## 📊 Vendor Categories

### Code Generation
- ✅ gpt-pilot (existing)
- ⏭️ swe-agent (recommended)
- ⏭️ aider (recommended)
- ⏭️ sweep (optional)

### LLM Evaluation & Testing
- ✅ promptfoo (existing)
- ✅ trulens (existing)

### Multi-Agent Development
- ✅ chatdev (existing)
- ✅ BMAD-METHOD (existing)
- ✅ autogen (existing)
- ✅ metagpt (existing)

### UI Generation
- ⏭️ v0 (recommended if frontend needed)

### Observability
- ✅ trulens (existing)
- ✅ langfuse (existing)
- ✅ opentelemetry-python (existing)

---

## 🎯 Action Plan

### Immediate (High Value)
1. **swe-agent** - Advanced problem-solving
2. **aider** - Lightweight code generation

### If Frontend Needed
3. **v0** - UI component generation

### Optional (Nice-to-Have)
4. **sweep** - Codebase maintenance
5. **continue** - VS Code integration
6. **codeium** - Alternative coding assistant

---

## 📝 Summary

**Already Have:**
- ✅ gpt-pilot, chatdev, promptfoo, trulens (all requested)

**Recommended to Add:**
- ⏭️ swe-agent (high priority)
- ⏭️ aider (high priority)
- ⏭️ v0 (if frontend needed)

**Total Vendors Count:**
- Current: ~50+ vendors
- Recommended additions: 2-3 high priority

---

## Next Steps

1. ✅ Clone recommended vendors:
   ```bash
   cd vendors
   git clone https://github.com/princeton-nlp/SWE-agent.git swe-agent  # ✅ DONE
   git clone https://github.com/Aider-AI/aider.git aider  # ✅ DONE
   # v0: Repository not found (may be private or different name)
   ```

2. ✅ Commercial tools integration plan created:
   - See `docs/COMMERCIAL_TOOLS_INTEGRATION_PLAN.md`
   - Claude Code, Google Antigravity, AWS Kiro integration via adapters

3. ⏭️ Update vendor integration plan with new vendors

4. ⏭️ Evaluate integration opportunities with existing YBIS workflow

5. ⏭️ Research v0 alternative or correct repository name

