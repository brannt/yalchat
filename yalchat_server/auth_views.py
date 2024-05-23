from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
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
    password_hash = user_repo.get_password_hash(login_data.username)
    if not auth.validate_password(password_hash, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    if token := auth.get_authenticated_user_token(user_repo, login_data.username):
        auth.set_token_cookie(response, token)
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


@router.get("/telegram/callback")
async def auth_telegram(request: Request, user_repo=Depends(deps.user_repo)):
    telegram_data = dict(request.query_params)
    if not auth.validate_telegram(telegram_data):
        raise HTTPException(status_code=403, detail="Invalid hash")

    if token := auth.get_authenticated_user_token(
        user_repo, request.query_params["username"]
    ):
        response = RedirectResponse(url=config.FRONTEND_URL)
        auth.set_token_cookie(response, token)
        return response

    raise HTTPException(status_code=403, detail="Invalid username")
