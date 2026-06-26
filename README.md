# AI Job Portal Backend

This project is a FastAPI-based backend for an AI job portal system. It currently implements user authentication, token-based authorization, database access, and a basic user model.

## Project Structure

- `app/main.py`
  - FastAPI application entry point.
  - Includes the `users` router and exposes a root health endpoint.

- `app/api/auth.py`
  - Authentication routes:
    - `POST /auth/register` — user registration.
    - `POST /auth/login` — user login and JWT token generation.
    - `GET /auth/me` — returns the authenticated user's profile.

- `app/api/users.py`
  - Placeholder users router.
  - Current route: `GET /users/` returns a simple confirmation message.

- `app/core/config.py`
  - Loads environment variables using `pydantic-settings`.
  - Required settings:
    - `DATABASE_URL`
    - `SECRET_KEY`
    - `ALGORITHM`
    - `ACCESS_TOKEN_EXPIRE_MINUTES`

- `app/core/security.py`
  - Password hashing and verification with `passlib`.
  - JWT creation and decoding using `python-jose`.

- `app/dependencies/database.py`
  - Database session dependency for FastAPI routes.

- `app/dependencies/auth_dependencies.py`
  - `get_current_user` dependency for protected routes.
  - Decodes bearer tokens and loads the user from the database.

- `app/db/session.py`
  - SQLAlchemy database engine and session configuration.
  - Uses `settings.DATABASE_URL` from `.env`.

- `app/models/base.py`
  - SQLAlchemy base class and timestamp mixin.

- `app/models/user.py`
  - `User` model definition.
  - Fields include email, password hash, role, active state, verification state, last login, and audit timestamps.
  - Includes a roles enum: `jobseeker`, `recruiter`, `admin`.

- `app/repositories/user_repository.py`
  - User database persistence logic.
  - Supports create, read, update, delete, activation, deactivation, verification, and login tracking.

- `app/services/auth_service.py`
  - Registration and login business logic.
  - Uses `user_repository` and `core.security` for password and token handling.

- `app/services/user_service.py`
  - Higher-level user operations such as fetching, updating, verifying, and deleting users.

- `app/schemas/auth.py`
  - Pydantic request/response models for auth routes.

- `app/schemas/user.py`
  - Pydantic user response and update schemas.

- `app/utils/security.py`
  - Helper functions for password hashing.
  - Note: authentication currently uses `app/core/security.py`.

- `app/utils/jwt.py`
  - JWT helper functions.
  - Note: the active auth service uses the JWT helpers from `app/core/security.py`.

## Current Functionality

- User registration with email, password, and role.
- User login with email and password.
- JWT authentication for protecting endpoints.
- `GET /auth/me` returns the logged-in user.
- Database integration through SQLAlchemy and a Postgres connection URL.

## Required Environment Configuration

The project uses a `.env` file at the project root.

Example `.env` values:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/jobportal
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The current repository includes a `.env` with `DATABASE_URL`, but `SECRET_KEY`, `ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES` must also be provided.

## Installation

1. Create and activate a Python environment:

```powershell
python -m venv venv
venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib[bcrypt] pydantic-settings
```

3. Fill in the `.env` file with your database and JWT settings.

## Run the Application

Start the app with Uvicorn:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- `http://localhost:8000/` — root status
- `http://localhost:8000/docs` — Swagger UI

## API Endpoints

- `GET /`
  - Returns a basic API health message.

- `POST /auth/register`
  - Request body: `email`, `password`, `role`
  - Returns created user data.

- `POST /auth/login`
  - Request body: `email`, `password`
  - Returns `access_token` and `token_type`.

- `GET /auth/me`
  - Requires `Authorization: Bearer <token>` header.
  - Returns the current authenticated user's details.

- `GET /users/`
  - Placeholder route currently returning a confirmation message.

## Notes and Next Steps

- The user model has additional commented-out relationship fields for profiles, skills, companies, and applications.
- `app/api/users.py` is currently a placeholder and can be expanded to support user listing, updating, or admin operations.
- Alembic is present via `alembic.ini`, so database migrations can be added and configured later.
- The current codebase already separates concerns into routers, services, repositories, schemas, and dependencies.

## Helpful Commands

- Run the app: `uvicorn app.main:app --reload`
- Open docs: `http://localhost:8000/docs`
- Add migrations later with Alembic if configured.

## Summary

This FastAPI backend supports user authentication and JWT authorization on a PostgreSQL database. It is built with clear separation between API routers, business services, repositories, models, and shared dependencies. The current implementation is focused on auth flow and user identity management.
