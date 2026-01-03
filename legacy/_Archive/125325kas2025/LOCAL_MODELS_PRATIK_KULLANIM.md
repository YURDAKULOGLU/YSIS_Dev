# Local Modelleri Pratikte Kullanma Rehberi

**Oluşturulma:** 2025-11-26T20:16:00+03:00
**Hedef Sistem:** RTX 5090 + Ryzen 9 9950X3D + 64GB RAM
**Durum:** 🟢 Sistemde 5 model hazır

---

## 🎯 3 Pratik Kullanım Yöntemi

### Yöntem 1: Terminal'den Direkt Kullanım (En Basit)

**Senaryo:** Hızlı kod üretimi, soru-cevap

```bash
# Model başlat ve soru sor
ollama run deepseek-r1:32b "Write a TypeScript interface for a User with id, name, email, and created_at fields"

# Başka bir model
ollama run qwen2.5:14b "Explain how React useEffect works"

# Kısa soru için hızlı model
ollama run llama3 "What is the difference between interface and type in TypeScript?"
```

**Avantajlar:**
- ✅ Anında cevap
- ✅ Kurulum gerektirmez
- ✅ API key yok
- ✅ Sınırsız kullanım

**Dezavantajlar:**
- ❌ Her seferinde model yüklenir (yavaş)
- ❌ Conversation history yok
- ❌ Dosyalarla etkileşim yok

---

### Yöntem 2: API Modu (Önerilen - En Esnek)

**Senaryo:** Script'lerden, VS Code extension'lardan, diğer tool'lardan kullanım

#### Adım 1: Ollama Server Başlat
```bash
# Terminal 1'de - Server'ı başlat (arka planda çalışır)
ollama serve
```

#### Adım 2: VS Code'da Kullan
```json
// .vscode/settings.json
{
  "continue.models": [
    {
      "title": "DeepSeek Coder",
      "provider": "ollama",
      "model": "deepseek-r1:32b",
      "apiBase": "http://localhost:11434"
    }
  ]
}
```

#### Adım 3: Python Script'ten Kullan
```python
# generate_tests.py
import requests
import json

def generate_unit_tests(code_file):
    with open(code_file, 'r') as f:
        code = f.read()

    prompt = f"Generate comprehensive Jest unit tests for this TypeScript code:\n\n{code}"

    response = requests.post('http://localhost:11434/api/generate',
        json={
            'model': 'deepseek-r1:32b',
            'prompt': prompt,
            'stream': False
        })

    return response.json()['response']

# Kullanım
tests = generate_unit_tests('src/hooks/useUserContext.tsx')
print(tests)
```

#### Adım 4: Node.js Script'ten Kullan
```javascript
// generate_docs.js
import ollama from 'ollama';

async function generateDocs(filePath) {
  const code = await fs.readFile(filePath, 'utf-8');

  const response = await ollama.generate({
    model: 'qwen2.5:14b',
    prompt: `Generate comprehensive JSDoc comments for this TypeScript code:\n\n${code}`,
  });

  return response.response;
}

// Kullanım
const docs = await generateDocs('src/services/ai/tools.ts');
console.log(docs);
```

**Avantajlar:**
- ✅ Server bir kez başlar, hep hazır
- ✅ OpenAI API ile uyumlu
- ✅ Scriptlerden kolay erişim
- ✅ Conversation history tutulabilir
- ✅ Streaming support

**Dezavantajlar:**
- ❌ Server'ın açık kalması gerekir

---

### Yöntem 3: Workflow Automation (En Güçlü)

**Senaryo:** Multi-agent sistemde otomatik görev dağıtımı

#### Örnek Workflow: Test Generation

```bash
# workflow-test-generation.sh

#!/bin/bash

echo "🧪 Automated Test Generation Workflow"
echo "======================================"

# 1. Değişen dosyaları bul
CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | grep ".tsx\|.ts")

for FILE in $CHANGED_FILES; do
    echo "📝 Generating tests for: $FILE"

    # 2. Dosya içeriğini oku
    CODE=$(cat $FILE)

    # 3. DeepSeek ile test üret
    TESTS=$(ollama run deepseek-r1:32b "Generate Jest unit tests for this TypeScript code. Only output the test code:\n\n$CODE")

    # 4. Test dosyası oluştur
    TEST_FILE="${FILE%.tsx}.test.tsx"
    echo "$TESTS" > "$TEST_FILE"

    echo "✅ Created: $TEST_FILE"
done

echo "🎉 Test generation complete!"
```

#### Örnek Workflow: Documentation Update

```bash
# workflow-update-docs.sh

#!/bin/bash

echo "📚 Automated Documentation Update"
echo "=================================="

# 1. Tüm servis dosyalarını bul
SERVICE_FILES=$(find src/services -name "*.ts" -not -name "*.test.ts")

for FILE in $SERVICE_FILES; do
    echo "📖 Updating docs for: $FILE"

    # 2. Qwen ile dokümantasyon üret
    DOCS=$(ollama run qwen2.5:14b "Add comprehensive JSDoc comments to this code. Return the full code with comments:\n\n$(cat $FILE)")

    # 3. Dosyayı güncelle
    echo "$DOCS" > "$FILE"

    echo "✅ Updated: $FILE"
done

echo "🎉 Documentation update complete!"
```

