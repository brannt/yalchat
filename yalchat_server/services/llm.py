from typing import AsyncGenerator, Type, TypeVar
from litellm import acompletion
from litellm.utils import ModelResponse
from pydantic import BaseModel
from yalchat_server.types import ChatMessage
from yalchat_server.config import config


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


SUMMARIZE_SYSTEM_PROMPT = """
Return a fitting title and tags for a conversation between a user and an AI assistant that starts with the provided user message.
The title should be a short concise summary of the conversation, and the tags should be a list of broad categories assigned to this conversation
in a conversation management system. Use JSON format as in the example below.
```
{
    "title": "string",
    "tags": ["string"]
}
```
Do not add any additional information to the output, return just ONE SINGLE JSON object. Do not include the user message in the output.
Do not return more than one object in the output. The input should be a single JSON object that can be parsed into a dictionary.
"""


class SummarizeOutput(BaseModel):
    title: str
    tags: list[str]


async def summarize_title(
    message, model: str | None = None, retries=5
) -> tuple[str, list[str]]:
    model = model or config.SUMMARIZE_MODEL
    messages = [
        {"content": SUMMARIZE_SYSTEM_PROMPT, "role": "system"},
        {"content": f"Here is the initial message: \n{message}", "role": "user"},
    ]
    last_exception = None
    for _ in range(retries):
        result = await acompletion(model=model, messages=messages, temperature=0)

        response_message = result.choices[0]["message"]
        try:
            output = parse_json_output(response_message["content"], SummarizeOutput)
            return output.title, output.tags
        except Exception as e:
            error_message = {
                "content": f"I got and error while parsing your last output, please provide a corrected JSON object. Error: {e}",
                "role": "user",
            }
            last_exception = e

            messages.extend(
                [
                    response_message,
                    error_message,
                ]
            )

    raise last_exception


M = TypeVar("M", bound=BaseModel)


def parse_json_output(output: str, schema: Type[M]) -> M:
    """
    Extract and clean the JSON output from the model response and parse it into the provided schema.
    """
    output_lines = output.split("\n")

    def _iter():
        json_found = False
        for line in output_lines:
            if line.startswith("{"):
                json_found = True
            if json_found:
                yield line
            if line.startswith("}"):
                break

    json_output = "\n".join(_iter())
    return schema.model_validate_json(json_output)
