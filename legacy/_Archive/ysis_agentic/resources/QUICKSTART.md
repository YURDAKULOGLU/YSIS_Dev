# YBIS Quick Start Guide

**Goal:** Get you coding in 5 minutes
**Audience:** Developers ready to implement
**Last Updated:** 2025-11-04
**Note:** Widget-based navigation implemented (AD-019)

---

## ⚡ 5-Minute Setup

### 1. Prerequisites Check
```bash
node --version  # Should be 20.11.0 LTS
npm --version   # Should be 9.0.0+
```

### 2. Clone & Install
```bash
cd C:\Projeler\YBIS
npm install     # Already done! (1546 packages installed)
```

### 3. Environment Setup
```bash
# Copy example env
cp .env.example .env

# Add your keys (get from team)
SUPABASE_URL=your_url
SUPABASE_ANON_KEY=your_key
OPENAI_API_KEY=your_key
```

### 4. Verify Setup
```bash
# Test TypeScript compilation
npm run type-check

# Test linting
npm run lint

# Test backend
cd apps/backend
npm run dev  # Should start on http://localhost:3000
```

---

## 🏗️ Project Structure (Monorepo)

```
YBIS/
├── apps/
│   ├── mobile/           ← Expo SDK 54 app (YOUR FOCUS)
│   └── backend/          ← Hono API (Vercel)
├── packages/
│   ├── @ybis/core        ← Shared types, schemas, utils
│   ├── @ybis/ui          ← Tamagui components
│   ├── @ybis/chat        ← Chat UI (react-native-gifted-chat)
│   ├── @ybis/auth        ← Expo Auth Session wrapper
│   ├── @ybis/database    ← Supabase client
│   ├── @ybis/llm         ← OpenAI + Anthropic clients
│   ├── @ybis/theme       ← Tamagui theme config
│   ├── @ybis/i18n        ← Translations (TR/EN)
│   └── @ybis/utils       ← Shared utility functions
└── docs/                 ← You are here!
```

---

## 🎯 Your First Task

### Option A: Mobile App Screens (Recommended Start)

**What:** Create basic Expo Router screens
**Why:** Foundation for all features
**Effort:** 2-3 hours

**Files to create:**
```
apps/mobile/app/
├── _layout.tsx           ← Root layout (auth check)
├── (auth)/
│   ├── _layout.tsx       ← Auth layout
│   └── login.tsx         ← Login screen
├── (main)/               ← Main app layout group
│   ├── _layout.tsx       ← Main layout with header
│   ├── index.tsx         ← The widget-based dashboard screen
│   ├── tasks.tsx         ← Dedicated tasks screen
│   ├── notes.tsx         ← Dedicated notes screen
│   └── settings.tsx      ← Settings screen
└── +not-found.tsx        ← 404 screen
```

**Key APIs to use:**
- `expo-router` - File-based navigation
- `@ybis/ui` - Tamagui components (buttons, inputs)
- `@ybis/theme` - Theme configuration
- `@ybis/auth` - Auth context (to be implemented)

**Commands:**
```bash
cd apps/mobile
npm run start  # Start Expo dev server
```

**Reference:**
- Expo Router docs: https://docs.expo.dev/router/introduction/
- Tamagui components: https://tamagui.dev/ui/intro

---

### Option B: Auth Implementation

**What:** Google OAuth with Expo Auth Session
**Why:** Users need to login
**Effort:** 3-4 hours

**Files to create/modify:**
```
packages/auth/src/
├── AuthProvider.tsx      ← React context provider
├── useAuth.ts           ← Auth hook
├── ExpoAuthAdapter.ts   ← Port implementation
└── types.ts             ← Auth types

packages/core/src/ports/
└── AuthPort.ts          ← Port interface
```

**Key APIs:**
- `expo-auth-session` - OAuth flow
- `expo-web-browser` - In-app browser
- `expo-crypto` - PKCE challenge
- `expo-secure-store` - Token storage

**Implementation steps:**
1. Create AuthPort interface in `@ybis/core`
2. Implement ExpoAuthAdapter in `@ybis/auth`
3. Create AuthProvider context
4. Test Google OAuth flow

**Reference:**
- Expo Auth docs: https://docs.expo.dev/versions/latest/sdk/auth-session/
- Google OAuth setup: https://console.cloud.google.com/

---

### Option C: Backend Health Check

**What:** Simple health check endpoint
**Why:** Verify backend works
**Effort:** 30 minutes

**Files to create:**
```
apps/backend/src/
├── index.ts             ← Main Hono app
└── routes/
    └── health.ts        ← Health check route
```

**Implementation:**
```typescript
// apps/backend/src/routes/health.ts
import { Hono } from 'hono';

const health = new Hono();

health.get('/', (c) => {
  return c.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '0.1.0',
    environment: process.env.NODE_ENV || 'development'
  });
});

export default health;
```

**Test:**
```bash
cd apps/backend
npm run dev
curl http://localhost:3000/health
```

---

## 🧭 Navigation Guide

### I want to...

**...understand the tech stack**
→ Read `YBIS_STANDARDS/tech-stack.md`

**...see what's been done**
→ Check `Güncel/DEVELOPMENT_LOG.md`

**...know the coding standards**
→ Review `YBIS_STANDARDS/2_Kalite_Ve_Standartlar/README.md`

**...understand architecture decisions**
→ Read `YBIS_STANDARDS/1_Anayasa/README.md` (Principles)
→ Read `YBIS_STANDARDS/README.md` (For overall architecture guidance)

**...see the task list**
→ Open `YBIS_STANDARDS/README.md` (Refer to the Control Center for task management)

**...use BMad commands**
→ Read `../.YBIS_Dev/AI_SYSTEM_GUIDE.md`

---

