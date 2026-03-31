from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/agent_team"
    AGENT_MODEL: str = "claude-sonnet-4-20250514"

    model_config = {"env_file": ".env"}


settings = Settings()
