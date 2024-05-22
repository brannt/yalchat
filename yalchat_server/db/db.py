from databases import Database
import sqlalchemy as sa
from yalchat_server.config import config

from .dialects import dialect

database = Database(config.DATABASE_URI)
metadata = sa.MetaData()


async def connect_to_db() -> Database:
    await database.connect()
    return database


async def close_db_connection():
    await database.disconnect()


async def create_table(table: sa.Table):
    schema = sa.schema.CreateTable(table, if_not_exists=True)
    query = str(schema.compile(dialect=dialect))
    await database.execute(query=query)
