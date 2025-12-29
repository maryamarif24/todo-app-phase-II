# Research: Phase II Full-Stack Web Todo Application

**Feature**: Phase II Full-Stack Web Todo Application
**Date**: 2024-12-27
**Branch**: `002-phase-ii-web-todo`

## Research Questions

### Q1: FastAPI + Better Auth Integration Pattern

**Question**: How does Better Auth integrate with FastAPI backend?

**Findings**:
- Better Auth is primarily designed for client-side use but provides server-side utilities
- For FastAPI integration, Better Auth can be used in "headless" mode
- The server handles session validation and user data through Better Auth's server utilities
- Session cookies are validated on each protected request
- User data is retrieved from the database using the session

**Decision**: Use Better Auth server utilities for session validation in FastAPI middleware. The frontend uses Better Auth client, backend validates sessions.

### Q2: Neon PostgreSQL + SQLModel Async Connection

**Question**: How to configure SQLModel with Neon PostgreSQL for async operations?

**Findings**:
- Neon provides a PostgreSQL connection string for SQLModel
- Use `sqlmodel.create_engine()` with asyncpg driver for async support
- Set `connect_args={"ssl": "require"}` for Neon connections
- Environment variable `DATABASE_URL` contains the full connection string
- SQLModel 0.0.14+ supports async sessions with `AsyncSession`

**Decision**: Use SQLModel with asyncpg driver for Neon connections. Configure via environment variables.

### Q3: Next.js App Router + Better Auth Client

**Question**: How to integrate Better Auth client with Next.js App Router?

**Findings**:
- Better Auth provides a React client library
- Use `createAuthClient` from `@better-auth/react` for Next.js
- Wrap application with `AuthProvider` component
- Client-side auth state accessible through `useAuth` hook
- Server Components can use `auth()` helper for server-side auth
- App Router route groups organize auth vs. protected pages

**Decision**: Use Better Auth React client with Next.js App Router. Route groups separate auth pages from protected todo pages.

### Q4: Responsive UI Strategy for Todo Application

**Question**: What CSS approach provides responsive design for both desktop and mobile?

**Findings**:
- Tailwind CSS is the de facto standard for Next.js projects
- Provides utility-first classes for responsive design
- Mobile-first breakpoints built-in (`sm`, `md`, `lg`, `xl`, `2xl`)
- No additional CSS files needed; co-located with components
- Dark mode support available out of the box

**Decision**: Use Tailwind CSS for responsive UI. Apply mobile-first breakpoints.

## Technology Decisions

### Backend Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Web Framework | FastAPI | Constitution-approved; high performance; native async |
| ORM | SQLModel | Constitution-approved; type-safe; Pydantic integration |
| Database | Neon PostgreSQL | Constitution-approved; serverless; cost-effective |
| Auth | Better Auth | Constitution-approved; TypeScript support; session management |

### Frontend Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | Next.js 14+ | Constitution-approved; App Router; server components |
| Language | TypeScript 5.x | Constitution-required; type safety |
| Styling | Tailwind CSS | Industry standard; responsive design; low bundle size |
| Auth Client | Better Auth React | Matches backend auth; seamless integration |

### Integration Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │  Auth Pages │    │  Todo Pages │    │  API Client     │  │
│  │ (signup,    │    │ (list,      │    │  (fetch with    │  │
│  │  signin)    │    │   edit)     │    │   cookies)      │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP + Cookies
┌─────────────────────────▼───────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Better Auth │    │  API Routes │    │  SQLModel       │  │
│  │ (session    │    │  (CRUD)     │    │  (PostgreSQL)   │  │
│  │  validation)│    │             │    │                 │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │  Neon PostgreSQL    │
                └─────────────────────┘
```

## Best Practices Identified

### Backend

1. **Dependency Injection**: Use FastAPI's `Depends()` for auth dependency
2. **Error Handling**: Create custom HTTPException handlers for consistent errors
3. **Validation**: Use Pydantic models for all request/response validation
4. **Ownership Checks**: Always verify todo.user_id matches current user
5. **Async Operations**: Use async/await throughout for scalability

### Frontend

1. **Route Protection**: Create HOC or middleware to protect todo pages
2. **Loading States**: Show loading UI during auth state resolution
3. **Error Boundaries**: Wrap pages in error boundaries for graceful failures
4. **Form Handling**: Use controlled components with validation feedback
5. **Optimistic Updates**: Update UI immediately, revert on API failure

### Database

1. **Indexes**: Index user_id on todos for fast filtered queries
2. **Cascading**: No cascade delete; explicit ownership checks instead
3. **Migrations**: Use Alembic for schema migrations (separate from code)
4. **Connection Pooling**: Configure appropriate pool size for Neon

## Security Considerations

1. **Password Hashing**: bcrypt with appropriate work factor
2. **Session Security**: HttpOnly, Secure, SameSite cookie flags
3. **SQL Injection**: Prevented by SQLModel's parameterized queries
4. **XSS Prevention**: React escapes by default; be careful with dangerouslySetInnerHTML
5. **CSRF Protection**: Built into Better Auth session handling
6. **Rate Limiting**: Apply to auth endpoints (5 attempts per minute)

## References

- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLModel Documentation: https://sqlmodel.tiangolo.com
- Better Auth Documentation: https://better-auth.com/docs
- Next.js Documentation: https://nextjs.org/docs
- Neon PostgreSQL Documentation: https://neon.tech/docs
- Tailwind CSS Documentation: https://tailwindcss.com/docs
