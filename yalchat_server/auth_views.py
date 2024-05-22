from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer  # , OAuth2PasswordRequestForm
from pydantic import BaseModel

from yalchat_server import auth, deps, types
from yalchat_server.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


TokenData = str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PasswordRequest(BaseModel):
    username: str
    password: str


@router.post("/token")
async def login(
    # TODO: Replace with this after installing multipart support
    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_data: PasswordRequest,
    response: Response,
    user_repo=Depends(deps.user_repo),
) -> TokenResponse:
    if token := auth.get_authenticated_user_token(
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
async def logout(
    response: Response, user: Annotated[types.User, deps.get_current_user]
):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=not config.DEBUG,
        samesite="none" if not config.DEBUG else "strict",
    )
