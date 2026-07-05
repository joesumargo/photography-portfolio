
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    title: str = "Photography Portfolio"
    debug: bool = False
    photos_data_path: str = "data/photos.yaml"
    photos_base_url: str = "/static/photos"

    model_config = {"env_prefix": "APP_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
