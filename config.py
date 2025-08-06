from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Config(BaseSettings):
    api_key: str
    api_url: str

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def search_url(self):
        return f"{self.api_url}{self.api_key}/search"


@lru_cache
def get_config() -> Config:
    return Config()
