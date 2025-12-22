# T-064: Basic Offline Support

**Priority:** P1 (Important)
**Effort:** 2-3 days
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 9

---

## Description

Implement basic offline support so users can view their data and queue actions when offline.

## Tasks

### Phase 1: Detection & UI
- [ ] Add network status hook (`useNetworkStatus`)
- [ ] Show offline indicator in UI
- [ ] Disable actions that require network

### Phase 2: Data Caching
- [ ] Cache notes, tasks, events in AsyncStorage
- [ ] Implement cache invalidation
- [ ] Show cached data when offline

### Phase 3: Mutation Queue
- [ ] Queue create/update/delete operations when offline
- [ ] Sync queue when back online
- [ ] Handle conflicts (last-write-wins or prompt user)

## Implementation

```typescript
// apps/mobile/src/hooks/useNetworkStatus.ts
import NetInfo from '@react-native-community/netinfo';

export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);
  
  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected ?? true);
    });
    return unsubscribe;
  }, []);
  
  return { isOnline };
}
```

## Acceptance Criteria

- User knows when offline
- Cached data viewable offline
- Queued actions sync when online
- No data loss

