# Framework Documentation Quality Gate

> Hataların tekrarlanmaması için otomatik kontrol mekanizması

---

## Problem

Framework dokümanları indirilirken hatalar oluşuyor:
- SPADE dokümanları indirilemedi (GitHub fallback çalışmıyor)
- RAG ingestion hatası (add_document() missing argument)
- Eski framework'lerin dokümanları eksik (crewai, autogen, swarm, autogpt)

**Sonuç:** Framework'ler kuruluyor ama dokümanlar RAG'e eklenmiyor, agent'lar framework bilgisine erişemiyor.

---

## Solution: Quality Gate + Golden Task

### 1. Quality Gate: Framework Installation Verification

Her framework kurulumundan sonra otomatik kontrol:

```python
# scripts/verify_framework_installation.py
def verify_framework_installation(framework_name: str) -> dict:
    """Verify framework installation and documentation."""
    results = {
        "framework": framework_name,
        "package_installed": False,
        "docs_downloaded": False,
        "docs_count": 0,
        "rag_ingested": False,
        "errors": []
    }
    
    # 1. Check package installation
    try:
        __import__(framework_name)
        results["package_installed"] = True
    except ImportError:
        results["errors"].append(f"Package {framework_name} not installed")
    
    # 2. Check documentation
    docs_dir = Path(f"Knowledge/Frameworks/{framework_name}/docs")
    if docs_dir.exists():
        md_files = list(docs_dir.rglob("*.md"))
        results["docs_count"] = len(md_files)
        results["docs_downloaded"] = results["docs_count"] > 0
    else:
        results["errors"].append(f"Docs directory not found: {docs_dir}")
    
    # 3. Check RAG ingestion
    try:
        from src.agentic.tools.local_rag import get_local_rag
        rag = get_local_rag()
        if rag and rag.is_available():
            # Search for framework docs in RAG
            results_rag = rag.search(f"framework:{framework_name}", limit=1)
            results["rag_ingested"] = "No relevant context" not in results_rag
    except Exception as e:
        results["errors"].append(f"RAG check failed: {e}")
    
    return results
```

### 2. Golden Task: Framework Documentation Download

**Task ID:** `GOLDEN-FRAMEWORK-DOCS-001`

**Purpose:** Ensure all framework documentation is downloaded and ingested into RAG.

**Verification:**
```bash
python scripts/verify_framework_installation.py --all
```

**Success Criteria:**
- All installed frameworks have documentation
- All documentation is ingested into RAG
- No errors in installation logs

### 3. Pre-Installation Check: Open Source Verification

**Rule:** Sadece açık kaynak framework'ler kurulacak.

**Check:**
```python
# scripts/check_framework_license.py
FRAMEWORK_LICENSES = {
    "temporalio": "MIT",
    "ray": "Apache-2.0",
    "prefect": "Apache-2.0",
    "spade": "MIT",
    "celery": "BSD-3-Clause",
    "crewai": "MIT",
    "pyautogen": "MIT",  # Microsoft AutoGen - MIT License
    "swarm": "MIT",
    "autogpt": "MIT",
    "langgraph": "MIT",
    "litellm": "Apache-2.0",
    "instructor": "MIT",
    "ollama": "MIT",
}

def verify_license(framework_name: str) -> bool:
    """Verify framework is open source."""
    if framework_name not in FRAMEWORK_LICENSES:
        # Check GitHub for license
        # If no license found, reject
        return False
    return True
```

**AutoGen License Check:**
- ✅ **MIT License** (Open Source)
- ✅ **Microsoft AutoGen** - Açık kaynak, MIT lisansı
- ✅ **Kurulabilir**

---

## Implementation

### Step 1: Fix RAG Ingestion

**File:** `scripts/install_framework.py`

**Fix:**
- `add_document()` requires `doc_id` parameter
- Use recursive glob for all markdown files
- Generate unique doc_id from file path

### Step 2: Fix SPADE Documentation

**Problem:** GitHub fallback not working for SPADE

**Solution:**
- Check SPADE GitHub repo structure
- Use correct repo path: `javipalanca/spade`
- Recursive download for docs/ folder

### Step 3: Download Missing Documentation

**Missing:**
- AutoGen (pyautogen)
- Swarm
- AutoGPT
- LangGraph
- LiteLLM
- Instructor
- Ollama

**Action:**
```bash
python scripts/install_framework.py pyautogen
python scripts/install_framework.py swarm
python scripts/install_framework.py autogpt
# etc.
```

### Step 4: Create Verification Script

**File:** `scripts/verify_framework_installation.py`

**Purpose:**
- Verify all frameworks have documentation
- Verify all documentation is in RAG
- Report missing or failed installations

### Step 5: Create Golden Task

**File:** `docs/GOLDEN_TASKS.md`

**Add:**
```markdown
## GOLDEN-FRAMEWORK-DOCS-001: Framework Documentation Verification

**Purpose:** Ensure all framework documentation is downloaded and ingested.

**Verification:**
```bash
python scripts/verify_framework_installation.py --all
```

**Success Criteria:**
- All installed frameworks have docs
- All docs are in RAG
- No errors
```

---

## Prevention: Automated Checks

### 1. Pre-Commit Hook

**File:** `.git/hooks/pre-commit`

**Check:**
- Framework installation includes docs
- RAG ingestion successful
- License verification passed

### 2. CI/CD Check

**File:** `.github/workflows/framework-check.yml`

**Action:**
- Run `verify_framework_installation.py` on every PR
- Fail if any framework missing docs
- Fail if RAG ingestion failed

### 3. Periodic Verification

**Cron Job:** Weekly framework documentation check

**Command:**
```bash
python scripts/verify_framework_installation.py --all --fix
```

---

## Status

**Fixed:**
- ✅ RAG ingestion parameter fix (doc_id added)
- ✅ Recursive markdown file search
- ✅ Framework license verification

**Pending:**
- ⏳ SPADE documentation download fix
- ⏳ Missing framework documentation download
- ⏳ Verification script creation
- ⏳ Golden task creation

---

## Next Steps

1. Fix RAG ingestion in `install_framework.py`
2. Download AutoGen documentation
3. Fix SPADE documentation download
4. Create verification script
5. Create golden task
6. Add pre-commit hook
7. Run verification for all frameworks

