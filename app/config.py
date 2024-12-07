from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    title: str = "BigBurger"
    version: str = "v0.2.0"
    description: str = "API REST for diner management."
    
    db_url: str
    

@lru_cache
def get_settings():
    return Settings()
    