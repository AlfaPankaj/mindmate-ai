import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
env_path = os.path.join(project_root, ".env")

class Settings(BaseSettings):
    NVIDIA_API_KEY: Optional[str] = None
    MODEL_NAME: str = "meta/llama-3.3-70b-instruct"
    MONGODB_URI: str = "mongodb://localhost:27017/mindmate"
    
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "MindMate-AI"
    
    SECRET_KEY: str = "supersecret"
    ENVIRONMENT: str = "development"
    
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
