import uuid
import databases
import sqlalchemy as sa

from yalchat_server import db, types


chats = db.schema.chats


class ChatRepo:
    def __init__(self, database: databases.Database, user_id: int) -> None:
        self.database = database
        self.user_id = user_id

    async def setup(self):
        await db.create_table(chats)

    async def get_chats(self, offset=0, limit=20) -> list[types.Chat]:
        query = (
            chats.select()
            .order_by(chats.c.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        query = query.where(chats.c.user_id == self.user_id)
        result = await self.database.fetch_all(query=query)
        return [types.Chat.model_validate(dict(row._mapping)) for row in result]

    async def create_chat(
        self, model: str, title: str = "", tags: list[str] | None = None
    ) -> uuid.UUID:
        chat_id = uuid.uuid4()
        query = chats.insert().values(
            id=chat_id,
            title=title,
            tags=tags or [],
            model=model,
            history=[],
            created_at=sa.func.now(),
            user_id=self.user_id,
        )
        await self.database.execute(query=query)
        return chat_id

    async def get_chat(self, chat_id: types.ChatID) -> types.ChatWithHistory | None:
        query = chats.select().where(chats.c.id == chat_id)
        query = query.where(chats.c.user_id == self.user_id)
        result = await self.database.fetch_one(query=query)
        if not result:
            return None
        return types.ChatWithHistory(**result._mapping)

    async def update_chat(self, chat_id: types.ChatID, chat: types.Chat):
        query = chats.update().where(chats.c.id == chat_id)
        query = query.where(chats.c.user_id == self.user_id)
        query = query.values(**chat.model_dump())
        await self.database.execute(query=query)

    async def delete_chat(self, chat_id: types.ChatID):
        query = chats.delete().where(chats.c.id == chat_id)
        query = query.where(chats.c.user_id == self.user_id)
        await self.database.execute(query=query)

    async def add_chat_message(self, chat_id: types.ChatID, message: types.ChatMessage):
        query = chats.update().where(chats.c.id == chat_id)
        query = query.where(chats.c.user_id == self.user_id)
        query = query.values(
            history=db.func.json_append(chats.c.history, message.model_dump())
        )
        await self.database.execute(query=query)
