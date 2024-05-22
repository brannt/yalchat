from yalchat_server.repo import ChatRepo, users
from yalchat_server.db import database


def chat_repo():
    return ChatRepo(database)


def user_repo():
    return users
