# YBIS Technology Stack

**Last Updated:** 2025-11-04
**Version:** 1.2
**Status:** Production Ready - Expo SDK 54

---

## 📱 **Mobile (React Native + Expo)**

### Core Framework
```json
{
  "expo": "~54.0.21",
  "react": "19.1.0",
  "react-native": "0.81.4"
}
```

### Navigation & Routing
```json
{
  "expo-router": "~6.0.0",
  "react-native-screens": "~4.16.0",
  "react-native-safe-area-context": "5.6.1"
}
```

### UI Library
```json
{
  "tamagui": "^1.135.0",
  "@tamagui/config": "^1.135.0",
  "react-native-reanimated": "~4.1.0",
  "react-native-gesture-handler": "~2.28.0"
}
```

### Authentication
```json
{
  "expo-auth-session": "~7.0.0",
  "expo-web-browser": "~15.0.0",
  "expo-crypto": "~15.0.0",
  "expo-secure-store": "~15.0.0"
}
```

### Chat Interface
```json
{
  "react-native-gifted-chat": "^2.8.1"
}
```

### State Management
```json
{
  "zustand": "^5.0.8"
}
```

### Expo Modules
```json
{
  "expo-constants": "~18.0.0",
  "expo-device": "~8.0.0",
  "expo-file-system": "~19.0.0",
  "expo-font": "~14.0.0",
  "expo-haptics": "~15.0.0",
  "expo-notifications": "~0.32.0",
  "expo-status-bar": "~3.0.0"
}
```

---

## 🔧 **Backend (Serverless)**

### API Framework
```json
{
  "hono": "^4.6.14",
  "@hono/node-server": "^1.13.7"
}
```

### Runtime & Deployment
- **Node.js:** 20.11.0 LTS
- **Deployment:** DeploymentPort (AD-016) 🆕

**Current (Phase 0):**
- ✅ **VercelEdgeAdapter** - Serverless edge functions
- Free tier: 100K requests/month
- Auto-scaling, global CDN

**Planned (Phase 1):**
- 🔄 **CloudflareWorkerAdapter** - 10x cheaper ($5/10M vs $20/1M)
- Zero code change (same Hono)
- Faster cold start

**Future (Phase 2+):**
- 🔧 **NodeServerAdapter** - Traditional server if needed (long-running jobs)

---

## 🤖 **AI & LLM**

### AI SDKs
```json
{
  "openai": "^6.1.0",
  "@anthropic-ai/sdk": "^0.65.0"
}
```

### Strategy
- **Primary:** OpenAI GPT-4o-mini (cost-effective)
- **Fallback:** Anthropic Claude 3.5 Haiku
- **Future:** Multi-provider routing, local LLM support

---

## 💾 **Database & Storage**

### Database
```json
{
  "@supabase/supabase-js": "^2.58.0"
}
```

### Strategy
- **Primary:** Supabase PostgreSQL
- **Local:** AsyncStorage (offline-first)
- **Sync:** Real-time subscriptions

---

## 🌐 **Internationalization**

```json
{
  "i18next": "^25.5.3",
  "react-i18next": "^16.0.0"
}
```

### Supported Languages
- Turkish (TR)
- English (EN)
- Future: Spanish, French, German

---

## 🛠️ **Development Tools**

### TypeScript
```json
{
  "typescript": "^5.9.3"
}
```

### Linting & Formatting
```json
{
  "@typescript-eslint/eslint-plugin": "^8.45.0",
  "@typescript-eslint/parser": "^8.45.0",
  "eslint": "^9.37.0",
  "eslint-config-prettier": "^10.1.8",
  "eslint-plugin-react": "^7.33.2",
  "eslint-plugin-react-hooks": "^6.1.1",
  "prettier": "^3.2.4"
}
```

### Testing
```json
{
  "jest": "^30.2.0"
}
```

### Validation
```json
{
  "zod": "^4.1.11"
}
```

### Utilities
```json
{
  "date-fns": "^4.1.0"
}
```

### Git Hooks
```json
{
  "husky": "^9.1.7"
}
```

---

## 🏗️ **Architecture**

### Monorepo Structure
```
YBIS/
├── apps/
│   ├── mobile/          # Expo SDK 54 + React Native
│   ├── backend/         # Hono API (Vercel)
│   └── web/             # Future: Web dashboard
├── packages/
│   ├── @ybis/core       # Shared types, ports, and core interfaces
│   ├── @ybis/utils      # Shared utility functions (formatters, validators, etc.)
│   ├── @ybis/chat       # Chat UI components
│   ├── @ybis/ui         # Tamagui components (Design System)
│   ├── @ybis/auth       # Authentication client (implements AuthPort)
│   ├── @ybis/theme      # Theme configuration
│   ├── @ybis/i18n       # Translations
│   ├── @ybis/database   # Database client (implements DatabasePort)
│   ├── @ybis/llm        # AI/LLM client (implements LLMPort)
│   ├── @ybis/logging    # Centralized logging
│   ├── @ybis/storage    # Storage client (implements StoragePort)
│   └── @ybis/eslint-config # Shared ESLint rules
└── docs/                # Documentation
```

### API Client Mimarisi Notu
Proje, tek bir monolitik `@ybis/api-client` yerine, her bir harici servis için domaine özgü (domain-specific) istemci paketleri kullanır. Örneğin, `@ybis/database` veritabanı için, `@ybis/llm` ise yapay zeka modelleri için birer istemci görevi görür. Bu yaklaşım, her servisin kendi mantığını ve bağımlılıklarını izole ederek "Port Mimarisi" prensibini güçlendirir.

