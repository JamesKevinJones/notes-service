from psycopg import Connection

from app.entity.note import Note


class NoteRepository:
    """Every query is scoped to one owner, so another user's note looks exactly like a missing one."""

    def __init__(self, conn: Connection):
        self.conn = conn

    def insert(self, user_id: int, title: str, content: str) -> Note:
        row = self.conn.execute(
            "INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s) RETURNING *",
            (user_id, title, content),
        ).fetchone()
        return Note(**row)

    def find_all(self, user_id: int) -> list[Note]:
        rows = self.conn.execute(
            "SELECT * FROM notes WHERE user_id = %s ORDER BY created_at DESC, id DESC",
            (user_id,),
        ).fetchall()
        return [Note(**row) for row in rows]

    def find_by_id(self, user_id: int, note_id: int) -> Note | None:
        row = self.conn.execute(
            "SELECT * FROM notes WHERE id = %s AND user_id = %s",
            (note_id, user_id),
        ).fetchone()
        if row is None:
            return None
        return Note(**row)

    def update(self, user_id: int, note_id: int, title: str | None, content: str | None) -> Note | None:
        row = self.conn.execute(
            """
            UPDATE notes
            SET title = COALESCE(%s, title),
                content = COALESCE(%s, content),
                updated_at = now()
            WHERE id = %s AND user_id = %s
            RETURNING *
            """,
            (title, content, note_id, user_id),
        ).fetchone()
        if row is None:
            return None
        return Note(**row)

    def delete(self, user_id: int, note_id: int) -> bool:
        row = self.conn.execute(
            "DELETE FROM notes WHERE id = %s AND user_id = %s RETURNING id",
            (note_id, user_id),
        ).fetchone()
        return row is not None
