# Data Model: Phase II Full-Stack Web Todo Application

**Feature**: Phase II Full-Stack Web Todo Application
**Date**: 2024-12-27
**Branch**: `002-phase-ii-web-todo`

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                           User                                   │
├─────────────────────────────────────────────────────────────────┤
│ • id: UUID (PK)                                                 │
│ • email: String (unique, indexed)                               │
│ • password_hash: String                                         │
│ • created_at: DateTime                                          │
│ • updated_at: DateTime                                          │
└─────────────────────────────────────────────────────────────────┘
                              │ 1:n
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                           Todo                                   │
├─────────────────────────────────────────────────────────────────┤
│ • id: UUID (PK)                                                 │
│ • user_id: UUID (FK, indexed)                                   │
│ • title: String (min 1, max 200 chars)                          │
│ • description: String (optional, max 2000 chars)                │
│ • is_complete: Boolean (default false)                          │
│ • created_at: DateTime                                          │
│ • updated_at: DateTime                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Entity Definitions

### User Entity

Represents an authenticated user of the application.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique user identifier |
| email | String | Unique, Indexed, Max 255, Email format | User's email address |
| password_hash | String | Min 60 chars (bcrypt output) | Hashed password |
| created_at | DateTime | Auto-generated | Account creation timestamp |
| updated_at | DateTime | Auto-generated | Last update timestamp |

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Email must be unique (database constraint)
- Password must be hashed before storage (bcrypt)
- Password minimum length: 8 characters before hashing

**Relationships**:
- One-to-Many with Todo (a user has zero or more todos)

### Todo Entity

Represents a task item owned by a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique todo identifier |
| user_id | UUID | Foreign Key, Indexed | Owning user identifier |
| title | String | Min 1, Max 200 chars | Todo title (required) |
| description | String | Max 2000 chars, Optional | Todo description |
| is_complete | Boolean | Default false | Completion status |
| created_at | DateTime | Auto-generated | Creation timestamp |
| updated_at | DateTime | Auto-generated | Last update timestamp |

**Validation Rules**:
- Title is required (cannot be empty or whitespace only)
- Title maximum 200 characters
- Description maximum 2000 characters (if provided)
- Description is optional (can be null/empty)
- is_complete defaults to false

**Relationships**:
- Many-to-One with User (a todo belongs to exactly one user)
- User reference must exist (foreign key constraint)

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Todos Table

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_complete ON todos(user_id, is_complete);
```

## SQLModel Definitions (Type Hints)

### User Model (Python)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(min_length=60)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    todos: List["Todo"] = Relationship(back_populates="user")
```

### Todo Model (Python)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class Todo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", on_delete="CASCADE")
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="todos")
```

## Ownership Enforcement

The data model enforces user-to-todo ownership through:

1. **Foreign Key Constraint**: `todos.user_id` references `users.id`
2. **Cascade Delete**: When a user is deleted, all their todos are deleted
3. **Application-Level Checks**: API must verify `todo.user_id == current_user.id`

**Security Requirement**: Every API operation on todos MUST verify ownership:

```python
# Example ownership check pattern
async def get_todo(todo_id: UUID, current_user: User) -> Todo:
    todo = await db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return todo
```

## Index Strategy

| Index | Columns | Purpose |
|-------|---------|---------|
| idx_users_email | email | Fast email lookup for auth |
| idx_todos_user_id | user_id | Fast user-todo lookups |
| idx_todos_user_complete | user_id, is_complete | Efficient filtered list queries |

## Migration Strategy

Database migrations will be managed separately using Alembic:

1. Initial migration creates `users` and `todos` tables
2. Subsequent migrations for schema changes
3. Migration files tracked in version control
4. Production migrations applied during deployment

**Note**: Migration execution is not part of Phase II implementation tasks. It is a separate operational concern.
