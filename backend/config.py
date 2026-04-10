from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    DATABASE_URL: str = "sqlite+aiosqlite:///agent_team.db"
    AGENT_MODEL: str = "claude-sonnet-4-20250514"

    model_config = {"env_file": ".env"}


settings = Settings()
