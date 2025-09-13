from __future__ import annotations

import logging
from functools import lru_cache
from typing import Optional

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure .env is loaded whether API runs from repo root or backend directory
try:
    from dotenv import load_dotenv  # type: ignore
    import os

    HERE = os.path.dirname(os.path.abspath(__file__))
    BACKEND_ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
    REPO_ROOT = os.path.abspath(os.path.join(BACKEND_ROOT, os.pardir))
    # Load repo root first, then backend to allow backend overrides during dev
    load_dotenv(os.path.join(REPO_ROOT, ".env"), override=False)
    load_dotenv(os.path.join(BACKEND_ROOT, ".env"), override=False)
except Exception:
    # Optional dependency; pydantic settings will still look for .env in CWD
    pass


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Uses pydantic settings for typed configuration. Place values in a .env file.
    """

    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore")

    # App
    APP_NAME: str = Field(default="chatbot-backend")
    APP_ENV: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")

    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # Providers
    OPENAI_API_KEY: Optional[str] = None

    # Pinecone
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None  # legacy; optional
    PINECONE_INDEX: str = Field(default="chatbot-faq-index")
    PINECONE_NAMESPACE: str = Field(default="default")

    # Embeddings / LLM
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small")
    CHAT_MODEL: str = Field(default="gpt-4o-mini")
    MAX_TOKENS: int = Field(default=512)
    TEMPERATURE: float = Field(default=0.2)

    # RAG
    TOP_K: int = Field(default=6)
    CHUNK_SIZE: int = Field(default=1000)
    CHUNK_OVERLAP: int = Field(default=150)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        logging.getLogger(__name__).error("Settings validation error: %s", e)
        raise
