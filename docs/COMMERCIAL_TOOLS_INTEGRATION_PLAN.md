# Commercial AI Tools Integration Plan

**Date:** 2026-01-09  
**Status:** Planning Phase  
**Note:** These tools are **NOT vendors** (not cloned), but **integrated via adapters/config**

---

## Overview

Commercial AI coding tools that need integration (not vendor cloning):
1. **Claude Code** (Anthropic)
2. **Google Antigravity** (Google)
3. **AWS Kiro** (Amazon)

These tools are **commercial services** that require:
- API keys/authentication
- Adapter pattern integration
- Policy-based enablement
- Fallback mechanisms

---

## Integration Strategy

### 1. Claude Code (Anthropic)

**Status:** ✅ **Already Supported via Spec-Kit**

**Current Support:**
- Spec-kit's agent config already includes Claude Code
- YBIS can use Claude Code via spec-kit's `/speckit.*` commands
- No additional adapter needed

**Enhancement Opportunities:**
- Create direct YBIS adapter for Claude Code API (if needed)
- Integrate Claude Code as executor alternative to `local_coder`

**Adapter Implementation:**
```python
# src/ybis/adapters/claude_code.py
class ClaudeCodeExecutor:
    """Claude Code executor adapter."""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        # Use Anthropic SDK or litellm
    
    def is_available(self) -> bool:
        return self.api_key is not None
    
    def execute(self, task: str, context: Dict) -> str:
        # Call Claude Code API
        pass
```

**Registry Entry:**
```yaml
# configs/adapters.yaml
claude_code:
  name: "claude_code"
  type: "executor"
  module_path: "src.ybis.adapters.claude_code.ClaudeCodeExecutor"
  description: "Anthropic Claude Code executor"
  maturity: "beta"
  dependencies:
    - "anthropic>=0.18.0"
  capabilities:
    - "code_generation"
    - "file_editing"
  health_check: "is_available()"
  policy_key: "adapters.claude_code.enabled"
  notes: "Requires ANTHROPIC_API_KEY. Commercial service."
```

---

### 2. Google Antigravity

**Status:** ⏭️ **Integration Needed**

**Current State:**
- Not yet integrated
- Commercial IDE service (not open-source)

**Integration Approach:**
- **Option A:** API-based integration (if API available)
- **Option B:** CLI-based integration (if CLI available)
- **Option C:** MCP server integration (if supported)

**Adapter Implementation:**
```python
# src/ybis/adapters/google_antigravity.py
class GoogleAntigravityExecutor:
    """Google Antigravity executor adapter."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_ANTIGRAVITY_API_KEY")
        # Use Google AI SDK
    
    def is_available(self) -> bool:
        return self.api_key is not None
    
    def execute(self, task: str, context: Dict) -> str:
        # Call Antigravity API
        pass
```

**Registry Entry:**
```yaml
# configs/adapters.yaml
google_antigravity:
  name: "google_antigravity"
  type: "executor"
  module_path: "src.ybis.adapters.google_antigravity.GoogleAntigravityExecutor"
  description: "Google Antigravity AI IDE executor"
  maturity: "experimental"
  dependencies:
    - "google-generativeai>=0.3.0"
  capabilities:
    - "code_generation"
    - "file_editing"
  health_check: "is_available()"
  policy_key: "adapters.google_antigravity.enabled"
  notes: "Requires GOOGLE_ANTIGRAVITY_API_KEY. Commercial service. API availability TBD."
```

**Research Needed:**
- [ ] Check if Antigravity has public API
- [ ] Check if CLI tool available
- [ ] Check MCP server support
- [ ] Verify authentication method

---

### 3. AWS Kiro

**Status:** ⏭️ **Integration Needed**

**Current State:**
- Not yet integrated
- Commercial IDE service (not open-source)

**Integration Approach:**
- **Option A:** AWS SDK integration (if API available)
- **Option B:** AWS CLI integration (if CLI available)
- **Option C:** MCP server integration (if supported)

**Adapter Implementation:**
```python
# src/ybis/adapters/aws_kiro.py
class AWSKiroExecutor:
    """AWS Kiro executor adapter."""
    
    def __init__(self):
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        # Use boto3 or AWS SDK
    
    def is_available(self) -> bool:
        # Check AWS credentials
        return bool(os.getenv("AWS_ACCESS_KEY_ID"))
    
    def execute(self, task: str, context: Dict) -> str:
        # Call Kiro API via AWS SDK
        pass
```

**Registry Entry:**
```yaml
# configs/adapters.yaml
aws_kiro:
  name: "aws_kiro"
  type: "executor"
  module_path: "src.ybis.adapters.aws_kiro.AWSKiroExecutor"
  description: "AWS Kiro AI IDE executor"
  maturity: "experimental"
  dependencies:
    - "boto3>=1.34.0"
  capabilities:
    - "code_generation"
    - "file_editing"
  health_check: "is_available()"
  policy_key: "adapters.aws_kiro.enabled"
  notes: "Requires AWS credentials. Commercial service. API availability TBD."
```

**Research Needed:**
- [ ] Check if Kiro has public API
- [ ] Check AWS SDK support
- [ ] Verify authentication method (IAM, API keys)
- [ ] Check pricing/billing model

---

## Implementation Priority

### Phase 1: Claude Code (Already Supported)
- ✅ **Status:** No action needed (via spec-kit)
- ⏭️ **Optional:** Create direct adapter if needed

### Phase 2: Research Phase
- ⏭️ Research Antigravity API/CLI availability
- ⏭️ Research Kiro API/CLI availability
- ⏭️ Document integration requirements

### Phase 3: Adapter Implementation
- ⏭️ Implement Antigravity adapter (if API available)
- ⏭️ Implement Kiro adapter (if API available)
- ⏭️ Add to adapter registry
- ⏭️ Add to policy profiles

### Phase 4: Testing & Documentation
- ⏭️ Test adapter availability checks
- ⏭️ Test fallback mechanisms
- ⏭️ Document API key setup
- ⏭️ Add to adapter documentation

---

## Policy Configuration

**Default Profile (`configs/profiles/default.yaml`):**
```yaml
adapters:
  claude_code:
    enabled: false  # Opt-in, requires API key
  google_antigravity:
    enabled: false  # Opt-in, requires API key
  aws_kiro:
    enabled: false  # Opt-in, requires AWS credentials
```

**Development Profile (`configs/profiles/dev.yaml`):**
```yaml
adapters:
  claude_code:
    enabled: true  # If API key available
  google_antigravity:
    enabled: false  # TBD based on API availability
  aws_kiro:
    enabled: false  # TBD based on API availability
```

---

## Environment Variables

**Required for Claude Code:**
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

**Required for Google Antigravity:**
```bash
GOOGLE_ANTIGRAVITY_API_KEY=...  # TBD
```

**Required for AWS Kiro:**
```bash
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

---

## Success Criteria

1. ✅ Claude Code accessible via spec-kit (already done)
2. ⏭️ Antigravity adapter created (if API available)
3. ⏭️ Kiro adapter created (if API available)
4. ⏭️ All adapters registered in `configs/adapters.yaml`
5. ⏭️ Policy-based enablement working
6. ⏭️ Fallback to `local_coder` when commercial tools unavailable
7. ⏭️ Documentation updated

---

## Notes

- **These are NOT vendors** - they're commercial services integrated via adapters
- **API availability is TBD** - need to research actual API/CLI availability
- **Fallback is critical** - always fallback to `local_coder` if commercial tools unavailable
- **Cost considerations** - document pricing/billing for each service
- **Security** - API keys must be stored securely (env vars, not in code)