#### Örnek Workflow: Code Review

```bash
# workflow-code-review.sh

#!/bin/bash

echo "🔍 Automated Code Review"
echo "========================"

# 1. PR'daki değişiklikleri al
DIFF=$(git diff main...HEAD)

# 2. Gemini (veya başka model) ile review yap
REVIEW=$(ollama run mixtral:latest "Review this code diff. Check for:\n- YBIS Constitution violations\n- TypeScript best practices\n- Potential bugs\n- Performance issues\n\nDiff:\n$DIFF")

# 3. Review'u markdown'a kaydet
echo "# Automated Code Review - $(date)" > review.md
echo "" >> review.md
echo "$REVIEW" >> review.md

# 4. Slack/Discord'a gönder (opsiyonel)
# curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$REVIEW\"}" $SLACK_WEBHOOK

echo "✅ Review saved to review.md"
cat review.md
```

---

## 🚀 Hızlı Başlangıç: En Pratik Setup

### 1. Ollama Server'ı Arka Planda Başlat

```bash
# Windows'ta (PowerShell)
Start-Process -NoNewWindow ollama serve

# Linux/Mac'te
nohup ollama serve &
```

### 2. VS Code Extension Kur (Continue.dev)

```bash
# VS Code'da
# Extensions -> "Continue" ara -> Install
# Sonra settings.json'a ekle:
{
  "continue.models": [
    {
      "title": "DeepSeek 32B (Heavy)",
      "model": "deepseek-r1:32b",
      "provider": "ollama"
    },
    {
      "title": "Qwen 14B (Medium)",
      "model": "qwen2.5:14b",
      "provider": "ollama"
    },
    {
      "title": "Llama 8B (Fast)",
      "model": "llama3",
      "provider": "ollama"
    }
  ]
}
```

### 3. Package Scripts Ekle

```json
// package.json
{
  "scripts": {
    "ai:test": "node scripts/ai-generate-tests.js",
    "ai:docs": "node scripts/ai-update-docs.js",
    "ai:review": "bash scripts/ai-code-review.sh",
    "ai:refactor": "node scripts/ai-suggest-refactor.js"
  }
}
```

---

## 💡 Pratik Kullanım Senaryoları

### Senaryo 1: Unit Test Üretimi
```bash
# Manuel
ollama run deepseek-r1:32b < useUserContext.tsx > useUserContext.test.tsx

# Otomatik (git hook)
# .git/hooks/pre-commit
npm run ai:test
```

### Senaryo 2: API Dokümantasyonu
```bash
# Tüm API route'ları için swagger docs üret
find apps/backend/src/routes -name "*.ts" | while read file; do
    ollama run qwen2.5:14b "Generate OpenAPI/Swagger documentation for this Express route: $(cat $file)" > "${file%.ts}.swagger.yaml"
done
```

### Senaryo 3: Code Review Asistanı
```bash
# PR'daki her commit için review
git log main..HEAD --pretty=format:"%H" | while read commit; do
    DIFF=$(git show $commit)
    ollama run mixtral "Review this commit for YBIS standards:\n$DIFF" > "reviews/$commit.md"
done
```

### Senaryo 4: Refactoring Önerileri
```bash
# Karmaşık dosyalar için refactoring önerisi
find src -name "*.tsx" -exec wc -l {} \; | sort -rn | head -10 | while read lines file; do
    if [ $lines -gt 200 ]; then
        ollama run deepseek-r1:32b "Suggest refactoring for this large file (${lines} lines): $(cat $file)" > "refactor-suggestions/$(basename $file).md"
    fi
done
```

---

## ⚡ Performance Optimizasyonu

### Hot Loading (Önerilen)
```bash
# Model'i VRAM'e yükle ve orada tut
ollama run deepseek-r1:32b "" &
ollama run qwen2.5:14b "" &

# Şimdi her çağrı HIZLI (model zaten yüklü)
# 1. çağrı: 30 saniye (model loading)
# 2+ çağrılar: 2 saniye (sadece inference)
```

### Parallel Processing
```bash
# 3 task'ı paralel çalıştır
(ollama run deepseek-r1:32b "Generate tests for file1" > file1.test.tsx) &
(ollama run qwen2.5:14b "Generate docs for file2" > file2.docs.md) &
(ollama run llama3 "Explain file3" > file3.explanation.txt) &

wait
echo "All done!"
```

### Batch Processing
```bash
# Birçok dosyayı toplu işle
find src -name "*.tsx" | xargs -P 3 -I {} bash -c 'ollama run qwen2.5:14b "Add comments to: $(cat {})" > {}.commented'
```

---

## 🎯 Agentic Workflow Entegrasyonu

