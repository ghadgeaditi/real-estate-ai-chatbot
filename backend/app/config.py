from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_model: str = "openrouter/free"
    app_name: str = "PropertyLens AI"
    data_file: str = "backend/data/properties.json"
    allowed_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
