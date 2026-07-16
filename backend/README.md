# AI Job Portal — Backend

Lightweight FastAPI backend for the AI Job Portal project. Focused on user authentication, JWT authorization, and PostgreSQL-based persistence with clear separation of routers, services, repositories, and models.

## Features

- User registration and login (email + password)
- JWT-based authentication and protected endpoints
- Role support: `jobseeker`, `recruiter`, `admin`
- SQLAlchemy models and repository layer
- Alembic present for migrations

## Quick Start

Requirements: Python 3.10+ and a Postgres database.

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

2. Install dependencies (uses `requirements.txt`):

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` (create if missing) and set the required vars:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/jobportal
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

4. Apply database migrations (Alembic):

```powershell
alembic upgrade head
```

5. Run the application:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/docs` for the Swagger UI.

## Project Layout (key files)

- `app/main.py` — FastAPI application entrypoint
- `app/api/*` — API routers (auth, users, company, jobs, resumes, skills)
- `app/services/*` — Business logic
- `app/repositories/*` — DB persistence layer
- `app/models/*` — SQLAlchemy models
- `app/schemas/*` — Pydantic request/response models
- `app/db/session.py` — DB engine and session
- `alembic/` + `alembic.ini` — Migrations

## Environment Variables

Provide the following in `.env` at project root:
- `DATABASE_URL` — Postgres connection URL
- `SECRET_KEY` — JWT secret
- `ALGORITHM` — JWT algorithm (e.g. `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token lifetime in minutes

## Running Tests

If you add tests under `app/tests/`, run them with `pytest`:

```powershell
pip install pytest
pytest -q
```

## Development Notes

- The current implementation focuses on authentication and user management. `app/api/users.py` is a placeholder and can be extended for admin operations and user listing.
- Uploaded resumes are stored under `uploads/resumes/` — ensure that directory exists and is writable.

## Helpful Commands

- Start dev server: `uvicorn app.main:app --reload`
- DB migrations: `alembic revision --autogenerate -m "msg"` then `alembic upgrade head`

## Next Steps

- Expand `users` endpoints for admin use-cases
- Add automated tests for services and repositories
- Add CI workflow to run linting and tests

---

If you'd like, I can further tailor this README (add API examples, curl snippets, or Docker instructions). 
