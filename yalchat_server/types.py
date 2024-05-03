import datetime
import uuid
from pydantic import BaseModel, TypeAdapter


class ChatMessage(BaseModel):
    content: str
    role: str


class UserMessage(ChatMessage):
    role: str = "user"


class BotMessage(ChatMessage):
    role: str = "assistant"


class SystemMessage(ChatMessage):
    role: str = "system"


ChatMessageList = TypeAdapter(list[ChatMessage])

ChatID = uuid.UUID


class Chat(BaseModel):
    id: ChatID
    title: str
    tags: list[str] | None = None
    model: str
    created_at: datetime.datetime


class ChatWithHistory(Chat):
    history: list[ChatMessage] = []
