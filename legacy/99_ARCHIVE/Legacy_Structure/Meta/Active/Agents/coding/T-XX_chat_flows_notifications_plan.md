# Plan: Chat (Supabase) İyileştirme + Notification Hook + Çekirdek Flows (ClaudeCode)

## Hedef (bugün)
1) Chat iyileştirme: Supabase `useChat.ts` içinde deterministik conversation create/select/delete akışı.
2) Notification hook: Asgari lokal push/hook; izin/uyarı UX.
3) Çekirdek Flows: Manual/schedule tetik + 3–4 basit template; CRUD + manual run çalışır.

## Detay Adımlar
### 1) Chat (Supabase) İyileştirme (≈2h)
- `apps/mobile/src/features/chat/hooks/useChat.ts`: “Yeni sohbet” deterministik; butonda veya ilk mesajda Supabase’e insert, ID ile `/ (tabs)?conversationId=...` push; `loadConversation` bu ID’yi kullanır.
- Mevcut sohbeti yükleme/seçme/silme akışı tutarlı; boş sohbet oluşumundan kaçınmak için guard + insert politikası netleştir.
- Auto-title/rename (ilk mesajdan) opsiyonel ama destekleniyorsa kırma.
- Smoke: Yeni sohbet → mesaj → app kapan-aç → doğru thread yükleniyor.

### 2) Notification Hook (≈1.5h)
- Asgari lokal push: due/approaching Task/Event için izin iste + schedule trigger veya hook fonksiyonu; UI’da izin/uyarı göster.
- Chat/tool call sonrası minimal “AI çalışıyor/işlem bitti” feedback (UI içinde) ekle.

### 3) Çekirdek Flows (≈3–4h)
- Veri modeli: Flow (manual/schedule trigger, basit actions) Supabase’de sakla.
- API: Hono endpoints list/create/run (manual), schedule alanı (cron) kaydedilir; ileri işlem stub olabilir.
- Template set (kaydedilmiş veya hazır): günlük özet, kargo tracking, overdue reminder (opsiyonel haftalık rapor). Parametreler statik, karmaşık koşul yok.
- Chat entegrasyonu: tool veya UI butonuyla “run flow {id}”; sonuç/log göster.
- Smoke: Flow oluştur → manual run → log/output görülüyor; schedule alanı kaydoluyor.

## Kabul Kriterleri
- Chat Supabase hook kullanıyor; deterministik conversation create/select/delete; navigation doğru.
- Supabase Auth (email/Google) bozulmadan çalışıyor; chat markdown + i18n korunuyor.
- Bildirim için izin/hook hazır; en az bir due/approaching senaryosunda lokal push veya çağrılabilir fonksiyon mevcut.
- Flows: CRUD + manual run çalışıyor; ≥3 template kayıtlı; schedule alanı kaydediliyor (cron), ileri işlenmese de veri modelinde hazır.
- Hızlı smoke: Auth → Chat → tool call → Task/Note CRUD → Flow manual run → bildirim izin kontrolü; sonuçlar raporlanır.
