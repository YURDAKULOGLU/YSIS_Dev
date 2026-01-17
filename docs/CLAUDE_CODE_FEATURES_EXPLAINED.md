# Claude Code Özellikleri - Detaylı Açıklama

**Date:** 2026-01-10  
**Purpose:** Skills, Commands, Hooks'un tam olarak ne işe yaradığını açıklamak

---

## Genel Bakış

Claude Code'un 3 ana özelleştirme mekanizması var:

1. **Commands** - Manuel tetiklenen özel komutlar
2. **Skills** - Otomatik tetiklenen yetenekler
3. **Hooks** - Tool çağrılarını intercept eden güvenlik/izleme katmanı

---

## 1. COMMANDS (Custom Commands)

### Ne İşe Yarar?

**Commands**, kullanıcının manuel olarak tetiklediği özel komutlardır. `/project:command-name` formatında kullanılır.

### Nasıl Çalışır?

```
Kullanıcı: /project:ybis-full-cycle TASK-123
    ↓
Claude Code: .claude/commands/ybis-full-cycle.md dosyasını okur
    ↓
Command içindeki talimatları takip eder
    ↓
8 fazlı execution: Task → Analysis → Plan → Implement → Test → Verify → Commit → Report
    ↓
Sonuç: Task tamamlandı, rapor oluşturuldu
```

### Ne Zaman Kullanılır?

**Commands kullan:**
- ✅ Belirli bir iş akışını tekrar tekrar çalıştırırken
- ✅ Standart bir süreç varsa (örn: full cycle development)
- ✅ Kullanıcı açıkça komutu çağırdığında
- ✅ Kompleks, çok adımlı işlemler için

**Commands kullanma:**
- ❌ Otomatik tetiklenmesi gereken durumlar (Skills kullan)
- ❌ Her tool çağrısında çalışması gereken şeyler (Hooks kullan)

### YBIS Örneği

**Command:** `ybis-full-cycle.md`

**Kullanım:**
```bash
/project:ybis-full-cycle TASK-123
```

**Ne Yapar:**
1. Task'ı claim eder
2. Codebase'i analiz eder
3. Plan oluşturur
4. Kodu implement eder
5. Test eder
6. Verify eder
7. Commit eder
8. Rapor oluşturur

**Avantajları:**
- ✅ Tek komutla tüm süreç
- ✅ Standart workflow
- ✅ Tekrarlanabilir
- ✅ Dokümante edilmiş

---

## 2. SKILLS (Auto-Triggered Capabilities)

### Ne İşe Yarar?

**Skills**, belirli koşullar sağlandığında otomatik olarak aktive olan yeteneklerdir. Kullanıcı açıkça çağırmaz, sistem otomatik algılar.

### Nasıl Çalışır?

```
Kullanıcı: "YBIS task T-abc123'ü çalıştır"
    ↓
Claude Code: Skills klasöründeki tüm skill'leri kontrol eder
    ↓
ybis-task-executor.md skill'i trigger pattern'ları kontrol eder:
    - Pattern: "YBIS task" ✅ Match!
    - Pattern: "run task T-XXX" ✅ Match!
    - Keyword: "YBIS" ✅ Match!
    ↓
Skill otomatik aktive olur
    ↓
Skill execution flow başlar:
    1. Task'ı claim et
    2. Execute et
    3. Report et
    ↓
Sonuç: Task otomatik çalıştırıldı
```

### Ne Zaman Kullanılır?

**Skills kullan:**
- ✅ Kullanıcı belirli konulardan bahsettiğinde otomatik aktive olması gereken durumlar
- ✅ Context'e göre otomatik öneriler
- ✅ Pattern matching ile akıllı algılama
- ✅ Kullanıcı farkında olmadan yardımcı olmak

**Skills kullanma:**
- ❌ Her zaman çalışması gereken şeyler (Hooks kullan)
- ❌ Manuel tetiklenmesi gereken durumlar (Commands kullan)

### YBIS Örneği

**Skill:** `ybis-task-executor.md`

