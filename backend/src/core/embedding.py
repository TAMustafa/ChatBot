from __future__ import annotations

from typing import List

from langchain_openai import OpenAIEmbeddings

from config.settings import get_settings


class EmbeddingClient:
    """Wrapper around OpenAI embeddings with sensible defaults.

    NOTE: This class can be adapted to support other providers by matching the interface.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self._client = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # The OpenAIEmbeddings in LangChain is sync; call in thread executor if needed.
        return self._client.embed_documents(texts)

    async def embed_query(self, text: str) -> List[float]:
        return self._client.embed_query(text)
