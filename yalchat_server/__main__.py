import fire


def run(host: str = "0.0.0.0", port: int = 8080, reload: bool = False):
    import uvicorn

    uvicorn.run("yalchat_server.app:app", host=host, port=port, reload=reload)


async def ainit_db():
    from yalchat_server import db, repo

    try:
        database = await db.connect_to_db()
        await repo.ChatRepo(database).setup()
    finally:
        await db.close_db_connection()


def init_db():
    import asyncio

    asyncio.run(ainit_db())


if __name__ == "__main__":
    fire.Fire()
