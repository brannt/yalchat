import base64
import hashlib
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer  # , OAuth2PasswordRequestForm
from pydantic import BaseModel

from yalchat_server import deps, types
from yalchat_server.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


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


# TODO: Type the user_repo param after implementing a proper user repo
def get_current_user(
    token: Annotated[str, Depends(get_token_cookie)], user_repo=Depends(deps.user_repo)
) -> types.User:
    username = decode_token(token)
    if user := user_repo.get_user(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PasswordRequest(BaseModel):
    username: str
    password: str


def get_authenticated_user_token(user_repo, username: str, password: str) -> str | None:
    password_hash = user_repo.get_password_hash(username)
    if not password_hash:
        return
    in_password_hash = hash_password(password)
    if in_password_hash != password_hash:
        return
    return encode_token(username)


@router.post("/token")
async def login(
    # TODO: Replace with this after installing multipart support
    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_data: PasswordRequest,
    response: Response,
    user_repo=Depends(deps.user_repo),
) -> TokenResponse:
    if token := get_authenticated_user_token(
        user_repo, login_data.username, login_data.password
    ):
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
        return TokenResponse(access_token=token, token_type="bearer")

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password",
    )


@router.post("/logout")
async def logout(response: Response, user: Annotated[types.User, get_current_user]):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=not config.DEBUG,
        samesite="none" if not config.DEBUG else "strict",
    )
