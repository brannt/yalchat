import base64
import hashlib
from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer  # , OAuth2PasswordRequestForm

from yalchat_server.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


TokenData = str


# TODO: Replace with JWT
def encode_token(token_data: TokenData) -> str:
    return base64.urlsafe_b64encode(token_data.encode()).decode()


def decode_token(token: str) -> TokenData:
    return base64.urlsafe_b64decode(token).decode()


def hash_password(password: str) -> str:
    # TODO: Replace with BCrypt
    salted_password_bytes = (password + config.SECRET_KEY).encode()
    return hashlib.sha256(salted_password_bytes).hexdigest()


def get_token_cookie(request: Request) -> str:
    if token := request.cookies.get("access_token"):
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


def get_authenticated_user_token(user_repo, username: str, password: str) -> str | None:
    password_hash = user_repo.get_password_hash(username)
    if not password_hash:
        return
    in_password_hash = hash_password(password)
    if in_password_hash != password_hash:
        return
    return encode_token(username)
