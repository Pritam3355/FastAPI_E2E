# from pydantic_settings import BaseSettings
# import os
# from typing import List

# class Settings(BaseSettings):
#     DATABASE_URL: str = (
#         f"postgresql+psycopg2://{os.getenv('POSTGRESQL_USER')}:"
#         f"{os.getenv('POSTGRESQL_PASSWORD')}@"
#         f"{os.getenv('POSTGRESQL_SERVER', 'localhost')}:{os.getenv('POSTGRESQL_PORT',5432)}/"
#         f"{os.getenv('POSTGRESQL_DB')}"
#     )
#     BACKEND_CORS_ORIGINS: List[str] = [] # used in main.py
#     class Config:
#         env_file = ".env"

# settings = Settings()


from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os

class Settings(BaseSettings):
    DATABASE_URL: str = (
        f"postgresql+psycopg2://{os.getenv('POSTGRESQL_USER')}:"
        f"{os.getenv('POSTGRESQL_PASSWORD')}@"
        f"{os.getenv('POSTGRESQL_SERVER', 'localhost')}:{os.getenv('POSTGRESQL_PORT',5432)}/"
        f"{os.getenv('POSTGRESQL_DB')}"
    )
    
    BACKEND_CORS_ORIGINS: Union[List[str], str] = []
    
    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str) and v:
            # Split comma-separated string into list
            return [origin.strip() for origin in v.split(',')]
        return v or []
    
    class Config:
        env_file = ".env"

settings = Settings()