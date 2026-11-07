"""Authentication: bcrypt password checks and JWT access tokens."""
import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

# --- Required secrets: refuse to start without them (no guessable fallbacks) ---
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise RuntimeError("SECRET_KEY must be set in .env and be at least 32 characters")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_HASH = os.getenv("ADMIN_HASH")
if not ADMIN_HASH:
    raise RuntimeError("ADMIN_HASH must be set in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Used so a wrong username takes as long to reject as a wrong password,
# which stops attackers from discovering valid usernames by timing responses.
_DUMMY_HASH = bcrypt.hashpw(b"not-a-real-password", bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except ValueError:
        return False


def authenticate_user(username: str, password: str):
    username_ok = secrets.compare_digest(username.encode(), ADMIN_USERNAME.encode())
    password_ok = verify_password(password, ADMIN_HASH if username_ok else _DUMMY_HASH)
    if username_ok and password_ok:
        return {"username": username}
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # algorithms is pinned so a token signed with a different algorithm is rejected
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:  # covers bad signatures and expired tokens
        raise credentials_exception
    username = payload.get("sub")
    if not username:
        raise credentials_exception
    return {"username": username}
