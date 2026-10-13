# Verify

```bash
# 1. Database (from a WSL shell, in this folder)
docker compose up -d

# 1b. Only if the volume predates users (notes has no user_id column):
docker compose exec -T db psql -v ON_ERROR_STOP=1 -U notes -d notes -f - < migrations/001_users.sql

# 2. Python env (PowerShell, in this folder). Copy .env.example to .env and set JWT_SECRET.
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# 3. Run the API. Interactive docs are at http://localhost:8000/docs
#    Register, log in, then paste the access_token into the Authorize button.
.venv\Scripts\uvicorn app.application:app --reload

# 4. The spec (integration tests against the running Postgres)
.venv\Scripts\pytest -v
```

Done = every test in `tests/` passes.