**Trigger Koşulları:**
- Pattern: "YBIS task", "run task T-XXX"
- Files: `control_plane.db`, `PLAN.md`, `RESULT.md` açıksa
- Keywords: "YBIS", "task execution", "workflow run"
- Context: YBIS MCP server mevcut

**Kullanım:**
```
Kullanıcı: "YBIS'teki pending task'ları göster"
→ Skill aktive olur
→ get_tasks MCP tool'unu çağırır
→ Task listesini gösterir
```

**Avantajları:**
- ✅ Otomatik algılama
- ✅ Kullanıcı farkında olmadan yardım
- ✅ Context-aware
- ✅ Çoklu trigger tipi

---

## 3. HOOKS (Interceptors)

### Ne İşe Yarar?

**Hooks**, Claude Code'un tool çağrılarını intercept eden, güvenlik kontrolü, logging, ve monitoring yapan katmanlardır.

### Nasıl Çalışır?

```
Claude: "Edit dosya.py" tool'unu çağırmak istiyor
    ↓
PreToolUse Hook çalışır:
    - Dosya korumalı mı? ✅ Kontrol
    - Rate limit aşıldı mı? ✅ Kontrol
    - Input güvenli mi? ✅ Kontrol
    ↓
Hook kararı: "allow" veya "block"
    ↓
Eğer "allow":
    → Tool çalışır
    ↓
PostToolUse Hook çalışır:
    - Tool başarılı mı? ✅ Kontrol
    - Metrics kaydet
    - Audit log yaz
    ↓
Sonuç: Tool güvenli şekilde çalıştı, loglandı
```

### Hook Tipleri

#### 1. PreToolUse (Önce)
**Ne zaman:** Her tool çağrısından ÖNCE
**Ne yapar:**
- ✅ Güvenlik kontrolü (protected files, dangerous commands)
- ✅ Rate limiting
- ✅ Input validation
- ✅ Input sanitization
- ✅ Block/Allow kararı

**Örnek:**
```python
# PreToolUse hook
if file_path == "docs/governance/YBIS_CONSTITUTION.md":
    return {"decision": "block", "reason": "Protected file"}
```

#### 2. PostToolUse (Sonra)
**Ne zaman:** Her tool çağrısından SONRA
**Ne yapar:**
- ✅ Error detection
- ✅ Performance metrics
- ✅ Success/failure tracking
- ✅ Audit logging
- ✅ Cleanup operations

**Örnek:**
```python
# PostToolUse hook
if tool_output["exit_code"] != 0:
    log_error(tool_name, tool_output)
    track_metrics(tool_name, duration, success=False)
```

#### 3. Notification (Bildirim)
**Ne zaman:** Bildirim gönderildiğinde
**Ne yapar:**
- ✅ Notification routing
- ✅ Alert filtering
- ✅ Multi-channel support (console, file, webhook)
- ✅ Priority handling

**Örnek:**
```python
# Notification hook
if notification_type == "error":
    send_to_slack(notification)
    send_to_email(notification)
```

#### 4. Stop (Durdurma)
**Ne zaman:** Claude durduğunda
**Ne yapar:**
- ✅ Session cleanup
- ✅ Final reporting
- ✅ Resource release
- ✅ State persistence

**Örnek:**
```python
# Stop hook
cleanup_temp_files()
save_session_summary()
release_resources()
```

### Ne Zaman Kullanılır?

**Hooks kullan:**
- ✅ Her tool çağrısında çalışması gereken şeyler
- ✅ Güvenlik kontrolleri
- ✅ Logging ve monitoring
- ✅ Rate limiting
- ✅ Input validation

**Hooks kullanma:**
- ❌ Kullanıcı tarafından tetiklenen işlemler (Commands kullan)
- ❌ Otomatik algılama gereken durumlar (Skills kullan)

### YBIS Örneği

**PreToolUse Hook:**
```python
# Kullanıcı: "Edit docs/governance/YBIS_CONSTITUTION.md"
# Hook: BLOCK
# Reason: "Protected file cannot be edited"
```

