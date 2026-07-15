from typing import List,Any
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX:str='/api'
    ALLOWED_ORIGINS:Any=[]
    DEBUG:bool=False
    DATABASE_URL:str
    API_KEY:str=""

    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def assemble_allowed_origins(cls, v) -> List[str]:
        if isinstance(v, str):
            # Strips whitespaces and filters out empty items
            return [item.strip() for item in v.split(',') if item.strip()]
        return v or []
    
    class Config:
        env_file='.env'
        env_file_encoding='utf-8'
        case_sensitive=True

settings=Settings()
