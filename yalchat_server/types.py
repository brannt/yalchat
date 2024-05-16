import datetime
import json
from typing import Any
import uuid
from pydantic import BaseModel, TypeAdapter, field_validator


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


def parse_to_json(value: str | Any) -> Any:
    return json.loads(value) if isinstance(value, str) else value


class Chat(BaseModel):
    id: ChatID
    title: str
    tags: list[str] | None = None
    model: str
    created_at: datetime.datetime

    _parse_tags = field_validator("tags", mode="before")(parse_to_json)


class ChatWithHistory(Chat):
    history: list[ChatMessage] = []

    _parse_history = field_validator("history", mode="before")(parse_to_json)
