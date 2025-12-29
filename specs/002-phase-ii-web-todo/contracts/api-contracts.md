# API Contracts: Phase II Full-Stack Web Todo Application

**Feature**: Phase II Full-Stack Web Todo Application
**Date**: 2024-12-27
**Branch**: `002-phase-ii-web-todo`

## API Overview

All API endpoints return JSON responses. Authentication endpoints are public; all todo endpoints require a valid session cookie. Errors return standard HTTP status codes with JSON error details.

## Authentication Endpoints (Public)

### POST /auth/signup

Create a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2024-12-27T10:00:00Z"
}
```

**Response (400 Bad Request)** - Validation error:
```json
{
  "detail": "Email already registered"
}
```

### POST /auth/signin

Authenticate an existing user.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com"
  },
  "session": {
    "token": "session_cookie_set",
    "expires_at": "2024-12-28T10:00:00Z"
  }
}
```

**Response (401 Unauthorized)** - Invalid credentials:
```json
{
  "detail": "Invalid email or password"
}
```

### POST /auth/signout

End the current user session.

**Request**: (empty body, cookies included)

**Response (200 OK)**:
```json
{
  "message": "Successfully signed out"
}
```

## Todo Endpoints (Protected)

All todo endpoints require a valid session cookie. Requests without authentication receive 401 Unauthorized.

### GET /todos

Retrieve all todos for the authenticated user.

**Request**: (cookies included, no body)

**Response (200 OK)**:
```json
{
  "todos": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "is_complete": false,
      "created_at": "2024-12-27T10:00:00Z",
      "updated_at": "2024-12-27T10:00:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "title": "Walk the dog",
      "description": null,
      "is_complete": true,
      "created_at": "2024-12-26T14:00:00Z",
      "updated_at": "2024-12-27T09:00:00Z"
    }
  ]
}
```

**Response (401 Unauthorized)**:
```json
{
  "detail": "Not authenticated"
}
```

### POST /todos

Create a new todo for the authenticated user.

**Request**:
```json
{
  "title": "New task",
  "description": "Optional description"
}
```

**Response (201 Created)**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440003",
  "title": "New task",
  "description": "Optional description",
  "is_complete": false,
  "created_at": "2024-12-27T10:30:00Z",
  "updated_at": "2024-12-27T10:30:00Z"
}
```

**Response (400 Bad Request)** - Validation error:
```json
{
  "detail": "Title is required"
}
```

### GET /todos/:id

Retrieve a specific todo by ID.

**Response (200 OK)**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440003",
  "title": "New task",
  "description": "Optional description",
  "is_complete": false,
  "created_at": "2024-12-27T10:30:00Z",
  "updated_at": "2024-12-27T10:30:00Z"
}
```

**Response (404 Not Found)**:
```json
{
  "detail": "Todo not found"
}
```

**Response (403 Forbidden)** - Not owner:
```json
{
  "detail": "Not authorized to access this todo"
}
```

### PUT /todos/:id

Update an existing todo.

**Request**:
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response (200 OK)**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440003",
  "title": "Updated title",
  "description": "Updated description",
  "is_complete": false,
  "created_at": "2024-12-27T10:30:00Z",
  "updated_at": "2024-12-27T11:00:00Z"
}
```

### PATCH /todos/:id/toggle

Toggle the complete status of a todo.

**Request**: (empty body, just the endpoint)

**Response (200 OK)**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440003",
  "title": "Updated title",
  "description": "Updated description",
  "is_complete": true,
  "created_at": "2024-12-27T10:30:00Z",
  "updated_at": "2024-12-27T11:00:00Z"
}
```

### DELETE /todos/:id

Delete a todo.

**Response (200 OK)**:
```json
{
  "message": "Todo deleted successfully"
}
```

**Response (404 Not Found)** - Already deleted:
```json
{
  "detail": "Todo not found"
}
```

## Error Response Format

All errors follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful operations |
| 201 | Created | Resource creation (signup, todo create) |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Not authorized to access resource |
| 404 | Not Found | Resource does not exist |
| 422 | Unprocessable Entity | Validation failed |
| 500 | Internal Server Error | Unexpected server errors |

## Authentication Flow

1. User submits signup form → POST /auth/signup → 201 Created + session cookie
2. User submits signin form → POST /auth/signin → 200 OK + session cookie
3. Session cookie automatically included in all subsequent requests
4. User clicks signout → POST /auth/signout → 200 OK + cookie cleared

## Frontend API Client

The frontend uses the fetch API with credentials:

```typescript
// Example: Fetch todos with session cookie
async function fetchTodos(): Promise<Todo[]> {
  const response = await fetch('/todos', {
    method: 'GET',
    credentials: 'include',  // Important: include cookies
  });

  if (!response.ok) {
    throw new Error('Failed to fetch todos');
  }

  const data = await response.json();
  return data.todos;
}
```

**Important**: `credentials: 'include'` is required for session cookies to be sent.
