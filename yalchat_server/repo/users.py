from yalchat_server import types

USERS = {
    "brannt": {
        "id": 1,
        "username": "localuser",
        "email": "",
        # Hashed empty string
        "password_hash": "2afe16a6d630d94cd07c68d5e35568655bf5f60bef29c4f1321fc857816afec9",
    }
}


def get_user(username: str) -> types.User | None:
    if user := USERS.get(username):
        return types.User(**user)


def get_password_hash(username: str) -> str | None:
    if user := USERS.get(username):
        return user["password_hash"]
