from psycopg import Connection

from app.entity.user import User


class UserRepository:

    def __init__(self, conn: Connection):
        self.conn = conn

    def insert(self, email: str, password_hash: str) -> User | None:
        """None when the email is already taken. ON CONFLICT avoids a check-then-insert race."""
        row = self.conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) "
            "ON CONFLICT (email) DO NOTHING RETURNING *",
            (email, password_hash),
        ).fetchone()
        return User(**row) if row else None

    def find_by_email(self, email: str) -> User | None:
        row = self.conn.execute("SELECT * FROM users WHERE email = %s", (email,)).fetchone()
        return User(**row) if row else None

    def find_by_id(self, user_id: int) -> User | None:
        row = self.conn.execute("SELECT * FROM users WHERE id = %s", (user_id,)).fetchone()
        return User(**row) if row else None