### Build System
- **Package Manager:** pnpm workspaces
- **Mobile Bundler:** Metro (Expo optimized)
- **Build Platform:** EAS Build (Expo Application Services)

### PNPM Monorepo Configuration

**File:** `.npmrc`

```ini
node-linker=hoisted
public-hoist-pattern[]=*expo*
public-hoist-pattern[]=*react-native*
```

**Rationale:**
- **`node-linker=hoisted`**: Places all packages in root `node_modules/` for flat structure
- **`public-hoist-pattern`**: Creates symlinks in each workspace package's `node_modules/` for matching patterns
- Expo SDK 54 and React Native native tooling (Android Gradle, iOS CocoaPods) require flat node_modules structure
- Expo CLI binary scripts need local access to dependencies (e.g., `apps/mobile/node_modules/.bin/expo` → `../expo/bin/cli`)
- Ensures all workspace packages can access Expo/React Native modules locally

**Reference:** [Expo Monorepo Guide](https://docs.expo.dev/guides/monorepos/#isolated-installations)

---

## 🚀 **Deployment**

### Mobile
- **Platform:** Expo Application Services (EAS)
- **iOS:** App Store
- **Android:** Google Play Store
- **OTA Updates:** Expo Updates

### Backend
- **Hosting:** Vercel Edge Functions
- **Region:** Auto (global edge network)
- **CI/CD:** GitHub Actions (planned)

---

## 📊 **Key Technical Decisions**

### ✅ Why Expo SDK 54?
- **Managed Workflow:** Less native code complexity
- **Fast Development:** Hot reload, Expo Go
- **OTA Updates:** Instant updates without app store
- **React 19.1.0 Support:** Latest React features
- **XCFramework:** Faster iOS builds

### ✅ Why React 19.1.0?
- **Latest Features:** React Compiler, Actions API
- **Performance:** Zero-bundle size abstractions
- **Stability:** Stable release (not RC)

### ✅ Why Hono?
- **Edge-Optimized:** Fast on Vercel Edge
- **Lightweight:** Minimal overhead
- **Modern:** TypeScript-first

### ✅ Why Supabase?
- **Real-time:** Built-in subscriptions
- **PostgreSQL:** Familiar, powerful
- **Cost-Effective:** Good free tier
- **Auth Ready:** OAuth integrations

### ✅ Why Tamagui?
- **Performance:** Optimized for React Native
- **Cross-Platform:** Web + Mobile
- **Modern:** React 19 compatible
- **Type-Safe:** Full TypeScript support

### ✅ Why Zustand?
- **Simple:** Minimal boilerplate
- **Fast:** Better performance than Redux
- **Small:** Tiny bundle size
- **React 19:** Full compatibility

---

## 🔄 **Migration Path (Completed)**

### From → To
- ❌ React Native CLI → ✅ Expo Managed
- ❌ Firebase Auth → ✅ Expo Auth Session
- ❌ React 19.2.0 → ✅ React 19.1.0
- ❌ React Native 0.81.0 → ✅ React Native 0.81.4
- ❌ Outdated packages → ✅ Latest stable versions

---

## 📈 **Performance Targets**

### Mobile App
- **Cold Start:** < 3 seconds
- **Hot Reload:** < 2 seconds
- **Memory Usage:** < 150MB idle
- **Bundle Size:** < 50MB
- **Frame Rate:** 60 FPS

### API
- **Response Time:** < 500ms (p95)
- **AI Response:** < 5 seconds
- **Uptime:** > 99.9%

---

## 🔒 **Security**

### Mobile
- **Data:** Encrypted storage (expo-secure-store)
- **Auth:** OAuth 2.0 (expo-auth-session)
- **Network:** TLS 1.3

### Backend
- **Runtime:** Serverless (stateless)
- **Secrets:** Environment variables
- **Rate Limiting:** Planned

---

## 🧪 **Quality Assurance**

### Testing Strategy
- **Unit Tests:** Jest (packages)
- **Integration Tests:** Planned
- **E2E Tests:** Planned (Detox)

### Code Quality
- **TypeScript:** Strict mode enabled
- **Linting:** ESLint + Prettier
- **Pre-commit:** Husky hooks
- **Type Checking:** All packages

---

## 📦 **Package Versions Summary**

### Critical Dependencies (as of 2025-11-04)
```
expo: ~54.0.21
react: 19.1.0
react-native: 0.81.4
expo-router: 6.0.x
tamagui: 1.135.0
openai: 6.1.0
@supabase/supabase-js: 2.58.0
typescript: ^5.9.3
```

### Update Policy
- **Security Updates:** Immediate
- **Minor Updates:** Weekly review
- **Major Updates:** Quarterly review + testing
- **Expo SDK:** Follow official release cycle

---

## 🔮 **Future Roadmap**

### Phase 1 (Current)
- ✅ Expo SDK 54 migration
- ✅ React 19.1.0 upgrade
- ✅ Package modernization

### Phase 2 (Next 3 months)
- [ ] EAS Build configuration
- [ ] First test build (iOS + Android)
- [ ] Beta deployment
- [ ] Performance optimization

### Phase 3 (Next 6 months)
- [ ] Web dashboard (Expo web)
- [ ] CI/CD pipeline
- [ ] E2E testing
- [ ] Production release

### Phase 4 (Future)
- [ ] Local LLM support
- [ ] Offline-first sync
- [ ] Advanced workflows
- [ ] Team features

---

**Technology Stack Status:** ✅ **Production Ready**
**Next Steps:** EAS Build setup → Test build → Beta testing
