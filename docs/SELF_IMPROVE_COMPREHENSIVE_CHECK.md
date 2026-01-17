# Self-Improve Workflow Kapsamlı Kontrol Raporu

**Tarih:** 2026-01-12  
**Kontrol Edilen:** Self-Improve Workflow State Management

## 1. WorkflowState TypedDict ✅

**Dosya:** `src/ybis/orchestrator/graph.py`

```python
class WorkflowState(TypedDict, total=False):
    # ... existing fields ...
    # Self-improve workflow specific state
    repair_retries: int  # Number of repair attempts in self-improve workflow
    max_repair_retries: int  # Maximum repair retry attempts
    repair_failed: bool  # Flag indicating repair failed
    repair_max_retries_reached: bool  # Flag indicating max repair retries reached
    test_passed: bool  # Flag indicating tests passed
    lint_passed: bool  # Flag indicating lint passed
    tests_passed: bool  # Flag indicating unit tests passed
```

**Durum:** ✅ **DOĞRU**
- `total=False` ile optional keys destekleniyor
- Tüm self-improve state key'leri tanımlı
- LangGraph bu key'leri state'te koruyacak

## 2. Repair Node State Management ✅

**Dosya:** `src/ybis/orchestrator/self_improve.py` (satır 690-947)

### 2.1 Initialization
```python
if "repair_retries" not in state:
    state["repair_retries"] = 0
if "max_repair_retries" not in state:
    state["max_repair_retries"] = 3
```
**Durum:** ✅ **DOĞRU**

### 2.2 Retry Check
```python
retries = state.get("repair_retries", 0)
max_repair_retries = state.get("max_repair_retries", 3)

if retries >= max_repair_retries:
    state["repair_max_retries_reached"] = True
    state["test_passed"] = True
    return state
```
**Durum:** ✅ **DOĞRU**

### 2.3 Increment
```python
new_retries = retries + 1
state["repair_retries"] = new_retries
```
**Durum:** ✅ **DOĞRU** - State'te increment ediliyor

### 2.4 Return
```python
return state
```
**Durum:** ✅ **DOĞRU** - State return ediliyor

## 3. Implement Node State Preservation ⚠️

**Dosya:** `src/ybis/orchestrator/self_improve.py` (satır 467-597)

### 3.1 State Updates
```python
state["status"] = "running"
return state
```

**Durum:** ⚠️ **POTANSİYEL SORUN**
- Sadece `status` set ediliyor
- `repair_retries` ve diğer key'ler **açıkça korunmuyor**
- Ancak LangGraph state merge yapıyorsa, bu sorun olmayabilir

**Öneri:** LangGraph'in state merge davranışını test etmek gerekiyor.

## 4. Test Node State Updates ✅

**Dosya:** `src/ybis/orchestrator/self_improve.py` (satır 600-656)

```python
state["test_passed"] = test_passed
state["lint_passed"] = verifier_report.lint_passed
state["tests_passed"] = verifier_report.tests_passed
state["test_errors"] = verifier_report.errors or []
state["test_warnings"] = verifier_report.warnings or []
```

**Durum:** ✅ **DOĞRU** - Tüm test flags set ediliyor

## 5. Conditional Routing ✅

**Dosya:** `src/ybis/workflows/conditional_routing.py` (satır 111-145)

### 5.1 Max Retries Check
```python
if state.get("repair_max_retries_reached", False):
    return "integrate"
```

**Durum:** ✅ **DOĞRU**

### 5.2 Retry Limit Check
```python
repair_retries = state.get("repair_retries", 0)
max_repair_retries = state.get("max_repair_retries", 3)

if repair_retries >= max_repair_retries:
    return "integrate"
```

**Durum:** ✅ **DOĞRU**

### 5.3 Route to Repair
```python
logger.info(f"Tests failed, routing to repair (attempt {repair_retries + 1}/{max_repair_retries})")
return "repair"
```

**Durum:** ✅ **DOĞRU**

## 6. Workflow YAML Configuration ⚠️

**Dosya:** `configs/workflows/self_improve.yaml`

```yaml
- from: test
  to: integrate
  condition: test_failed

- from: test
  to: repair
  condition: test_failed
```

**Durum:** ⚠️ **POTANSİYEL SORUN**
- İki connection aynı condition (`test_failed`) ile
- LangGraph bunu nasıl handle ediyor?
- `test_failed` fonksiyonu `"integrate"` veya `"repair"` döndürüyor, bu doğru
- Ancak YAML'da `route` key'i yok, bu bir sorun olabilir

**Kontrol:** `src/ybis/workflows/runner.py`'de conditional routing nasıl handle ediliyor?

## 7. LangGraph State Merge Behavior ❓

**Sorun:** LangGraph TypedDict state'i nasıl merge ediyor?

**Beklenti:**
- Node'dan return edilen state, mevcut state ile merge edilmeli
- TypedDict'te tanımlı key'ler korunmalı
- `total=False` ile optional key'ler de korunmalı

**Test Gerekiyor:**
1. Repair node `repair_retries = 1` set ediyor
2. Implement node sadece `status = "running"` set ediyor
3. Test node `repair_retries`'i okuduğunda 1 olmalı

## 8. Tespit Edilen Sorunlar

### 8.1 Implement Node State Preservation
**Sorun:** `implement_node` sadece `status` set ediyor, diğer state key'lerini açıkça korumuyor.

**Çözüm Önerisi:**
```python
# implement_node içinde
# State'i korumak için açıkça merge et
state = {**state, "status": "running"}
# veya
# LangGraph'in merge davranışına güven (eğer çalışıyorsa)
```

### 8.2 Workflow YAML Route Key
**Sorun:** YAML'da `route` key'i yok, sadece `condition` var.

**Kontrol:** `runner.py`'de conditional routing nasıl handle ediliyor?

## 9. Öneriler

1. **LangGraph State Merge Test:**
   - Repair node'da `repair_retries = 1` set et
   - Implement node'da sadece `status` set et
   - Test node'da `repair_retries`'i oku ve kontrol et

2. **Implement Node State Preservation:**
   - Eğer LangGraph merge yapmıyorsa, implement node'da state'i açıkça koru

3. **Workflow YAML Route Key:**
   - `runner.py`'de conditional routing logic'ini kontrol et
   - Eğer `route` key'i gerekiyorsa, YAML'ı güncelle

4. **Debug Logging:**
   - Her node'da state'i logla
   - `repair_retries` değerini her adımda kontrol et

## 10. Sonuç

**Genel Durum:** ⚠️ **POTANSİYEL SORUNLAR VAR**

**Ana Sorun:** LangGraph'in state merge davranışı belirsiz. Implement node state'i açıkça korumuyor.

**Öncelikli Aksiyon:**
1. LangGraph state merge davranışını test et
2. Implement node'da state preservation ekle (gerekirse)
3. Workflow YAML route key kontrolü yap

