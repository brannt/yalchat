from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "mysecretkey"  # Always set in production!
    DEBUG: bool = False
    MODEL: str = "ollama_chat/phi3"
    SUMMARIZE_MODEL: str = "ollama_chat/phi3"
    OPENAI_API_KEY: str = ""
    DATABASE_URI: str = "sqlite+aiosqlite:///yalchat.db"
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",
    ]


config = Settings(_env_file=".env", _env_file_encoding="utf-8")
