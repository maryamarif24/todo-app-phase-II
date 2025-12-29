---
title: Worksy Todo API
emoji: ✅
colorFrom: pink
colorTo: red
sdk: docker
pinned: false
license: mit
---

# Worksy Todo API

A FastAPI backend for the Worksy Todo application.

## Features

- User authentication (signup, signin, signout)
- Todo CRUD operations
- PostgreSQL database (Neon)
- RESTful API design

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/signin` - Sign in user
- `POST /auth/signout` - Sign out user

### Todos
- `GET /todos` - List all todos
- `POST /todos` - Create new todo
- `GET /todos/{id}` - Get todo by ID
- `PUT /todos/{id}` - Update todo
- `PATCH /todos/{id}/toggle` - Toggle completion
- `DELETE /todos/{id}` - Delete todo

### Health
- `GET /` - Health check
- `GET /health` - Health status

## Environment Variables

Set these in your Hugging Face Space settings:

- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret for auth tokens
- `FRONTEND_URL` - Frontend URL for CORS
