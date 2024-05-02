from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from yalchat_server import services
from yalchat_server.config import config
from yalchat_server.types import ChatMessage

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    model: str = config.MODEL
    history: list[ChatMessage] | None = None


class ChatResponse(BaseModel):
    message: str


@router.post("/chat")
async def chat(ch: ChatRequest) -> ChatResponse:
    response = await services.chat.get_chat_answer(ch.model, ch.query, ch.history)
    return ChatResponse(message=response)


@router.post("/stream_chat")
async def stream_chat(ch: ChatRequest):
    return StreamingResponse(
        services.chat.stream_chat_answer(ch.model, ch.query, ch.history),
        media_type="text/plain",
    )
