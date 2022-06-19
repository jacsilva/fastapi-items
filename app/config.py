from pydantic import BaseSettings
from functools import lru_cache
from fastapi import Depends

class Settings(BaseSettings):
    app_name: str
    admin_email: str
    database_string: str 
    postgres_user: str
    # items_per_user: int = 50

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    
@lru_cache()
def get_settings():
    return Settings()

    