from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat query payload."""

    query: str = Field(min_length=1, description="User question to answer using RAG")


class StructuredAnswer(BaseModel):
    """Structured formatting for nicer UI rendering."""

    summary: str = Field(description="Concise answer suitable for direct display")
    bullets: List[str] = Field(default_factory=list, description="Key bullet points")


class ChatResponse(BaseModel):
    """Standardized chat response from backend."""

    answer: str
    structured: Optional[StructuredAnswer] = None
    sources: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
