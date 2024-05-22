import datetime
from io import StringIO
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import StreamingResponse
from openai import BaseModel
from yalchat_server import auth, deps, services, types
from yalchat_server.repo import ChatRepo

router = APIRouter()


class CreateChatRequest(BaseModel):
    model: str
    first_message: str | None = None


class CreateChatResponse(BaseModel):
    chat_id: types.ChatID


class ChatRequest(BaseModel):
    message: str


class StatusResponse(BaseModel):
    status: str


@router.get("/")
async def get_chats(
    chat_repo: Annotated[ChatRepo, Depends(deps.chat_repo)],
    user: Annotated[types.User, Depends(deps.get_current_user)],
) -> list[types.Chat]:
    """
    Get all chat sessions.
    """
    result = await chat_repo.get_chats()
    return result


@router.post("/")
async def create_chat(
    chat_repo: Annotated[ChatRepo, Depends(deps.chat_repo)],
    chat: CreateChatRequest,
    user: Annotated[types.User, Depends(deps.get_current_user)],
) -> types.Chat:
    """
    Start a new chat session.
    """
    now = datetime.datetime.now()

    title = f"Unnamed chat with {chat.model} at {now.isoformat(sep=' ', timespec='seconds')}"
    tags = []
    if chat.first_message:
        title, tags = await services.llm.summarize_title(chat.first_message)

    result = await chat_repo.create_chat(
        model=chat.model,
        title=title,
        tags=tags,
    )
    return types.Chat(
        id=result, model=chat.model, title=title, tags=tags, created_at=now
    )


@router.get("/{chat_id}")
async def get_chat(
    chat_repo: Annotated[ChatRepo, Depends(deps.chat_repo)],
    chat_id: types.ChatID,
    user: Annotated[types.User, Depends(deps.get_current_user)],
) -> types.ChatWithHistory:
    """
    Get a chat session.
    """
    result = await chat_repo.get_chat(chat_id)
    if not result:
        raise HTTPException(status_code=404, detail="Chat not found")
    return result


@router.delete("/{chat_id}", response_model=StatusResponse)
async def delete_chat(
    chat_repo: Annotated[ChatRepo, Depends(deps.chat_repo)],
    chat_id: types.ChatID,
    user: Annotated[types.User, Depends(deps.get_current_user)],
):
    """
    Delete a chat session.
    """
    await chat_repo.delete_chat(chat_id)
    return {"status": "ok"}


@router.post("/{chat_id}/stream")
async def stream_chat(
    chat_repo: Annotated[ChatRepo, Depends(deps.chat_repo)],
    bg_tasks: BackgroundTasks,
    chat_id: types.ChatID,
    ch: ChatRequest,
    user: Annotated[types.User, Depends(deps.get_current_user)],
) -> StreamingResponse:
    """
    Stream a chat response with history.
    """
    # Get chat model and history from the database
    stored_chat = await chat_repo.get_chat(chat_id)
    await chat_repo.add_chat_message(chat_id, types.UserMessage(content=ch.message))
    if not stored_chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    model_response = StringIO()

    async def generate():
        async for chunk in services.llm.stream_chat_answer(
            stored_chat.model, ch.message, stored_chat.history
        ):
            model_response.write(chunk)
            yield chunk

    async def save_response():
        await chat_repo.add_chat_message(
            chat_id,
            types.BotMessage(content=model_response.getvalue()),
        )

    bg_tasks.add_task(save_response)

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )
