---

description: "Phase II implementation tasks for full-stack web todo application"
---

# Tasks: Phase II Full-Stack Web Todo Application

**Input**: Design documents from `/specs/002-phase-ii-web-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/api-contracts.md, quickstart.md

**Tests**: Tests are NOT requested in spec - skip test tasks

**Organization**: Tasks grouped by user story for independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

### Backend Setup

- [ ] T001 Create backend directory structure per plan.md: `backend/src/{models,services,api,auth,main.py}`
- [ ] T002 Create backend/requirements.txt with dependencies: fastapi, uvicorn, sqlmodel, better-auth, bcrypt, python-dotenv
- [ ] T003 Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL, SESSION_MAX_AGE

### Frontend Setup

- [ ] T004 Create frontend directory structure per plan.md: `frontend/src/{app/{auth,todos},components/{ui,auth,todos},lib,types}`
- [ ] T005 Initialize Next.js 14+ project with TypeScript in frontend/ using `npx create-next-app@latest`
- [ ] T006 Configure frontend/package.json with dependencies: next, react, react-dom, tailwindcss, better-auth
- [ ] T007 Create frontend/.env.local with NEXT_PUBLIC_API_URL and BETTER_AUTH_URL

### Shared Setup

- [ ] T008 Create tests/ directory structure: `tests/contract/`, `tests/e2e/`
- [ ] T009 [P] Configure linting: ruff for Python, eslint for TypeScript
- [ ] T010 [P] Configure formatting: black for Python, prettier for TypeScript

**Checkpoint**: Setup complete - both backend and frontend project structures created

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [ ] T011 Create backend/src/models/database.py with SQLModel async engine setup for Neon PostgreSQL
- [ ] T012 Create backend/src/models/__init__.py exporting User, Todo, and database utilities
- [ ] T013 Create backend/src/models/user.py with User SQLModel entity per data-model.md
- [ ] T014 Create backend/src/models/todo.py with Todo SQLModel entity per data-model.md
- [ ] T015 [P] Create database initialization script to create tables in Neon PostgreSQL

### Authentication Foundation

- [ ] T016 Create backend/src/auth/config.py with Better Auth configuration
- [ ] T017 Create backend/src/auth/server.py with Better Auth server instance
- [ ] T018 Create backend/src/auth/middleware.py with session validation dependency for protected routes
- [ ] T019 [P] Create backend/src/auth/schemas.py with Pydantic schemas for auth requests/responses

### API Foundation

- [ ] T020 Create backend/src/api/__init__.py with API router exports
- [ ] T021 Create backend/src/main.py with FastAPI app initialization and CORS configuration
- [ ] T022 [P] Create backend/src/api/dependencies.py with auth dependency and ownership verification helpers

### Frontend Foundation

- [ ] T023 Create frontend/src/lib/api.ts with fetch wrapper including credentials: 'include'
- [ ] T024 Create frontend/src/types/index.ts with TypeScript interfaces matching API responses
- [ ] T025 [P] Create frontend/src/lib/auth-client.ts with Better Auth client configuration
- [ ] T026 Create frontend/src/app/layout.tsx with root layout including AuthProvider

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Allow new users to create accounts with email and password

**Independent Test**: Can be fully tested by registering a new user and verifying account exists in database

### Backend Implementation (User Registration)

- [ ] T027 [US1] Create POST /auth/signup endpoint in backend/src/api/auth/signup.py per api-contracts.md
- [ ] T028 [US1] Implement email validation (format check) and password length validation (min 8 chars)
- [ ] T029 [US1] Implement duplicate email check against database
- [ ] T030 [US1] Implement password hashing with bcrypt before storage
- [ ] T031 [US1] Return 201 Created with user data on success, 400 with error message on failure

### Frontend Implementation (User Registration)

- [ ] T032 [US1] Create frontend/src/app/(auth)/signup/page.tsx with signup form UI
- [ ] T033 [US1] Create frontend/src/components/auth/signup-form.tsx with email, password, confirm password fields
- [ ] T034 [US1] Implement form validation (email format, password min 8 chars, passwords match)
- [ ] T035 [US1] Call POST /auth/signup and handle success (redirect to signin) or error (display message)
- [ ] T036 [US1] Create frontend/src/app/(auth)/layout.tsx with shared auth layout styling

**Checkpoint**: User Registration complete and testable

---

## Phase 4: User Story 2 - User Sign In (Priority: P1)

**Goal**: Allow registered users to sign in and establish authenticated session

**Independent Test**: Can be fully tested by signing in with valid credentials and verifying session is established

### Backend Implementation (User Sign In)

- [ ] T037 [US2] Create POST /auth/signin endpoint in backend/src/api/auth/signin.py per api-contracts.md
- [ ] T038 [US2] Implement credential validation (email exists, password matches hash)
- [ ] T039 [US2] Return 200 OK with session cookie on success, 401 Unauthorized on failure
- [ ] T040 [US2] Create POST /auth/signout endpoint in backend/src/api/auth/signout.py

### Frontend Implementation (User Sign In)

- [ ] T041 [US2] Create frontend/src/app/(auth)/signin/page.tsx with signin page UI
- [ ] T042 [US2] Create frontend/src/components/auth/signin-form.tsx with email and password fields
- [ ] T043 [US2] Implement form validation for required fields
- [ ] T044 [US2] Call POST /auth/signin with credentials and handle success (redirect to /todos) or error
- [ ] T045 [US2] Implement redirect from /signin to /todos when already authenticated (via useEffect)

**Checkpoint**: User Sign In complete and testable

---

## Phase 5: User Story 3 - View Todo List (Priority: P1)

**Goal**: Display all todos belonging to the authenticated user

**Independent Test**: Can be fully tested by signing in and verifying all user's todos are displayed

### Backend Implementation (View Todos)

- [ ] T046 [US3] Create GET /todos endpoint in backend/src/api/todos/list.py per api-contracts.md
- [ ] T047 [US3] Validate session via auth middleware
- [ ] T048 [US3] Query todos filtered by user_id
- [ ] T049 [US3] Return 200 OK with todos array, 401 Unauthorized if not authenticated

### Frontend Implementation (View Todos)

- [ ] T050 [US3] Create frontend/src/app/todos/page.tsx with protected todo list page
- [ ] T051 [US3] Create frontend/src/components/todos/todo-list.tsx with todo display components
- [ ] T052 [US3] Fetch todos from GET /todos on page load using credentials: 'include'
- [ ] T053 [US3] Display todos in a list with title, description, complete status
- [ ] T054 [US3] Handle empty state (no todos) with friendly message per spec
- [ ] T055 [US3] Add signout button redirecting to signin page

**Checkpoint**: View Todo List complete and testable

---

## Phase 6: User Story 4 - Create Todo (Priority: P1)

**Goal**: Allow authenticated users to add new todos to their list

**Independent Test**: Can be fully tested by creating a new todo and verifying it appears in the list

### Backend Implementation (Create Todo)

- [ ] T056 [US4] Create POST /todos endpoint in backend/src/api/todos/create.py per api-contracts.md
- [ ] T057 [US4] Validate session via auth middleware
- [ ] T058 [US4] Validate request body (title required, max 200 chars, description optional max 2000)
- [ ] T059 [US4] Create todo with user_id set to current user
- [ ] T060 [US4] Return 201 Created with created todo, 400 with validation error

### Frontend Implementation (Create Todo)

- [ ] T061 [US4] Create frontend/src/app/todos/new/page.tsx with todo creation page
- [ ] T062 [US4] Create frontend/src/components/todos/todo-form.tsx with title and optional description fields
- [ ] T063 [US4] Implement form validation (title required, max 200 chars)
- [ ] T064 [US4] Call POST /todos and handle success (redirect to todo list) or error
- [ ] T065 [US4] Add "Add Todo" button on todo list page linking to /todos/new

**Checkpoint**: Create Todo complete and testable

---

## Phase 7: User Story 5 - Edit Todo (Priority: P2)

**Goal**: Allow authenticated users to modify existing todos

**Independent Test**: Can be fully tested by editing a todo's title/description and verifying changes persist

### Backend Implementation (Edit Todo)

- [ ] T066 [US5] Create GET /todos/:id endpoint in backend/src/api/todos/detail.py per api-contracts.md
- [ ] T067 [US5] Create PUT /todos/:id endpoint in backend/src/api/todos/update.py per api-contracts.md
- [ ] T068 [US5] Implement ownership verification (todo.user_id == current_user.id)
- [ ] T069 [US5] Return 403 Forbidden if not owner, 404 Not Found if not exists
- [ ] T070 [US5] Validate request body (title optional but required if provided, max 200 chars)

### Frontend Implementation (Edit Todo)

- [ ] T071 [US5] Create frontend/src/app/todos/[id]/page.tsx with todo edit page
- [ ] T072 [US5] Create frontend/src/components/todos/todo-edit-form.tsx pre-populated with existing values
- [ ] T073 [US5] Implement form validation (title required if provided, max 200 chars)
- [ ] T074 [US5] Call PUT /todos/:id and handle success (redirect to todo list) or error
- [ ] T075 [US5] Add "Edit" button on each todo in the list linking to /todos/[id]

**Checkpoint**: Edit Todo complete and testable

---

## Phase 8: User Story 6 - Delete Todo (Priority: P2)

**Goal**: Allow authenticated users to remove todos from their list

**Independent Test**: Can be fully tested by deleting a todo and verifying it no longer appears

### Backend Implementation (Delete Todo)

- [ ] T076 [US6] Create DELETE /todos/:id endpoint in backend/src/api/todos/delete.py per api-contracts.md
- [ ] T077 [US6] Implement ownership verification (todo.user_id == current_user.id)
- [ ] T078 [US6] Return 200 OK on success, 403 Forbidden if not owner, 404 Not Found

### Frontend Implementation (Delete Todo)

- [ ] T079 [US6] Create frontend/src/components/todos/delete-confirm.tsx with confirmation dialog UI
- [ ] T080 [US6] Add delete button to each todo in the list with confirmation
- [ ] T081 [US6] Call DELETE /todos/:id on confirmation and remove todo from list on success
- [ ] T082 [US6] Handle cancel by keeping todo in list

**Checkpoint**: Delete Todo complete and testable

---

## Phase 9: User Story 7 - Toggle Todo Complete (Priority: P1)

**Goal**: Allow authenticated users to mark todos as complete/incomplete

**Independent Test**: Can be fully tested by toggling a todo's status and verifying the visual change

### Backend Implementation (Toggle Todo)

- [ ] T083 [US7] Create PATCH /todos/:id/toggle endpoint in backend/src/api/todos/toggle.py per api-contracts.md
- [ ] T084 [US7] Implement ownership verification (todo.user_id == current_user.id)
- [ ] T085 [US7] Flip is_complete boolean value
- [ ] T086 [US7] Return 200 OK with updated todo, 403 Forbidden if not owner

### Frontend Implementation (Toggle Todo)

- [ ] T087 [US7] Add checkbox or toggle button to each todo in the todo list
- [ ] T088 [US7] Call PATCH /todos/:id/toggle when toggled
- [ ] T089 [US7] Update todo's visual appearance based on complete status (strikethrough or color)
- [ ] T090 [US7] Handle API errors by reverting visual state

**Checkpoint**: Toggle Todo Complete complete and testable

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Backend Polish

- [ ] T091 [P] Implement consistent error handling across all API endpoints
- [ ] T092 [P] Add input validation using Pydantic models for all request bodies
- [ ] T093 [P] Add rate limiting on auth endpoints (5 attempts per minute)

### Frontend Polish

- [ ] T094 [P] Implement responsive layout for desktop and mobile using Tailwind CSS
- [ ] T095 [P] Add loading states during API calls (spinners or skeleton loaders)
- [ ] T096 [P] Handle error messages from API and display user-friendly feedback
- [ ] T097 [P] Add empty state UI for todo list (no todos message)
- [ ] T098 [P] Ensure consistent styling across all pages and components

### Integration Polish

- [ ] T099 [P] Test full auth flow: signup → signin → create todo → toggle → signout
- [ ] T100 [P] Verify local development setup works per quickstart.md

**Checkpoint**: All phases complete - full application ready for testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-9)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) or sequentially in priority order
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Priority | Depends On | Can Start After |
|-------|----------|------------|-----------------|
| US1: Registration | P1 | Phase 2 | Phase 2 complete |
| US2: Sign In | P1 | Phase 2 | Phase 2 complete |
| US3: View Todos | P1 | Phase 2 | Phase 2 complete |
| US4: Create Todo | P1 | Phase 2 | Phase 2 complete |
| US5: Edit Todo | P2 | Phase 2 | Phase 2 complete |
| US6: Delete Todo | P2 | Phase 2 | Phase 2 complete |
| US7: Toggle Complete | P1 | Phase 2 | Phase 2 complete |

### Within Each User Story

- Backend models before backend endpoints
- Backend endpoints before frontend pages
- Frontend components before page integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel
- All backend model tasks in a story can run in parallel
- All backend endpoint tasks in a story can run in parallel
- All frontend component tasks in a story can run in parallel

---

## Parallel Execution Examples

### Phase 1: Setup (can run in parallel)
```bash
Task T001: Create backend directory structure
Task T004: Create frontend directory structure
Task T008: Create tests directory structure
Task T009: Configure linting for Python
Task T010: Configure formatting for Python
```

### Phase 2: Foundational (can run in parallel within phase)
```bash
Task T011: Create database.py
Task T013: Create user.py model
Task T014: Create todo.py model
Task T016: Create auth config
Task T017: Create auth server
Task T018: Create auth middleware
Task T019: Create auth schemas
Task T020: Create API router
Task T021: Create main.py
Task T022: Create dependencies
Task T023: Create frontend API lib
Task T024: Create TypeScript types
Task T025: Create auth client
Task T026: Create root layout
```

### User Story Implementation (can run in parallel across stories)
```bash
# Once Phase 2 is complete, these can all run in parallel:
Task T027-T031: User Registration (backend + frontend)
Task T037-T040: User Sign In (backend + frontend)
Task T046-T049: View Todos (backend)
Task T056-T060: Create Todo (backend)
# etc.
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Registration) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Sign In) → Test independently → Deploy/Demo
4. Add User Story 3 (View Todos) → Test independently → Deploy/Demo
5. Add User Story 4 (Create Todo) → Test independently → Deploy/Demo
6. Add User Story 5 (Edit Todo) → Test independently → Deploy/Demo
7. Add User Story 6 (Delete Todo) → Test independently → Deploy/Demo
8. Add User Story 7 (Toggle Complete) → Test independently → Deploy/Demo
9. Polish → Final deployment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Registration)
   - Developer B: User Story 2 (Sign In)
   - Developer C: User Story 3 (View Todos) + User Story 4 (Create Todo)
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Description | Task Count |
|-------|-------------|------------|
| Phase 1 | Setup | 10 tasks |
| Phase 2 | Foundational | 16 tasks |
| Phase 3 | US1: User Registration | 10 tasks |
| Phase 4 | US2: User Sign In | 9 tasks |
| Phase 5 | US3: View Todo List | 10 tasks |
| Phase 6 | US4: Create Todo | 10 tasks |
| Phase 7 | US5: Edit Todo | 10 tasks |
| Phase 8 | US6: Delete Todo | 7 tasks |
| Phase 9 | US7: Toggle Complete | 8 tasks |
| Phase 10 | Polish & Cross-Cutting | 10 tasks |
| **Total** | | **100 tasks** |

### Task Count per User Story

| User Story | Priority | Tasks |
|------------|----------|-------|
| US1: Registration | P1 | 10 |
| US2: Sign In | P1 | 9 |
| US3: View Todos | P1 | 10 |
| US4: Create Todo | P1 | 10 |
| US5: Edit Todo | P2 | 10 |
| US6: Delete Todo | P2 | 7 |
| US7: Toggle Complete | P1 | 8 |

### Parallel Opportunities

- Phase 1: 5 parallel tasks (T001, T004, T008, T009, T010)
- Phase 2: 16 parallel tasks (T011-T026, all marked [P])
- User Stories: Each story's backend and frontend tasks can run in parallel once foundational is complete

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
