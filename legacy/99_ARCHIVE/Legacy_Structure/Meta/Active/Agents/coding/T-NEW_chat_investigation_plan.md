# Chat Akışı İnceleme Planı (ClaudeCode için)

## Tespitler (kod okumadan)
- **Çift log/navigasyon**: `apps/mobile/app/(tabs)/chat.tsx` `handleCreateNewChat` sadece `router.push('/(tabs)')` yapıyor; `_layout.tsx` her path değişiminde log atıyor. Dev/Strict Mode veya re-render ile onPress iki kez tetikleniyor olabilir.
- **Boş sohbet davranışı**: Conversation listesi `filter(conv => conv.hasMessages)` ile boş sohbetleri gizliyor. “Yeni sohbet”e basınca liste değişmiyor; conversation DB’ye ilk mesajda ekleniyor.
- **İki farklı useChat**: `src/features/chat/hooks/useChat.ts` (lokal DB + OpenAI) ve `useChat.backend.ts` (chatApi + SSE). Hangisi kullanılacak net değil; `/ (tabs)/index.tsx` şu an ilkini kullanıyor.
- **i18n eksikleri**: `chat.tsx` (liste ekranı), `useChat.ts` (tool call uyarıları), `ChatInput`, `SuggestionPrompts` gibi bileşenlerde kullandığımız `t('chat.*')` anahtarları `packages/i18n/src/locales/tr/mobile.json` içinde yok; fallback string’ler Türkçe ama encode bozuk.

## Yapılacaklar (öncelik sırası)
1) **Navigation/log dedupe**
   - `_layout.tsx`: `lastPathRef` ile ardışık aynı `pathname`’i loglama.
   - `apps/mobile/app/(tabs)/chat.tsx`: `handleCreateNewChat`’e ref-based guard + benzersiz marker (nanoid) ekle. Aynı guard `index.tsx` headerRight pen ikonu için de kullanılacak.

2) **Yeni sohbet akışı kararı**
   - Opsiyon A (minimal değişiklik): Mevcut davranışı koru, ancak onPress guard + toast “Yeni sohbet başlatıldı, ilk mesajı yazın” ekle. Filtre devam ederse UX’i dokümante et.
   - Opsiyon B (deterministik): `handleCreateNewChat`’te DB’ye boş conversation insert et, ID’yi `router.push({ pathname: '/(tabs)', params: { conversationId } })` ile geçir; `useChat` param varsa `loadConversation` çağıracak. Boş sohbetlerin listede görünmesi için `filter(conv => conv.hasMessages)` kaldır veya “0 mesaj” etiketiyle bırak.
   - Hangisi seçilirse STATUS_BOARD’a not düş.

3) **useChat konsolidasyonu**
   - Karar ver: `useChat.backend.ts` (chatApi + SSE) mi yoksa mevcut local OpenAI/DB akışı mı? Öneri: backend versiyonunu kullan, diğeriyle çakışmayı kaldır (dosyayı ya sil ya da `index.tsx` import’unu backend’e taşı).
   - Seçilen hook’ta conversation yaratma ve `conversationId` param yüklemeyi destekle (Opsiyon B yapılırsa).

4) **i18n tamamlama**
   - `packages/i18n/src/locales/tr/mobile.json` ve `en/mobile.json` içine aşağıdaki anahtarları ekle (boş değerler şimdilik İngilizce/Türkçe):
     - `chat.conversations`, `chat.no_conversations`, `chat.start_conversation`, `chat.new_conversation`, `chat.delete_conversation`, `chat.delete_confirmation`, `chat.edit_name`, `chat.enter_new_name`, `chat.calling_tool`, `chat.tool_executed`.
   - Kodda fallback string’leri temizle (doğrudan `t(...)` kullan; gerekiyorsa defaultOptions ile).

5) **Log gözlemi**
   - Guard’lardan sonra loglarda çift marker kaldı mı kontrol et. Dev/prod build farkı için bir kez prod-like build logu al.

## Dosya Referansları
- `apps/mobile/app/_layout.tsx` (navigation logger)
- `apps/mobile/app/(tabs)/chat.tsx` (liste ekranı, yeni sohbet butonu, filtre)
- `apps/mobile/app/(tabs)/index.tsx` (main chat, headerRight yeni sohbet ikonu)
- `apps/mobile/src/features/chat/hooks/useChat.ts` ve `useChat.backend.ts` (hook seçimi)
- `packages/i18n/src/locales/tr/mobile.json` ve `.../en/mobile.json` (i18n ekleri)
