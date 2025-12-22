# Talimat: Chat Navigasyon & Yeni Sohbet Akışı Dedupe (ClaudeCode)

## Bağlam
Loglarda aynı anda iki kez “Starting new conversation” ve “Navigation to /” görüyoruz. Kod akışı:
- `apps/mobile/app/(tabs)/chat.tsx` > `handleCreateNewChat`: sadece `router.push('/(tabs)')` + `Logger.info('Starting new conversation')`.
- `_layout.tsx` > `useEffect` ile `Logger.info(\`Navigation to ${pathname}\`)` her pathname değişiminde.
- `apps/mobile/app/(tabs)/index.tsx` > `useChat.handleNewChat` sadece state temizliyor; conversation DB’ye ilk mesajda ekleniyor.

Muhtemel nedenler: React Native dev/Strict Mode çift çağrısı, onPress’in birden fazla tetiklenmesi (re-render), navigation log effect’in dedupesiz olması, UX’te boş sohbetlerin listede filtrelenmesi (kullanıcı “Yeni sohbet”e basınca liste değişmiyor).

## Hedef
Çift log/çift navigasyon tetiklemelerini engelle, yeni sohbet akışını deterministik yap, gerekirse boş sohbet davranışını netleştir.

## Yapılacaklar
1) **Logging dedupe (opsiyonel ama önerilir)**  
   - `_layout.tsx` navigation logger’a son path’i hatırlayan bir ref ekle; aynı pathname art arda geliyorsa loglama.
     ```ts
     const lastPathRef = useRef<string>();
     useEffect(() => {
       if (lastPathRef.current === pathname) return;
       lastPathRef.current = pathname;
       Logger.info(`Navigation to ${pathname}`, { ... });
     }, [pathname, segments]);
     ```
2) **Yeni sohbet onPress guard**  
   - `apps/mobile/app/(tabs)/chat.tsx` içindeki `handleCreateNewChat`’e ref tabanlı guard ekle:
     ```ts
     const creatingRef = useRef(false);
     const handleCreateNewChat = useCallback(() => {
       if (creatingRef.current) return;
       creatingRef.current = true;
       router.push('/(tabs)');
       Logger.info('Starting new conversation', { type: 'USER_ACTION', nonce: nanoid() });
       setTimeout(() => { creatingRef.current = false; }, 400);
     }, [router]);
     ```
   - Aynı guard’ı Navbar’daki pen ikonu için de kullan (index.tsx headerRight).
3) **Yeni sohbet akışının netleştirilmesi**  
   - Opsiyon A (en hızlı): Şimdiki davranışı koru ama UX mesajı ekle (boş liste state’inde “Yeni sohbet açıldı, ilk mesajı yazın” toast).  
   - Opsiyon B (daha deterministik): `handleCreateNewChat` içinde hemen boş conversation oluştur (DB insert) ve ID’yi `/ (tabs)`’e parametre olarak gönder; `useChat` param varsa `loadConversation` çağırır, yoksa yeni chat mode’a geçer. Bu, “listeye yansımıyor” şikayetini çözer ama boş sohbetlerin listede görünmesi için filtreyi kaldırman gerekir.
4) **Conversation listesi filtre düzeltmesi (isteğe bağlı)**  
   - `chat.tsx`’te `filter(conv => conv.hasMessages)` boş sohbetleri gizliyor. Boş sohbetlerin görünmesini istiyorsan filtreyi kaldır ya da minimum 1 mesaj şartını UX kararı olarak dokümante et.
5) **İzleme için marker ekle**  
   - `Logger.info('Starting new conversation', { type: 'USER_ACTION', marker: nanoid() })` gibi benzersiz marker ekle; logda çift marker varsa çift handler tetikleniyor demektir.

## Test Notları
- Dev/Prod farkını kontrol et: Expo dev’de React Strict Mode çift render yapar; guard’ların çalıştığını doğrula.
- Yeni sohbet akışında: butona çift tıklayınca ikinci navigasyon olmamalı; loglar tek olmalı.
- Eğer Opsiyon B uygulanırsa: yeni conversation ID’siyle `/ (tabs)?conversationId=...` rotasına gidildiğini, `useChat`’in `loadConversation` çağırdığını ve listeye (filtre kaldırıldıysa) eklendiğini doğrula.

## Dosya Referansları
- `apps/mobile/app/_layout.tsx` (navigation logger)
- `apps/mobile/app/(tabs)/chat.tsx` (conversation listesi ve yeni sohbet butonu)
- `apps/mobile/app/(tabs)/index.tsx` (main chat ekranı, headerRight pen ikonu)
- `apps/mobile/src/features/chat/hooks/useChat.ts` (handleNewChat ve conversation yükleme)
