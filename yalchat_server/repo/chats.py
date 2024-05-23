import uuid
import databases
import sqlalchemy as sa

from yalchat_server import db, types


class ChatRepo:
    table = db.schema.chats

    def __init__(self, database: databases.Database, user_id: int) -> None:
        self.database = database
        self.user_id = user_id

    async def setup(self):
        await db.create_table(self.table)

    async def get_chats(self, offset=0, limit=20) -> list[types.Chat]:
        query = (
            self.table.select()
            .order_by(self.table.c.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        query = query.where(self.table.c.user_id == self.user_id)
        result = await self.database.fetch_all(query=query)
        return [types.Chat.model_validate(dict(row._mapping)) for row in result]

    async def create_chat(
        self, model: str, title: str = "", tags: list[str] | None = None
    ) -> uuid.UUID:
        chat_id = uuid.uuid4()
        query = self.table.insert().values(
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
        query = self.table.select().where(self.table.c.id == chat_id)
        query = query.where(self.table.c.user_id == self.user_id)
        result = await self.database.fetch_one(query=query)
        if not result:
            return None
        return types.ChatWithHistory(**result._mapping)

    async def update_chat(self, chat_id: types.ChatID, chat: types.Chat):
        query = self.table.update().where(self.table.c.id == chat_id)
        query = query.where(self.table.c.user_id == self.user_id)
        query = query.values(**chat.model_dump())
        await self.database.execute(query=query)

    async def delete_chat(self, chat_id: types.ChatID):
        query = self.table.delete().where(self.table.c.id == chat_id)
        query = query.where(self.table.c.user_id == self.user_id)
        await self.database.execute(query=query)

    async def add_chat_message(self, chat_id: types.ChatID, message: types.ChatMessage):
        query = self.table.update().where(self.table.c.id == chat_id)
        query = query.where(self.table.c.user_id == self.user_id)
        query = query.values(
            history=db.func.json_append(self.table.c.history, message.model_dump())
        )
        await self.database.execute(query=query)
