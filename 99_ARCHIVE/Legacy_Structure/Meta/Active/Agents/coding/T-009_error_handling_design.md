# T-009: Backend Error Handling - Design Document

**Agent:** @ClaudeCode (Terminal Coder)
**Date:** 2025-11-30
**Status:** Design Complete

---

## Current State Analysis

### Problems Identified

1. **Inconsistent Error Response Format**
   - Some errors return `{ error: string }`
   - Some return `{ error: string, code: string }`
   - Validation errors return `{ error: string, details: array }`
   - Success responses sometimes include `{ success: boolean }`

2. **Improper HTTP Status Codes**
   - DatabaseError always returns 500 (should be context-dependent)
   - LLMError always returns 500 (should be context-dependent)
   - No 409 (Conflict), 403 (Forbidden) used

3. **Code Duplication**
   - Every route repeats the same try-catch-if-DatabaseError-return pattern
   - Error logging inconsistent across routes

4. **Missing Error Context**
   - Errors don't include timestamp
   - Errors don't include request path
   - No correlation IDs for tracing

---

## Proposed Solution

### 1. Custom Error Classes

Create a hierarchy of custom error classes with proper HTTP status codes:

```typescript
// Base class
class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number,
    public code?: string,
    public details?: unknown
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

// Specific error types
class ValidationError extends AppError {
  constructor(message: string, details?: unknown) {
    super(message, 400, 'VALIDATION_ERROR', details);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(message, 403, 'FORBIDDEN');
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND');
  }
}

class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 409, 'CONFLICT');
  }
}

class InternalError extends AppError {
  constructor(message = 'Internal server error', details?: unknown) {
    super(message, 500, 'INTERNAL_ERROR', details);
  }
}
```

### 2. Standard Error Response Format

All errors will return this structure:

```typescript
{
  error: {
    message: string;       // Human-readable error message
    code: string;          // Machine-readable error code
    details?: unknown;     // Optional additional context
    timestamp: string;     // ISO timestamp
    path: string;          // Request path
  }
}
```

### 3. Global Error Middleware

Replace the simple `app.onError` handler with a comprehensive middleware:

```typescript
app.onError((err, c) => {
  const timestamp = new Date().toISOString();
  const path = c.req.path;

  // Handle AppError instances
  if (err instanceof AppError) {
    Logger.warn(`Request error: ${err.message}`, {
      type: 'HTTP',
      path,
      method: c.req.method,
      status: err.statusCode,
      code: err.code,
    });

    return c.json(
      {
        error: {
          message: err.message,
          code: err.code,
          details: err.details,
          timestamp,
          path,
        },
      },
      err.statusCode
    );
  }

  // Handle DatabaseError
  if (err instanceof DatabaseError) {
    const statusCode = mapDatabaseErrorToStatus(err);

    Logger.error('Database error', err, {
      type: 'DATABASE',
      path,
      method: c.req.method,
      code: err.code,
    });

    return c.json(
      {
        error: {
          message: err.message,
          code: err.code || 'DATABASE_ERROR',
          timestamp,
          path,
        },
      },
      statusCode
    );
  }

  // Handle LLMError
  if (err instanceof LLMError) {
    Logger.error('LLM error', err, {
      type: 'LLM',
      path,
      method: c.req.method,
      code: err.code,
    });

    return c.json(
      {
        error: {
          message: err.message,
          code: err.code || 'LLM_ERROR',
          timestamp,
          path,
        },
      },
      500
    );
  }

  // Handle unknown errors
  Logger.error('Unhandled error', err, {
    type: 'HTTP',
    path,
    method: c.req.method,
  });

  return c.json(
    {
      error: {
        message: process.env.NODE_ENV === 'production'
          ? 'Internal server error'
          : err.message,
        code: 'INTERNAL_ERROR',
        timestamp,
        path,
      },
    },
    500
  );
});
```

### 4. Route Simplification

Routes can now throw custom errors instead of returning responses:

**Before:**
```typescript
if (!validationResult.success) {
  return c.json(
    { error: 'Validation failed', details: validationResult.error.issues },
    400
  );
}
```

**After:**
```typescript
if (!validationResult.success) {
  throw new ValidationError('Validation failed', validationResult.error.issues);
}
```

**Before:**
```typescript
if (!task || task.user_id !== user.id) {
  return c.json({ error: 'Task not found' }, 404);
}
```

**After:**
```typescript
if (!task || task.user_id !== user.id) {
  throw new NotFoundError('Task');
}
```

---

## Implementation Plan

### Phase 1: Create Error Infrastructure
1. Create `src/middleware/errors.ts` with custom error classes
2. Create helper function `mapDatabaseErrorToStatus()`
3. Update global error handler in `src/index.ts`

### Phase 2: Update Routes
1. Update `src/routes/tasks.ts` to use custom errors
2. Update `src/routes/notes.ts` to use custom errors
3. Update `src/routes/chat.ts` to use custom errors
4. Update `src/routes/llm.ts` to use custom errors
5. Update `src/middleware/auth.ts` to use custom errors

### Phase 3: Testing
1. Run existing tests to ensure compatibility
2. Add new tests for error scenarios
3. Manual testing of error responses

---

## Benefits

1. **Consistency**: All errors follow the same format
2. **DRY**: No repeated error handling code in routes
3. **Type Safety**: TypeScript ensures proper error usage
4. **Debuggability**: Timestamps and paths aid debugging
5. **Maintainability**: Centralized error logic
6. **Production Ready**: Different behavior for dev/prod modes
