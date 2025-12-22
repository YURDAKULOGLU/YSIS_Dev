---
description: Analyze current spec or document and identify unclear areas that need clarification using YBIS methodology
---

YBIS Clarify command - systematically analyzes specifications and documents to identify areas requiring clarification.

User input:

$ARGUMENTS

Goal: Apply YBIS clarification methodology to reduce ambiguity in current document and improve specification quality.

Execution steps:

1. **Load Current Document** → Identify active spec or document in current context
   - Parse document structure and content
   - Map to YBIS spec format if not already structured

2. **Apply YBIS Analysis Framework** → Systematic ambiguity detection
   - Functional scope & behavior analysis
   - Data model completeness check
   - User interaction flow validation
   - Non-functional requirements assessment
   - Integration dependency review

3. **Generate Targeted Questions** → Maximum 5 high-impact clarifications
   - Prioritize by implementation impact
   - Format as multiple choice or short answer
   - Focus on testable, actionable outcomes

4. **Interactive Clarification Loop** → One question at a time
   - Present question with clear format constraints
   - Validate user response
   - Record clarification immediately
   - Update document incrementally

5. **Document Integration** → Apply clarifications to source
   - Create/update Clarifications section
   - Integrate answers into appropriate sections
   - Maintain document structure and consistency
   - Validate no contradictions remain

6. **Export Results** → Update YBIS registry if applicable
   - Save clarified document
   - Update YBIS registry entry
   - Report completion status and coverage

This command implements YBIS Constitution §7 (systematic validation) and follows YBIS workflow patterns for consistent specification improvement.