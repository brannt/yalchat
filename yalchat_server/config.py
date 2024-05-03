from pydantic import BaseModel


class PydanticSettings(BaseModel):
    DEBUG: bool = False
    MODEL: str = "ollama_chat/phi3"
    SUMMARIZE_MODEL: str = "ollama_chat/phi3"
    OPENAI_API_KEY: str = ""
    DATABASE_URI: str = "sqlite+aiosqlite:///yalchat.db"


config = PydanticSettings()