### Task Board'dan Otomatik Görev Alma

```javascript
// agent-worker-local.js
const fs = require('fs');
const ollama = require('ollama');

async function checkTaskBoard() {
    const taskBoard = fs.readFileSync('shared/TASK_BOARD.md', 'utf-8');

    // "P2: Generate unit tests" gibi bir task bul
    const match = taskBoard.match(/\[ \] \*\*P2: Generate unit tests for `(.+)`\*\*/);

    if (match) {
        const file = match[1];
        console.log(`📝 Found task: Generate tests for ${file}`);

        // DeepSeek ile test üret
        const code = fs.readFileSync(file, 'utf-8');
        const response = await ollama.generate({
            model: 'deepseek-r1:32b',
            prompt: `Generate Jest unit tests:\n\n${code}`
        });

        // Test dosyası oluştur
        const testFile = file.replace('.tsx', '.test.tsx');
        fs.writeFileSync(testFile, response.response);

        // Communication log'a yaz
        const log = `\n### [AGENT: DeepSeek-R1] [TIME: ${new Date().toISOString()}]
**Status:** ✅ COMPLETED
**Task:** Generate unit tests for ${file}
**Output:** ${testFile}
**Lines Generated:** ${response.response.split('\n').length}
**Duration:** ${response.total_duration / 1e9}s\n`;

        fs.appendFileSync('communication_log.md', log);

        console.log(`✅ Completed: ${testFile}`);
    }
}

// Her 5 dakikada bir kontrol et
setInterval(checkTaskBoard, 5 * 60 * 1000);
```

---

## 📊 Model Seçim Rehberi

### DeepSeek-R1 32B (19GB)
**Ne zaman kullan:**
- ✅ Complex coding tasks
- ✅ Multi-file refactoring planları
- ✅ Architecture decisions
- ✅ Test generation (comprehensive)
- ❌ Basit sorular için overkill

**Örnek:**
```bash
ollama run deepseek-r1:32b "Refactor this 500-line component into smaller, reusable pieces"
```

### Qwen2.5 14B (9GB)
**Ne zaman kullan:**
- ✅ Documentation generation
- ✅ Code explanation
- ✅ Medium complexity coding
- ✅ API design
- ❌ Quick questions için yavaş

**Örnek:**
```bash
ollama run qwen2.5:14b "Generate comprehensive JSDoc for this service class"
```

### Llama3 8B (4.7GB)
**Ne zaman kullan:**
- ✅ Quick questions
- ✅ Simple code generation
- ✅ Explanation requests
- ✅ Code formatting
- ❌ Complex reasoning için yetersiz

**Örnek:**
```bash
ollama run llama3 "What does this function do?"
```

### Mixtral (26GB)
**Ne zaman kullan:**
- ✅ Code review
- ✅ Heavy reasoning tasks
- ✅ Multi-language tasks
- ✅ Architecture analysis
- ❌ VRAM'de yer kaplar

**Örnek:**
```bash
ollama run mixtral "Review this PR for security vulnerabilities"
```

---

## 🔥 İlk 3 Pratik Adım (Bugün Yapılabilir)

### 1. Server'ı Başlat (2 dakika)
```bash
ollama serve
```

### 2. İlk Test'i Üret (5 dakika)
```bash
ollama run deepseek-r1:32b "Generate Jest unit tests for this hook: $(cat apps/mobile/src/hooks/useUserContext.tsx)" > test-output.txt
cat test-output.txt
```

### 3. Script Oluştur (10 dakika)
```bash
# scripts/ai-generate-tests.sh
#!/bin/bash
FILE=$1
ollama run deepseek-r1:32b "Generate Jest tests: $(cat $FILE)" > "${FILE%.tsx}.test.tsx"
echo "✅ Generated: ${FILE%.tsx}.test.tsx"
```

**Kullanım:**
```bash
bash scripts/ai-generate-tests.sh src/hooks/useUserContext.tsx
```

---

## 💰 Maliyet Karşılaştırması

| Yöntem | Maliyet | Hız | Sınırlama |
|--------|---------|-----|-----------|
| **OpenAI GPT-4** | $0.03/1K tokens | Hızlı | Rate limits |
| **Claude Sonnet** | $0.015/1K tokens | Hızlı | Rate limits |
| **Local (Ollama)** | **$0** | Orta | GPU/RAM |

**Örnek Hesap:**
- 1000 test case üretimi
- GPT-4: ~$30
- Ollama: **$0**
- **Kazanç: $30 × 12 ay = $360/yıl**

---

## 🎯 Sonraki Adımlar

1. **Bugün:** `ollama serve` başlat, bir test üret
2. **Bu Hafta:** 3 automation script yaz
3. **Gelecek Hafta:** Agentic workflow'a entegre et
4. **Ay Sonuna:** 30% task'ları local modeller yapsın

---

**Oluşturan:** @GitHub Copilot CLI
**Güncelleme:** 2025-11-26T20:16:00+03:00
**Durum:** 🟢 Ready to use
