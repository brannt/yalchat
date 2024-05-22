from typing import Annotated

from fastapi import Depends, HTTPException, status
from yalchat_server import auth, types
from yalchat_server.repo import ChatRepo, users
from yalchat_server.db import database
# TODO: Type the user_repo param after implementing a proper user repo


def user_repo():
    return users


def get_current_user(
    token: Annotated[str, Depends(auth.get_token_cookie)], user_repo=Depends(user_repo)
) -> types.User:
    username = auth.decode_token(token)
    if user := user_repo.get_user(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )


def chat_repo(
    user: Annotated[types.User, Depends(get_current_user)],
):
    return ChatRepo(database, user.id)
