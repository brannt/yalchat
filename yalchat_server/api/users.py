from typing import Annotated
from fastapi import APIRouter, Depends
from yalchat_server import deps, types

router = APIRouter()


@router.get("/me")
async def get_current_user(
    current_user: Annotated[types.User, Depends(deps.get_current_user)],
) -> types.User:
    return current_user
