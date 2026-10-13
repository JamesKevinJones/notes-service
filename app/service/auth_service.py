from app.dto.user_dto import CredentialsRequest
from app.entity.user import User
from app.repository.user_repository import UserRepository
from app.util.exceptions import AuthenticationError, EmailTakenError
from app.util.security import create_access_token, decode_access_token, hash_password, verify_password


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, request: CredentialsRequest) -> User:
        email = request.email.strip().lower()
        user = self.repository.insert(email, hash_password(request.password))
        if user is None:
            raise EmailTakenError(email)
        return user

    def login(self, request: CredentialsRequest) -> str:
        user = self.repository.find_by_email(request.email.strip().lower())
        # One message for both cases, so login can't be used to probe which emails exist.
        if user is None or not verify_password(request.password, user.password_hash):
            raise AuthenticationError("Incorrect email or password")
        return create_access_token(user.id)

    def user_from_token(self, token: str) -> User:
        user_id = decode_access_token(token)
        # Look the user up too: a valid signature for a since-deleted user is still a reject.
        user = self.repository.find_by_id(user_id) if user_id is not None else None
        if user is None:
            raise AuthenticationError("Invalid or expired token")
        return user
