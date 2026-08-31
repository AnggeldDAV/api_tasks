from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    DATABASE_URL: str 
    JWT_SECRET: str 
    ALGORITHM: str 
    
    
    model_config = SettingsConfigDict(env_file="../.env", 
                                      env_file_encoding="utf-8", 
                                      extra="ignore", 
                                      env_ignore_empty=True )

@lru_cache        
def get_settings():
    return Settings()
        