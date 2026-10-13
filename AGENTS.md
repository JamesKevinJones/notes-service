# Notes Service

One microservice: users register and log in (JWT), then CRUD their own notes, stored in Postgres. It's a **learning project**.
The user writes the TODO bodies in the service, repository and controller layers, and agents review them. Don't
fill in the `TODO(n)` blocks unless the user asks for that.

## Stack
- FastAPI + uvicorn (the API, run locally)
- Postgres 17 in Docker (`docker-compose.yml`). The machine uses native Docker in WSL,
  so run `docker compose` from a WSL shell.
- psycopg 3 with raw SQL. No ORM, on purpose (see docs/DECISIONS.md).
- Auth: PyJWT (HS256 bearer tokens, 60 min) + stdlib `hashlib.scrypt` for password hashes.

## Layout (layered packages, set by the team lead)
- `schema.sql`: `users` + `notes` tables. Runs once when the DB volume is created.
- `migrations/`: hand-run SQL for volumes created before a schema change (`001_users.sql`).
- `app/application.py`: entry point. Builds the app, includes routers, maps exceptions to 404 / 409 / 401.
- `app/controller/`: HTTP only. Validates DTOs, calls one service method, returns a response DTO.
- `app/service/`: `NoteService`, `AuthService`, the business rules. No FastAPI, no SQL.
- `app/repository/`: `NoteRepository`, `UserRepository`, the only place SQL lives. Returns entities or None.
  Every notes query filters on `user_id`, so another user's note is a 404, never a 403.
- `app/entity/`: `Note`, `User` dataclasses that mirror DB rows (internal shape).
- `app/dto/`: Pydantic request/response models (the wire shape).
- `app/util/`: DB connection, the `Depends` wiring chain (incl. `get_current_user`), exceptions,
  `security.py` (password hashing, token create/decode).
- `tests/`: integration tests through HTTP against the real Postgres. `conftest.py` has the
  `signup` fixture, which returns an auth header for a fresh user. All green = done.

## Rules
- Each layer only calls the layer directly below it.
- SQL values are always parameterized (`%s`). Never f-string SQL.
- Every notes query is scoped by `user_id`. No response DTO ever carries a password hash.
- No Claude co-author lines on commits.

## System Operating Modes

Each mode is a persona defined in `.claude/modes/`. It sets what to focus on,
how to judge the work, and the output format.

| Mode | File | Switch (Claude Code) | Badge |
| --- | --- | --- | --- |
| Business Analyst | `ba.md` | `/mode ba` or `/ba` | `[Mode: Business Analyst]` |
| System Architect | `architect.md` | `/mode architect` or `/architect` | `[Mode: System Architect]` |
| Engineer (**default**) | `engineer.md` | `/mode engineer` or `/code` | `[Mode: Engineer]` |
| Auditor | `auditor.md` | `/mode auditor` or `/audit` | `[Mode: Auditor]` |

- `/mode reset` returns to Engineer.
- **Start every response with the current mode's badge on its own line.** If no mode has been chosen this session, use `[Mode: Engineer]`.
- A mode lasts until it is switched or reset. The Rules above apply in every mode.
- Codex and `agy` don't have these slash commands. Say "switch to ba mode" and they read `.claude/modes/ba.md` directly.
