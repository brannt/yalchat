from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from yalchat_server import deps, services, types
from yalchat_server.config import config
from yalchat_server.types import ChatMessage

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    model: str = config.MODEL
    history: list[ChatMessage] | None = None


class ChatResponse(BaseModel):
    message: str


@router.post("/")
async def chat(
    ch: ChatRequest, current_user: Annotated[types.User, Depends(deps.get_current_user)]
) -> ChatResponse:
    """
    Get a simple chat response without storing the history.
    """
    response = await services.llm.get_chat_answer(ch.model, ch.message, ch.history)
    return ChatResponse(message=response)


@router.post("/stream")
async def simple_stream_chat(ch: ChatRequest):
    """
    Stream a chat response without storing the history.
    """
    return StreamingResponse(
        services.llm.stream_chat_answer(ch.model, ch.message, ch.history),
        media_type="text/plain",
    )
