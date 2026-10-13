from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from psycopg import Connection

from app.entity.user import User
from app.repository.note_repository import NoteRepository
from app.repository.user_repository import UserRepository
from app.service.auth_service import AuthService
from app.service.note_service import NoteService
from app.util.database import get_conn
from app.util.exceptions import AuthenticationError

# auto_error=False: a missing header reaches get_current_user, which answers with our own 401.
bearer_scheme = HTTPBearer(auto_error=False)


def get_note_repository(conn: Connection = Depends(get_conn)) -> NoteRepository:
    return NoteRepository(conn)


def get_note_service(repository: NoteRepository = Depends(get_note_repository)) -> NoteService:
    return NoteService(repository)


def get_user_repository(conn: Connection = Depends(get_conn)) -> UserRepository:
    return UserRepository(conn)


def get_auth_service(repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    if credentials is None:
        raise AuthenticationError("Not authenticated")
    return service.user_from_token(credentials.credentials)
