from databases import Database
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from yalchat_server.config import config

database = Database(config.DATABASE_URI)
dialect_name = config.DATABASE_URI.split(":")[0].split("+")[0]
metadata = sa.MetaData()


def get_dialect():
    match dialect_name:
        case "sqlite":
            return sa.dialects.sqlite.dialect()
        case "postgresql":
            return sa.dialects.postgresql.dialect()
        case _:
            raise ValueError(f"Unsupported database dialect: {dialect_name}")


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


class SQLiteFunc:
    @staticmethod
    def uuid():
        return sa.func.uuid()

    @staticmethod
    def json_append(column, value):
        return sa.func.json_insert(column, "$", sa.func.json(value))

    @staticmethod
    def empty_json_array():
        return sa.func.json("[]")

    @staticmethod
    def json_array_column(column_name, **kwargs):
        return sa.Column(
            column_name,
            sa.JSON,
            server_default="[]",
            nullable=False,
            default=[],
            **kwargs,
        )


class PostgreSQLFunc:
    @staticmethod
    def uuid():
        return sa.func.gen_random_uuid()

    @staticmethod
    def json_append(column, value):
        return column.op("||")(sa.cast(value, JSONB))

    @staticmethod
    def empty_json_array():
        return sa.func.jsonb("[]")

    @staticmethod
    def json_array_column(column_name, **kwargs):
        return sa.Column(
            column_name,
            JSONB,
            server_default=sa.func.jsonb("[]"),
            nullable=False,
            default=[],
            **kwargs,
        )


def get_dialect_func():
    match dialect_name:
        case "sqlite":
            return SQLiteFunc()
        case "postgresql":
            return PostgreSQLFunc()
        case _:
            raise ValueError(f"Unsupported database dialect: {dialect_name}")


func = get_dialect_func()
