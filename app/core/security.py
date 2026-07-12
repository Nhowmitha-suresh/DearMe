import hashlib
import os
import hmac
from datetime import datetime, timedelta
import jwt
from typing import Optional

from app.core.config import settings

# We will use hashlib's pbkdf2_hmac as it is built-in and secure on all platforms
SALT_SIZE = 16
ITERATIONS = 100000
ALGORITHM = "HS256"
DEFAULT_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days session default


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        ITERATIONS
    )
    return f"{salt.hex()}${pwd_hash.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        parts = hashed_password.split('$')
        if len(parts) != 2:
            return False
        salt = bytes.fromhex(parts[0])
        original_hash = bytes.fromhex(parts[1])
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            ITERATIONS
        )
        return hmac.compare_digest(original_hash, new_hash)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=DEFAULT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.PyJWTError:
        return None