## 📝 Development Workflow

### Daily Workflow (Recommended)

1. **Pull latest changes**
   ```bash
   git pull origin main
   npm install  # If package.json changed
   ```

2. **Check current tasks**
   ```bash
   # Refer to YBIS_STANDARDS/README.md for task management
   ```

3. **Create feature branch**
   ```bash
   git checkout -b feature/task-name
   ```

4. **Develop**
   ```bash
   # Use BMad commands if needed:
   # /implement - For guided development
   # /review-story - For code review
   ```

5. **Test locally**
   ```bash
   npm run type-check
   npm run lint
   npm run test  # When tests exist
   ```

6. **Update DEVELOPMENT_LOG**
   ```markdown
   # Add to Güncel/DEVELOPMENT_LOG.md
   ### Day X - [DATE]
   - Completed: Task description
   - Files changed: List of files
   - Issues: Any blockers
   ```

7. **Commit & push**
   ```bash
   git add .
   git commit -m "feat: implement X"
   git push origin feature/task-name
   ```

---

## 🚨 Common Issues

### Issue: TypeScript errors after install
**Solution:**
```bash
npm run type-check
# Check specific package
cd packages/[package-name]
npm run type-check
```

### Issue: Metro bundler cache
**Solution:**
```bash
cd apps/mobile
npx expo start -c  # Clear cache
```

### Issue: Port already in use
**Solution:**
```bash
# Backend (default 3000)
lsof -ti:3000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :3000   # Windows
```

### Issue: Expo Go not connecting
**Solution:**
```bash
cd apps/mobile
npx expo start --tunnel  # Use tunnel mode
```

---

## 📚 Key Reference Links

### Official Docs
- [Expo SDK 54](https://docs.expo.dev/)
- [React 19.1.0](https://react.dev/)
- [Tamagui](https://tamagui.dev/)
- [Hono](https://hono.dev/)
- [Supabase](https://supabase.com/docs)

### YBIS Docs
- [Tech Stack](./YBIS_STANDARDS/tech-stack.md) - Complete package list
- [Constitution](./YBIS_STANDARDS/1_Anayasa/README.md) - Core principles
- [Tasks](./YBIS_STANDARDS/README.md) - Refer to Control Center for task management
- [Dev Log](./Güncel/DEVELOPMENT_LOG.md) - Daily progress

### BMad System
- [AI System Guide](../.YBIS_Dev/AI_SYSTEM_GUIDE.md) - Full guide
- [User Guide](../.YBIS_Dev/user-guide.md) - Workflow guide
- [Commands](../.claude/commands/YBIS/) - Available commands

---

## 🎯 Success Criteria

**You're ready when:**
- ✅ `npm install` runs without errors
- ✅ `npm run type-check` passes
- ✅ `npm run lint` passes
- ✅ Backend health check returns 200 OK
- ✅ Expo dev server starts successfully

**Next steps:**
1. Pick a task from `YBIS_STANDARDS/README.md` (Refer to Control Center for task management)
2. Create feature branch
3. Implement using port architecture
4. Update `Güncel/DEVELOPMENT_LOG.md`
5. Commit & push

---

## 🤖 BMad Assisted Development (Optional)

YBIS supports **BMad Method** for structured AI-driven development.

### Quick BMad Usage

**1. Story Creation (Scrum Master)**
```bash
# In Claude Code or Cursor
@sm *draft

# SM will:
# - Read YBIS_STANDARDS/README.md for task management
# - Create detailed story with Tasks/Subtasks
# - Save to docs/stories/
# - Status: Draft → Approved (by you)
```

**2. Story Implementation (Developer)**
```bash
# New chat with Dev agent
@dev *develop-story docs/stories/1.1.mobile-screens.md

# Dev will:
# - Read story file ONLY (no PRD/Architecture needed!)
# - Implement all tasks
# - Update story checkboxes
# - Mark as "Review" when done
```

**3. Code Review (QA)**
```bash
# Optional: QA review
@qa *review-story docs/stories/1.1.mobile-screens.md

# QA will:
# - Review code quality
# - Check test coverage
# - Leave improvement checklist
# - Update story status
```

### BMad vs Manual Development

| Aspect | Manual (QUICKSTART) | BMad Assisted |
|--------|---------------------|---------------|
| **Speed** | Faster for simple tasks | Better for complex stories |
| **Structure** | Flexible | Highly structured |
| **Documentation** | Update Güncel/DEVELOPMENT_LOG.md | Story files auto-tracked |
| **Best For** | Quick fixes, prototypes | Feature development, team work |

**Recommendation:** Start manual, use BMad for complex features.

---

## 💡 Pro Tips

1. 🔴 **Read YBIS_STANDARDS/2_Kalite_Ve_Standartlar/README.md FIRST** - Prevents ALL common issues we already solved!
2. **Always use port interfaces** - Never directly import 3rd party libs in app code
3. **Use FULL Tamagui prop names** - No shorthands (flex not f, alignItems not ai)
4. **Build packages before type-check** - `npx tsc --build ./packages/*`
5. **Update Güncel/DEVELOPMENT_LOG.md daily** - Future you will thank you (or let BMad track via stories)
6. **Run type-check before committing** - Catch errors early
7. **Use BMad for complex features** - Story-driven development ensures nothing missed
8. **Check YBIS_STANDARDS/tech-stack.md for versions** - Don't update packages randomly
9. **NO workarounds EVER** - Fix root cause, document in Güncel/DEVELOPMENT_LOG.md

---

**Ready to code?** Pick Option A (Mobile Screens) and let's go! 🚀
**Want structure?** See [`../.YBIS_Dev/AI_SYSTEM_GUIDE.md`](../.YBIS_Dev/AI_SYSTEM_GUIDE.md) for full BMad guide.
