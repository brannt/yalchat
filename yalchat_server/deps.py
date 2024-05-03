from yalchat_server.repo import ChatRepo
from yalchat_server.db import database


def chat_repo():
    return ChatRepo(database)
