# State

## Current status (2026-10-13)
Users and JWT authentication are in, and notes belong to a user.
- **Register**: POST /auth/register returns 201, 409 for a taken email (case-insensitive), 422 for a bad email or a password under 8 chars.
- **Login**: POST /auth/login returns `{access_token, token_type}`. Wrong password and unknown email give the same 401.
- **Me**: GET /users/me returns the current user.
- **Notes**: every /notes route needs `Authorization: Bearer <token>` (401 without). Users only see their own notes; someone else's note is a 404.

Integration suite (HTTP + real Postgres): 13 passed.
The local DB was migrated with `migrations/001_users.sql`, which deleted the 3 ownerless test notes.

## Next step
Committed locally (no remote yet). Before creating a GitHub repo and pushing, run `/security-review`.
The project is on the resume as the Digital Sherpa capstone, so be ready to explain every layer.

## Later, not now
- API Dockerfile + add the api service to docker-compose
- Pagination on list
- Alembic migrations (replace hand-run `migrations/*.sql`)
- Refresh tokens / logout (JWTs can't be revoked before they expire)
- Rate-limit /auth/login
