# Decisions

## 2026-09-22: Postgres over MySQL
Either works. Picked Postgres because `RETURNING *` saves a second query on every
write, and the sibling `gemini-notes-api` / `stock-research-api` projects
already use psycopg.

## 2026-09-22: Raw SQL (psycopg), no ORM
The point is learning what the database actually does. An ORM (SQLAlchemy) hides
the SQL. Revisit once raw SQL feels boring. That's the right time for an ORM.

## 2026-09-22: Only the DB is containerized
The API runs with uvicorn on the host, so tracebacks and reloads stay fast.
Add an API Dockerfile once CRUD works. That step is what makes it deployable as
a "real" microservice.

## 2026-09-24: Layered architecture (controller → service → repository)
Requested by the team lead, who wants the service built one layer at a time.
- Controller (`app/main.py`): HTTP only. Parses requests, calls the service,
  turns `NoteNotFound` into a 404.
- Service (`app/service.py`): business rules. Knows nothing about HTTP.
- Repository (`app/repository.py`): the only place SQL lives.
The connection comes from `Depends(get_conn)` in the controller and is passed down,
so each request stays a single transaction.

## 2026-09-28: Packages for every layer, entity/DTO split, classes
The team lead's requirement: entity, DTO, controller, service, repository and a util
package, with no main.py god file.
- Entity (`@dataclass Note`) is the internal shape and DTOs (Pydantic) are the wire shape,
  so the DB and the API contract can change independently.
- Service and repository are classes, wired via `Depends` in `util/dependencies.py`
  (kept out of service so the service never imports FastAPI).
- Not found: the repository returns None, the service raises `NoteNotFoundError`, and one
  exception handler in `application.py` returns 404. Controllers need no try/except.

## 2026-10-13: Users + JWT auth, notes owned by a user
- **JWT access tokens (PyJWT, HS256, 60 min)** over DB sessions. The signature proves the token,
  so any replica can check it without a shared session store. Trade-off: no logout before
  expiry. `get_current_user` still loads the user row, so a deleted user's token stops working.
- **stdlib `hashlib.scrypt`** for passwords (OWASP cost: n=2^14, r=8, p=1, 16-byte salt),
  stored as `scrypt$salt$hash`. No passlib/bcrypt dependency.
- **Ownership is a SQL filter**, not a check after loading: `WHERE id = %s AND user_id = %s`.
  Another user's note looks the same as a missing one (404), so ids can't be probed.
- **Register uses `INSERT ... ON CONFLICT (email) DO NOTHING`** instead of SELECT-then-INSERT,
  so two simultaneous signups with one email can't both pass the check.
- Emails are lowercased in the service before storing or looking up.
- `HTTPBearer` instead of `OAuth2PasswordBearer`: login takes JSON, and the form-based flow
  would need `python-multipart`. Swagger's Authorize button takes the pasted token.
- Existing DBs migrate with `migrations/001_users.sql` (hand-run). Alembic stays on the later list.
