from fastapi import APIRouter
from yalchat_server import deps, types

router = APIRouter()


@router.get("/me")
async def get_current_user(
    current_user: deps.AuthenticatedUserDep,
) -> types.User:
    return current_user
