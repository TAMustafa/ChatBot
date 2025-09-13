from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from config.settings import get_settings


class LLMClient:
    """Factory for chat LLM."""

    def __init__(self) -> None:
        s = get_settings()
        self.llm = ChatOpenAI(model=s.CHAT_MODEL, temperature=s.TEMPERATURE, max_tokens=s.MAX_TOKENS)

    def get(self) -> ChatOpenAI:
        return self.llm
