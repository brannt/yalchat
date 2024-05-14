from databases import Database
import sqlalchemy as sa

from yalchat_server.config import config

database = Database(config.DATABASE_URI)
metadata = sa.MetaData()


def get_dialect():
    match c := config.DATABASE_URI.split(":")[0].split("+")[0]:
        case "sqlite":
            return sa.dialects.sqlite.dialect()
        case "postgresql":
            return sa.dialects.postgresql.dialect()
        case "mysql":
            return sa.dialects.mysql.dialect()
        case _:
            raise ValueError(f"Unknown database dialect: {c}")


dialect = get_dialect()


async def connect_to_db() -> Database:
    await database.connect()
    return database


async def close_db_connection():
    await database.disconnect()


async def create_table(table: sa.Table):
    schema = sa.schema.CreateTable(table, if_not_exists=True)
    query = str(schema.compile(dialect=dialect))
    await database.execute(query=query)
