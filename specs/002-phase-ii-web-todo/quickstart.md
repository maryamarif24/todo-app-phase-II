# Quickstart: Phase II Full-Stack Web Todo Application

**Feature**: Phase II Full-Stack Web Todo Application
**Date**: 2024-12-27
**Branch**: `002-phase-ii-web-todo`

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend runtime |
| npm or pnpm | Latest | Frontend package manager |
| Git | Latest | Version control |

## Project Structure

```
todo-app-cli/
├── backend/              # FastAPI backend
│   ├── src/
│   │   ├── main.py      # Application entry point
│   │   ├── models/      # SQLModel entities
│   │   ├── services/    # Business logic
│   │   ├── api/         # API routes
│   │   └── auth/        # Authentication
│   └── requirements.txt
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/         # App Router pages
│   │   ├── components/  # React components
│   │   └── lib/         # Utilities
│   └── package.json
└── CLAUDE.md            # Agent instructions
```

## Environment Setup

### 1. Clone and Branch

```bash
git checkout 002-phase-ii-web-todo
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your Neon database URL
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install
```

### 4. Environment Variables

Create `.env` file in `backend/` directory:

```env
# Neon PostgreSQL connection string
DATABASE_URL=postgresql://user:password@ep-xyz.region.neon.tech/dbname?sslmode=require

# Better Auth secret (generate with: openssl rand -base64 32)
BETTER_AUTH_SECRET=your-secret-key-here

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# Session configuration
SESSION_MAX_AGE=86400  # 24 hours in seconds
```

Create `.env.local` file in `frontend/` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth configuration
BETTER_AUTH_URL=http://localhost:8000
```

## Running the Application

### 1. Start the Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload
```

The backend runs at `http://localhost:8000`.
API documentation available at `http://localhost:8000/docs`.

### 2. Start the Frontend

```bash
cd frontend
npm run dev
# or
pnpm dev
```

The frontend runs at `http://localhost:3000`.

### 3. Access the Application

1. Open `http://localhost:3000`
2. Click "Sign Up" to create an account
3. Verify email and complete registration
4. Sign in with your credentials
5. Start managing your todos

## Development Workflow

### Running Tests

**Backend tests**:
```bash
cd backend
pytest
```

**Frontend tests**:
```bash
cd frontend
npm test
# or
pnpm test
```

### Database Migrations

```bash
cd backend
alembic upgrade head
```

### Linting and Formatting

**Backend**:
```bash
cd backend
ruff check .
black .
```

**Frontend**:
```bash
cd frontend
npm run lint
npm run format
# or
pnpm lint
pnpm format
```

## Common Issues

### Issue: Database Connection Failed

**Solution**: Verify your `DATABASE_URL` in `.env`:
- Ensure the URL includes `?sslmode=require`
- Check that your Neon credentials are correct
- Verify your IP is allowlisted in Neon dashboard

### Issue: CORS Errors

**Solution**: Ensure `FRONTEND_URL` in backend `.env` matches your frontend URL exactly.

### Issue: Session Not Persisting

**Solution**: Check that:
1. `credentials: 'include'` is set in frontend fetch calls
2. Cookies are not being blocked by browser settings
3. Frontend and backend are on the same domain or CORS is configured correctly

## Next Steps

1. Review the [specification](spec.md) for requirements
2. Review the [data model](data-model.md) for database design
3. Review [API contracts](contracts/api-contracts.md) for endpoint details
4. Proceed to `/sp.tasks` for implementation tasks
