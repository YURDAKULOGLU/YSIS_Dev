# Flow Execution Fix - Test Plan

## ✅ Migration Applied
Database schema confirmed with `flow_executions` and `flow_execution_steps` tables.

## 🧪 Test Steps

### 1. Mobile App Test (REQUIRED)
**Bu testi SİZ yapmalısınız - mobile app'te:**

1. **Flow Oluştur/Seç**
   - Flows ekranına git
   - Mevcut bir flow seç veya yeni bir template'ten flow oluştur
   - Örnek: "Morning Routine" veya "Focus Mode" template'i

2. **Flow'u Çalıştır**
   - Flow'un yanındaki "Run" butonuna tıkla
   - Console log'larını izle (React Native Debugger veya Expo Go)

3. **Beklenen Sonuçlar**
   - ✅ `[USER_ACTION] User triggered flow run` logu görünmeli
   - ✅ `[FLOW_ENGINE] Starting execution: <flow_name>` logu görünmeli
   - ✅ `[FLOW_ENGINE] Flow execution record created` logu görünmeli
   - ✅ `[FLOW_ENGINE] Executing step` logları görünmeli
   - ✅ `[FLOW_ENGINE] Flow execution completed successfully` logu görünmeli
   - ✅ Toast notification: "Flow completed!" veya benzeri
   - ✅ Flow'un oluşturduğu not/task/event DB'de görünmeli

4. **Önceki Hata (Artık Olmamalı)**
   - ❌ `[USER_ACTION]` logdan sonra sessizlik
   - ❌ Hiç step logu olmaması
   - ❌ Flow sonsuza kadar "running" durumunda kalması

### 2. Database Inspection (Script ile)
Flow çalıştırdıktan sonra:

```bash
# Latest execution'ı incele
npx tsx scripts/inspect-flow.ts
```

**Beklenen Output:**
```
🔍 Inspecting Flow Execution: <execution_id>

📋 Flow: Morning Routine (or whatever you ran)
Status: COMPLETED
Duration: 1.2s
Started: 2025-12-04 ...
----------------------------------------

[1] Step: tool (tool)
   Status: completed | Duration: 0.8s
   📥 Input: {...}
   📤 Output: {...}

[2] Step: output_notification (output)
   Status: completed | Duration: 0.4s
   📥 Input: {...}
   📤 Output: {...}

----------------------------------------
```

### 3. Error Case Test (Optional)
Test bir flow'un başarısız olması durumunu:

1. Supabase'de workspace_id'yi geçici olarak invalid yap
2. Flow çalıştır
3. Error logları ve DB'de `status: 'failed'` olmalı
4. `error_message` dolu olmalı

---

## 📊 Success Criteria

- [x] Migration başarıyla uygulandı (tablo yapısı doğru)
- [ ] Flow execution DB'ye kaydediliyor
- [ ] Steps DB'ye loglanıyor
- [ ] Execution tamamlanıyor (completed/failed)
- [ ] inspect-flow tool trace gösteriyor
- [ ] UI doğru status'u yansıtıyor

---

## 🐛 Sorun Çıkarsa

1. **Console log'larını kontrol edin**
   - `Failed to create flow execution record` var mı?
   - Başka RLS hataları var mı?

2. **Database'i kontrol edin**
   ```bash
   # En son execution kayıtlarını göster
   npx tsx scripts/inspect-flow.ts
   ```

3. **RLS policy'lerini doğrulayın**
   - Supabase Dashboard > Database > Policies
   - `flow_executions` için 3 policy olmalı: SELECT, INSERT, UPDATE
   - `flow_execution_steps` için 3 policy olmalı: SELECT, INSERT, UPDATE

---

**Lütfen mobile app'te bir flow çalıştırıp sonucu paylaşın!** 🚀
