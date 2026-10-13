-- For a database created before users existed. A fresh volume gets all of this from schema.sql.
-- Run once:  docker compose exec -T db psql -U notes -d notes -f - < migrations/001_users.sql
BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id             SERIAL PRIMARY KEY,
    email          TEXT        NOT NULL UNIQUE,
    password_hash  TEXT        NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Existing notes have no owner, so they can't satisfy NOT NULL. They were test data.
DELETE FROM notes;

ALTER TABLE notes
    ADD COLUMN IF NOT EXISTS user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS notes_user_created_idx ON notes (user_id, created_at DESC);

COMMIT;
