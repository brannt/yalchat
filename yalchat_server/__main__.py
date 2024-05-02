import logging

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

from yalchat_server import api
from yalchat_server.config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)16.16s %(funcName)10.10s %(levelname)7s: " "%(message)s",
    force=True,
)
logger = logging.getLogger("resol")

app = FastAPI()

# app.mount("/static", StaticFiles(directory="yalchat_server/static"), name="static")
app.include_router(api.router, prefix="/api")

origins = [
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if config.DEBUG:
    logger.info("API started in DEBUG mode.")

    @app.exception_handler(Exception)
    async def debug_exception_handler(request: Request, exc: Exception):
        import traceback

        header = "[DEBUG=TRUE] UNEXPECTED EXCEPTION\n\n"
        traceback_str = "".join(
            traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__)
        )

        return Response(content=header + traceback_str)
