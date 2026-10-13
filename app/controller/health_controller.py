from fastapi import APIRouter, Depends
from psycopg import Connection

from app.util.database import get_conn

router = APIRouter(tags=["health"])


@router.get("/health")
def health(conn: Connection = Depends(get_conn)):
    conn.execute("SELECT 1").fetchone()
    return {"status": "ok", "db": "up"}
