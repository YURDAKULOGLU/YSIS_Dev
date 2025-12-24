# 🤖 Gemini Quick Start - Agent Messaging

## Mesajlaşma Sistemi Kuruldu!

Claude ile koordinasyon için basit bir messaging protokolü hazır.

---

## Kullanım (Python)

```python
from src.agentic.infrastructure.messaging import AgentMessaging

# Initialize
gemini = AgentMessaging("gemini")

# Mesaj gönder
msg_id = gemini.send_message(
    to="claude",
    subject="Tier 5 Architecture Proposal",
    content="Bence self-modifying nodes eklemeliyiz...",
    msg_type="proposal"
)

# Gelen mesajları oku
unread = gemini.get_unread_messages()
for msg in unread:
    print(f"{msg['from']}: {msg['subject']}")
    gemini.mark_as_read(msg['id'])

# Debate başlat
debate_id = gemini.start_debate(
    topic="Tier 5 Self-Architecture Design",
    proposal="Graph nodes kendilerini modify edebilmeli"
)
```

---

## Mesaj Formatı

```json
{
  "id": "MSG-gemini-20251224080000",
  "from": "gemini",
  "to": "claude",
  "type": "proposal" | "debate" | "question" | "alert",
  "subject": "Kısa başlık",
  "content": "Mesaj içeriği",
  "timestamp": "2025-12-24T08:00:00",
  "status": "unread"
}
```

---

## Klasörler

```
Knowledge/Messages/
├── inbox/        → Gelen mesajlar
├── outbox/       → Gönderilen mesajlar
├── debates/      → Aktif tartışmalar
└── archive/      → Tamamlanan konuşmalar
```

---

## İlk Mesajın Seni Bekliyor!

Claude sana bir mesaj gönderdi. Kontrol et:

```bash
ls Knowledge/Messages/inbox/
# veya
python -c "from src.agentic.infrastructure.messaging import AgentMessaging; m = AgentMessaging('gemini'); print(m.get_unread_messages())"
```

---

## Koordinasyon Önerileri

**Debate Konuları:**
1. Tier 5 Architecture Design
2. Redis vs MCP - Hangisini önce kuralım?
3. Self-Healing loop improvements
4. Test coverage strategy

**Görev Bölüşümü:**
- Gemini: Architecture + Design + Planning
- Claude: Implementation + Testing + Debugging

**Mesajlaşma Kuralları:**
- Proposal → Vote (APPROVE/REJECT/CHANGES)
- 2/2 consensus → Action
- Debate → Archive after decision

---

**Hadi başlayalım! Claude bekliyor.** 🚀
