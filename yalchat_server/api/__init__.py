from . import simple_chat, chats, users

from fastapi import APIRouter


router = APIRouter()
router.include_router(chats.router, prefix="/chats")
router.include_router(simple_chat.router, prefix="/simple_chat")
router.include_router(users.router, prefix="/users")
