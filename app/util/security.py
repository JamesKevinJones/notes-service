import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.environ["JWT_SECRET"]
if len(JWT_SECRET) < 32:
    # A short or placeholder secret lets anyone forge a token for any user.
    raise RuntimeError("JWT_SECRET must be at least 32 characters; see .env.example")
JWT_ALGORITHM = "HS256"
TOKEN_TTL = timedelta(minutes=60)

# scrypt cost settings from the OWASP password storage cheat sheet.
SCRYPT_N, SCRYPT_R, SCRYPT_P = 2**14, 8, 1


def _scrypt(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode(), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    return f"scrypt${salt.hex()}${_scrypt(password, salt).hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    _, salt_hex, digest_hex = stored_hash.split("$")
    return hmac.compare_digest(_scrypt(password, bytes.fromhex(salt_hex)), bytes.fromhex(digest_hex))


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    claims = {"sub": str(user_id), "iat": now, "exp": now + TOKEN_TTL}
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """The user id inside a valid, unexpired token, else None."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None
