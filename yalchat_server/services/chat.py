from typing import AsyncGenerator
from litellm import acompletion
from litellm.utils import ModelResponse, CustomStreamWrapper
from yalchat_server.types import ChatMessage


async def get_chat_answer(
    model: str, message: str, history: list[ChatMessage] | None = None
) -> str:
    messages = [message.model_dump() for message in history] if history else []
    messages.append({"content": message, "role": "user"})
    response = await acompletion(model=model, messages=messages)
    assert isinstance(response, ModelResponse)
    return response.choices[0]["message"]["content"]


async def stream_chat_answer(
    model: str, message: str, history: list[ChatMessage] | None = None
) -> AsyncGenerator[str, None]:
    messages = [message.model_dump() for message in history] if history else []
    messages.append({"content": message, "role": "user"})
    response = await acompletion(model=model, messages=messages, stream=True)
    async for chunk in response:  # type: ignore
        if content := chunk.choices[0]["delta"]["content"]:
            yield content
