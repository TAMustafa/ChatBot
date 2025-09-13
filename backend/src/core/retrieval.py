from __future__ import annotations

import logging
from typing import List, Tuple

from langchain_pinecone import PineconeVectorStore
from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import get_settings
from core.embedding import EmbeddingClient

logger = logging.getLogger(__name__)


class Retriever:
    """Retriever built on Pinecone vector store using OpenAI embeddings.

    Handles building or connecting to an existing index and performing similarity search.
    """

    def __init__(self) -> None:
        s = get_settings()
        self.namespace = s.PINECONE_NAMESPACE
        self.index_name = s.PINECONE_INDEX
        self.top_k = s.TOP_K
        self.embeddings = EmbeddingClient()
        self.vs = PineconeVectorStore(index_name=self.index_name, embedding=self.embeddings._client)

    async def similarity_search(self, query: str, k: int | None = None) -> List[Document]:
        """Default similarity search."""
        k = k or self.top_k
        return self.vs.similarity_search(query, k=k, namespace=self.namespace)

    async def mmr_search(self, query: str, k: int | None = None, fetch_k: int | None = None, lambda_mult: float = 0.3) -> List[Document]:
        """Max Marginal Relevance search for broader coverage.

        fetch_k controls the initial candidate pool size; we default to 3x k for diversity.
        """
        k = k or self.top_k
        fetch_k = fetch_k or max(k * 5, 20)
        return self.vs.max_marginal_relevance_search(
            query,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult,
            namespace=self.namespace,
        )

    def filtered_search(self, query: str, k: int = 5, filters: dict | None = None) -> List[Document]:
        """Search limited by metadata filters (e.g., same source and page)."""
        return self.vs.similarity_search(query, k=k, namespace=self.namespace, filter=filters or {})

    @staticmethod
    def dedupe_docs(docs: List[Document]) -> List[Document]:
        seen = set()
        out: List[Document] = []
        for d in docs:
            key = (d.metadata.get("source"), d.metadata.get("page"), d.page_content[:200])
            if key in seen:
                continue
            seen.add(key)
            out.append(d)
        return out

    @staticmethod
    def split_documents(docs: List[Document]) -> List[Document]:
        s = get_settings()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=s.CHUNK_SIZE,
            chunk_overlap=s.CHUNK_OVERLAP,
        )
        return splitter.split_documents(docs)

    def add_documents(self, docs: List[Document]) -> Tuple[int, int]:
        """Add documents to the vector store. Returns (chunks, added)."""
        chunks = self.split_documents(docs)
        self.vs.add_documents(chunks, namespace=self.namespace)
        return (len(chunks), len(chunks))
