# Conversation History Architecture (T-006)

## Amaç
Tek oturum yerine çoklu sohbet geçmişi sağlamak: listeleme, oluşturma, seçme, silme; boş/yükleniyor/hata durumları ile birlikte mobil (öncelikli) ve web için aynı veri modeli.

## Varsayımlar
- Depolama: Supabase Postgres + mevcut mesaj tablosu (message.conversation_id zaten varsa yeniden kullan; yoksa migration eklenir).
- Backend: Hono tabanlı API katmanı mevcut; yeni uçlar eklenebilir.
- Kimlik: kullanıcı oturumu Supabase auth ile sağlanıyor; tüm sorgular user_id ile scoped.

## Veri Modeli
`conversations` tablosu (Supabase)
```
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id UUID NOT NULL -- auth.users.uid
title TEXT NOT NULL DEFAULT 'New chat'
last_message TEXT NULL
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
```
- **Indexler:** (user_id, updated_at DESC)
- **RLS:** user_id = auth.uid()

`messages` (mevcut) için gereksinim: `conversation_id UUID NOT NULL REFERENCES conversations(id)`; yoksa migration ile ekle, eski verileri tek conversation’a taşımak için fallback script eklenir.

## API Sözleşmeleri
Tüm uçlar auth zorunlu (Supabase JWT). JSON cevapları `{ data, error }` konvansiyonu ile.

- `GET /api/conversations?limit=50&cursor=<timestamp|id>` → `[ { id, title, lastMessage, updatedAt } ]`
- `POST /api/conversations` body `{ title?: string }` → `{ id, title, updatedAt }`
- `DELETE /api/conversations/:id` → 204
- `PATCH /api/conversations/:id/title` body `{ title }` → 200 (opsiyonel; UX gerekiyorsa)

Backend detay:
- Supabase client’ı server-side kullan; RLS açık olduğundan user_id filtrelenir.
- `lastMessage` alanını mesaj insert trigger’ı ile veya listelerken `SELECT ... ORDER BY created_at DESC LIMIT 1` ile doldur (performans için trigger önerilir).

## Mobil/Web Uygulama Gereksinimleri
- **Liste ekranı:** başlık, son mesaj önizlemesi, güncellenme zamanı; boş ve yükleniyor skeleton; hata yeniden dene butonu.
- **Oluşturma:** “Yeni sohbet” butonu; POST → yeni id; state: `activeConversationId` güncellenir, mesaj listesi resetlenir.
- **Seçme:** listedeki öğe tıklanınca aktif id değişir, mesajlar o id ile fetch edilir.
- **Silme:** kaydır-sil veya menü; DELETE sonrası liste ve aktif durum güncellenir (silinen aktifse, otomatik yeni sohbet oluştur veya boş ekran).
- **Optimistic UI:** create/delete için iyimser güncelleme; hata halinde rollback + toast.
- **Cache:** React Query/SWR kullanılıyorsa key: `['conversations', userId]`; invalidate create/delete ardından.

## Uygulama Planı (ClaudeCode + Cursor)
1. **Backend**
   - Migration: conversations tablosu + messages.conversation_id (gerekliyse default tek conversation aktarımı).
   - Hono route’ları: `conversations.ts` ekle; auth middleware ile koru; validation (Zod) ekle.
   - Test: contract/integration testi ekle (liste, oluştur, sil; RLS ihlali testleri).
2. **Mobile/Web UI**
   - Ortak sorgu katmanı: `packages/chat` içinde `useConversationsQuery` / `useCreateConversation` / `useDeleteConversation`.
   - Mobil ekran: `(tabs)/chat.tsx`’te liste + boş/yükleniyor/hata; seçilen id’yi chat view ile paylaştır.
   - State: `activeConversationId` context/store; create/delete sonrası senkronize.
   - Boş durum: “Henüz sohbet yok. Yeni sohbet oluştur.” CTA.
3. **Güvenlik/Performans**
   - RLS açık, user_id filtresi.
   - limit/pagination destekle; default limit 50.
   - `last_message` için trigger veya view ile N+1’leri engelle.

## Kabul Kriterleri
- Kullanıcı kendi sohbetlerini listeleyebilir, yeni sohbet açabilir, mevcut sohbeti seçebilir, silebilir.
- Boş/yükleniyor/hata durumları görülebilir; hata mesajı ve yeniden dene vardır.
- Aktif sohbet seçimi mesaj akışını günceller; silinen aktif sohbet sonrası yeni sohbet başlatılır veya boş ekran gösterilir.
- RLS ile başka kullanıcının verisi görülemez; istekler auth zorunlu.
