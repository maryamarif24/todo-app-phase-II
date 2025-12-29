# Implementation Plan: Phase II Full-Stack Web Todo Application

**Branch**: `002-phase-ii-web-todo` | **Date**: 2024-12-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-phase-ii-web-todo/spec.md`

## Summary

Phase II transforms the Phase I in-memory CLI todo application into a full-stack web application. The architecture consists of a Python FastAPI backend with SQLModel ORM connecting to Neon PostgreSQL, a Next.js TypeScript frontend, and Better Auth for authentication. All todo data is strictly associated with authenticated users, ensuring data isolation and privacy. The implementation follows the constitution's Phase II technology stack: FastAPI, SQLModel, Neon DB, Next.js, and Better Auth.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, Next.js 14+, Better Auth
**Storage**: Neon Serverless PostgreSQL (cloud-hosted)
**Testing**: pytest (backend), Jest/Testing Library (frontend)
**Target Platform**: Web browsers (desktop and mobile)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: 95% of API operations < 3s, page load < 2s
**Constraints**: No AI, no agents, no background workers, no real-time features
**Scale/Scope**: Single-tenant web application, hundreds of users expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Verification

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | All work derived from approved spec.md |
| II. Agent Behavior Rules | ✅ PASS | No feature invention; follows spec exactly |
| III. Phase Governance | ✅ PASS | Only Phase II technologies used; no Phase III+ features |
| IV. Quality Principles | ✅ PASS | Clean architecture with separation of concerns |

### Technology Constraints Verification

| Technology | Required | Status |
|------------|----------|--------|
| Python (backend) | Yes | ✅ Using Python 3.11+ |
| FastAPI | Yes | ✅ REST API framework |
| SQLModel | Yes | ✅ ORM and data modeling |
| Neon DB (PostgreSQL) | Yes | ✅ Persistent storage |
| Next.js | Yes | ✅ Frontend framework |
| TypeScript | Yes | ✅ Type-safe frontend |
| Better Auth | Yes | ✅ Authentication framework |

### Prohibited Technologies Check

| Prohibited Technology | Status |
|-----------------------|--------|
| MongoDB, Redis | ✅ Not used |
| Flask, Django, Express.js | ✅ Not used |
| React/Vue/Angular standalone | ✅ Not used (Next.js only) |
| OpenAI Agents SDK, MCP | ✅ Not used (Phase IV+) |
| WebSockets, real-time | ✅ Not used |
| Background job processors | ✅ Not used |

**Result**: CONSTITUTION CHECK PASSED - All requirements satisfied

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-ii-web-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-contracts.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todo-app-cli/
├── backend/
│   ├── src/
│   │   ├── models/          # SQLModel entities (User, Todo, Session)
│   │   ├── services/        # Business logic layer
│   │   ├── api/             # FastAPI routers/controllers
│   │   ├── auth/            # Better Auth integration
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   │   ├── (auth)/      # Auth pages group
│   │   │   │   ├── signup/
│   │   │   │   └── signin/
│   │   │   ├── todos/       # Todo pages group
│   │   │   │   ├── page.tsx
│   │   │   │   ├── new/
│   │   │   │   └── [id]/
│   │   │   └── layout.tsx
│   │   ├── components/      # React components
│   │   │   ├── ui/          # Base UI components
│   │   │   ├── auth/        # Auth-related components
│   │   │   └── todos/       # Todo-related components
│   │   ├── lib/             # Utilities and API client
│   │   └── types/           # TypeScript type definitions
│   ├── tests/
│   └── package.json
├── tests/
│   ├── contract/            # API contract tests
│   └── e2e/                 # End-to-end tests
└── CLAUDE.md
```

**Structure Decision**: Web application with separate backend and frontend directories. Backend uses clean architecture with models, services, and API layers. Frontend uses Next.js App Router with route groups for auth and todo pages. All paths follow the constitution-approved technology stack.

## Phase 0: Research Findings

### Backend Framework (FastAPI)

**Decision**: Use FastAPI for the REST API backend.

**Rationale**:
- FastAPI is the constitution-approved web framework for Phase II
- Native support for Pydantic validation and async operations
- Automatic OpenAPI documentation generation
- High performance comparable to Node.js
- Excellent integration with SQLModel for database operations

**Alternatives Considered**:
- Flask: Not approved by constitution; lacks modern async support
- Django: Over-engineered for simple todo CRUD; not approved

### Authentication Framework (Better Auth)

**Decision**: Use Better Auth for authentication integration.

**Rationale**:
- Better Auth is the constitution-approved authentication framework for Phase II
- Provides signup, sign-in, session management out of the box
- Type-safe with TypeScript support
- Extensible plugin architecture
- Works well with FastAPI as the backend

**Implementation Notes**:
- Better Auth will handle user registration and sign-in flows
- Session cookies will be used for authentication state
- Backend will validate sessions on protected API routes
- Frontend will consume auth state through Better Auth client

### Database (Neon PostgreSQL + SQLModel)

**Decision**: Use Neon Serverless PostgreSQL with SQLModel ORM.

**Rationale**:
- Neon is the constitution-approved database for Phase II
- Serverless architecture scales to zero, cost-effective for development
- PostgreSQL provides ACID compliance and relational integrity
- SQLModel provides type-safe ORM with native Pydantic integration
- Automatic relationship handling between User and Todo entities

**Connection Strategy**:
- Use SQLModel's async database connection
- Connection pooling managed by SQLModel/SQLAlchemy
- Environment variables for database URL configuration

### Frontend Framework (Next.js)

**Decision**: Use Next.js 14+ with App Router and TypeScript.

**Rationale**:
- Next.js is the constitution-approved frontend framework for Phase II
- App Router provides modern React Server Components
- Built-in routing and page structure
- Excellent developer experience and performance
- TypeScript integration for type safety

**UI Strategy**:
- Use a CSS framework (Tailwind CSS) for responsive design
- Mobile-first approach for desktop and mobile compatibility
- Client-side authentication state management with Better Auth
- Server Components for data fetching where appropriate

### API Communication

**Decision**: REST API with JSON payloads, frontend uses fetch API.

**Rationale**:
- REST is the standard pattern for web APIs
- JSON format required by spec (FR-API-007)
- No real-time features needed (FR-NF-003)
- Simple fetch API sufficient; no additional HTTP client needed

**Auth Token Flow**:
- Better Auth manages session cookies
- Cookies automatically sent with API requests
- Backend validates session on each protected request
- 401 responses trigger frontend redirect to sign-in

## Phase 1: Design Documents

### Data Model Design

See [data-model.md](data-model.md) for detailed entity definitions.

### API Contracts

See [contracts/api-contracts.md](contracts/api-contracts.md) for endpoint specifications.

### Quick Start Guide

See [quickstart.md](quickstart.md) for local development setup.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations requiring justification. All design decisions align with Phase II technology stack as defined in the constitution.

## Open Questions

No open questions. All technical decisions derived from constitution-approved technologies and spec requirements.
