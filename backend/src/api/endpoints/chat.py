from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from schemas.chat import ChatRequest, ChatResponse
from core.rag import RAGPipeline

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse, summary="Chat with RAG")
async def chat(req: ChatRequest) -> ChatResponse:
    """Main chat endpoint performing RAG and returning structured response."""
    try:
        pipeline = RAGPipeline()
        result = await pipeline.answer(query=req.query)
        return ChatResponse(**result)
    except Exception as e:  # noqa: BLE001
        logger.exception("/chat failed: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
