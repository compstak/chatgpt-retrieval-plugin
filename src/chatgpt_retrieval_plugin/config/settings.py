from functools import lru_cache
from typing import Optional
from uuid import uuid4

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    PROJECT_NAME: str = "Retrieval Plugin API"

    MILVUS_COLLECTION: str = "c" + uuid4().hex
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530
    MILVUS_USER: Optional[str] = None
    MILVUS_PASSWORD: Optional[str] = None
    MILVUS_USE_SECURITY: bool = False

    MILVUS_INDEX_PARAMS: Optional[str] = None
    MILVUS_SEARCH_PARAMS: Optional[str] = None
    MILVUS_CONSISTENCY_LEVEL: str = "Bounded"

    UPSERT_BATCH_SIZE: int = 100
    OUTPUT_DIM: int = 1536
    EMBEDDING_FIELD: str = "embedding"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
