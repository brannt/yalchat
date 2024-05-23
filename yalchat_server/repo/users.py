import databases
from yalchat_server import db, types


users = db.schema.users


class UserRepo:
    table = db.schema.users

    def __init__(self, database: databases.Database) -> None:
        self.database = database

    async def setup(self):
        await db.create_table(users)

    async def get_user(self, username: str) -> types.User | None:
        query = users.select().where(users.c.username == username)
        result = await self.database.fetch_one(query=query)
        if not result:
            return None
        return types.User(**result._mapping)

    async def get_password_hash(self, username: str) -> str | None:
        query = users.select().where(users.c.username == username)
        result = await self.database.fetch_one(query=query)
        if not result:
            return None
        return result.password_hash
