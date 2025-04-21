from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str | None = "text-embedding-3-large"
    OPENAI_CHAT_MODEL: str | None = "gpt-4o"
    DB_PATH: str = "vectors.db"

    class Config:
        env_file = ".env"


settings = Settings()
