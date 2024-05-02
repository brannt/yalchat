from pydantic import BaseModel


class PydanticSettings(BaseModel):
    DEBUG: bool = False
    MODEL: str = "ollama_chat/phi3"
    OPENAI_API_KEY: str = ""


config = PydanticSettings()
