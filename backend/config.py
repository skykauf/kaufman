from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings - SQLite for local development
    database_url: str = "sqlite:///./recipes.db"

    # Application settings
    debug: bool = False
    environment: str = "production"

    # API settings
    api_title: str = "Mimi's Recipe API"
    api_version: str = "1.0.0"

    # CORS settings
    allowed_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()
