import base64
import datetime
import hashlib
import hmac
from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from yalchat_server.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
TokenData = dict


def encode_token(token_data: TokenData, expires_in: int | None = None) -> str:
    expires_in = expires_in or config.JWT_EXPIRATION
    expire_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=expires_in
    )
    to_encode = {"exp": expire_time, **token_data}
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )
        if "sub" not in payload:
            raise jwt.InvalidTokenError
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


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


async def get_authenticated_user_token(user_repo, username: str) -> str | None:
    if await user_repo.get_user(username):
        return encode_token({"sub": username})
    return None


def set_token_cookie(response, token):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        # Use secure cookies in production
        secure=not config.DEBUG,
        # Use samesite="strict" in development
        # because the frontend and backend run on different ports
        # and we cannot use samesite="none" without HTTPS
        samesite="none" if not config.DEBUG else "strict",
        max_age=60 * 60 * 24,
    )


def validate_password(password_hash: str | None, check_password: str) -> bool:
    return bool(password_hash and hash_password(check_password) != password_hash)


def validate_telegram(tg_data: dict) -> bool:
    hash = tg_data.pop("hash")
    secret_key = hashlib.sha256(config.TELEGRAM_BOT_TOKEN.encode()).digest()
    data_check_string = "\n".join(
        [f"{key}={value}" for key, value in sorted(tg_data.items())]
    )
    check_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return check_hash == hash
