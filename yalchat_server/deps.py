from typing import Annotated

from fastapi import Depends, HTTPException, status
from yalchat_server import auth, types
from yalchat_server import repo
from yalchat_server.db import database


def user_repo() -> repo.UserRepo:
    return repo.UserRepo(database)


UserRepoDep = Annotated[repo.UserRepo, Depends(user_repo)]


async def get_current_user(
    token: Annotated[str, Depends(auth.get_token_cookie)],
    user_repo: UserRepoDep,
) -> types.User:
    username = auth.decode_token(token)["sub"]
    if user := await user_repo.get_user(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )


AuthenticatedUserDep = Annotated[types.User, Depends(get_current_user)]


def chat_repo(
    user: AuthenticatedUserDep,
) -> repo.ChatRepo:
    return repo.ChatRepo(database, user.id)


ChatRepoDep = Annotated[repo.ChatRepo, Depends(chat_repo)]