**PostToolUse Hook:**
```python
# Tool: Bash("rm -rf /tmp/test")
# Hook: Metrics kaydet (duration: 0.5s, success: true)
# Hook: Audit log yaz
```

---

## Karşılaştırma Tablosu

| Özellik | Commands | Skills | Hooks |
|---------|----------|--------|-------|
| **Tetikleme** | Manuel (`/project:command`) | Otomatik (pattern match) | Otomatik (her tool çağrısı) |
| **Kullanıcı Farkındalığı** | Açıkça çağırır | Farkında olmayabilir | Görünmez (arka planda) |
| **Kullanım Amacı** | Standart iş akışları | Context-aware yardım | Güvenlik & monitoring |
| **Çalışma Sıklığı** | İhtiyaç olduğunda | Koşul sağlandığında | Her tool çağrısında |
| **Kontrol Seviyesi** | Yüksek (kullanıcı kontrolü) | Orta (otomatik ama öneri) | Düşük (görünmez) |
| **Örnek** | `/project:ybis-full-cycle` | "YBIS task" dediğinde | Her Edit/Write/Bash çağrısında |

---

## Pratik Örnekler

### Senaryo 1: Task Çalıştırma

**Command Yaklaşımı:**
```
Kullanıcı: /project:ybis-full-cycle TASK-123
→ Command çalışır
→ 8 fazlı execution
→ Sonuç raporlanır
```

**Skill Yaklaşımı:**
```
Kullanıcı: "YBIS task TASK-123'ü çalıştır"
→ Skill otomatik algılar
→ Task'ı çalıştırır
→ Sonuç raporlanır
```

**Fark:** Command açıkça çağrılır, Skill otomatik algılar.

### Senaryo 2: Güvenlik Kontrolü

**Hook Yaklaşımı:**
```
Kullanıcı: "Edit docs/governance/YBIS_CONSTITUTION.md"
→ PreToolUse hook çalışır
→ Protected file tespit eder
→ BLOCK kararı
→ Kullanıcıya: "Protected file cannot be edited"
```

**Neden Hook?** Çünkü her Edit çağrısında çalışması gerekiyor.

### Senaryo 3: Otomatik Yardım

**Skill Yaklaşımı:**
```
Kullanıcı: "Test sonuçlarını kontrol et"
→ Test skill'i aktive olur (eğer test dosyaları varsa)
→ Test sonuçlarını analiz eder
→ Öneriler sunar
```

**Neden Skill?** Çünkü context'e göre otomatik algılanması gerekiyor.

---

## YBIS'teki Kullanım

### Commands
- ✅ `ybis-full-cycle` - Tam döngü task execution
- ✅ Kullanım: `/project:ybis-full-cycle TASK-123`

### Skills
- ✅ `ybis-task-executor` - Otomatik task detection ve execution
- ✅ Trigger: "YBIS task", "run task", "claim task" dediğinde

### Hooks
- ✅ `pre_tool_use` - Güvenlik, rate limiting, validation
- ✅ `post_tool_use` - Metrics, error detection, logging
- ✅ `notification` - Alert routing
- ✅ `stop` - Session cleanup

---

## Özet

### Commands = Manuel Tetiklenen İş Akışları
- Kullanıcı açıkça çağırır
- Standart süreçler için
- Örnek: `/project:ybis-full-cycle`

### Skills = Otomatik Algılanan Yetenekler
- Sistem otomatik algılar
- Context-aware yardım için
- Örnek: "YBIS task" dediğinde aktive olur

### Hooks = Görünmez Güvenlik Katmanı
- Her tool çağrısında çalışır
- Güvenlik ve monitoring için
- Örnek: Protected file kontrolü

---

## Sonuç

**Commands:** "Ne yapmak istediğini söyle, ben yaparım"  
**Skills:** "Ne yapmaya çalıştığını anlıyorum, yardım edeyim"  
**Hooks:** "Her şeyi güvenli tutuyorum, sen farkında olmayabilirsin"

**Hepsi birlikte:** Claude Code'u güçlü, güvenli ve akıllı bir platform yapar! 🚀

