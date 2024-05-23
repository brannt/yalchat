import logging

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from yalchat_server import api, auth_views, db
from yalchat_server.config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)16.16s %(funcName)10.10s %(levelname)7s: " "%(message)s",
    force=True,
)
logger = logging.getLogger("resol")

fastapi_app = FastAPI()

fastapi_app.include_router(api.router, prefix="/api")
fastapi_app.include_router(auth_views.router, prefix="/auth")

fastapi_app.add_event_handler("startup", db.connect_to_db)
fastapi_app.add_event_handler("shutdown", db.close_db_connection)


app = CORSMiddleware(
    fastapi_app,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if config.DEBUG:
    logger.info("API started in DEBUG mode.")

    @fastapi_app.exception_handler(Exception)
    async def debug_exception_handler(request: Request, exc: Exception):
        import traceback

        header = "[DEBUG=TRUE] UNEXPECTED EXCEPTION\n\n"
        traceback_str = "".join(
            traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__)
        )

        return Response(content=header + traceback_str)
