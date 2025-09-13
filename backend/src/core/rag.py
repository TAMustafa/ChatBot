from __future__ import annotations

import logging
from typing import Dict, List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.docstore.document import Document

from config.settings import get_settings
from core.llm_client import LLMClient
from core.prompt import build_rag_prompt
from core.retrieval import Retriever
from schemas.chat import StructuredAnswer

logger = logging.getLogger(__name__)


class RAGPipeline:
    """End-to-end retrieval augmented generation pipeline."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.retriever = Retriever()
        self.llm = LLMClient().get()

    async def _retrieve(self, query: str) -> List[Document]:
        """Retrieve diverse, relevant chunks using MMR for better coverage."""
        return await self.retriever.mmr_search(query, k=self.settings.TOP_K)

    async def answer(self, query: str) -> Dict[str, object]:
        """Run retrieval, construct prompt, query LLM, and return structured response."""
        docs = await self._retrieve(query)
        if not docs:
            return {
                "answer": "I couldn't find an answer in the knowledge base. Please contact support.",
                "sources": [],
                "confidence": 0.0,
            }

        # Augment context with additional chunks from the same source/page to capture full lists
        try:
            augmented: List[Document] = list(docs)
            seen_keys = {(d.metadata.get("source"), d.metadata.get("page")) for d in docs}
            for d in list(docs)[: self.settings.TOP_K]:
                src = d.metadata.get("source")
                page = d.metadata.get("page")
                if not src or page is None:
                    continue
                # Fetch a couple of extra chunks from the same page regardless of similarity to avoid truncation
                extras = self.retriever.filtered_search(query, k=3, filters={"source": src, "page": page})
                augmented.extend(extras)
            # Dedupe
            from core.retrieval import Retriever as _R

            docs = _R.dedupe_docs(augmented)
        except Exception:
            # Fallback silently if vector store doesn't support filter or any error occurs
            pass

        chunks = [d.page_content for d in docs]
        def _fmt_source(d: Document) -> str:
            src = d.metadata.get("source", "unknown")
            page = d.metadata.get("page")
            if isinstance(page, int):
                return f"{src} (p.{page})"
            return str(src)

        sources = [_fmt_source(d) for d in docs]

        prompt = build_rag_prompt(chunks, query)

        # Free-text answer
        free_text_chain = prompt | self.llm | StrOutputParser()
        result = await free_text_chain.ainvoke({})

        # Structured summary + bullets using Pydantic structured output
        try:
            structured_llm = self.llm.with_structured_output(StructuredAnswer)  # type: ignore[attr-defined]
            structured_obj: StructuredAnswer = await (prompt | structured_llm).ainvoke({})
        except Exception:
            structured_obj = self._build_structured(result.strip()) or None  # fallback to heuristic

        # Naive confidence based on number of documents retrieved; can be replaced.
        confidence = min(1.0, 0.5 + 0.05 * len(docs))

        answer_text = result.strip()
        # Prefer the model-generated structured output, fallback already applied above
        structured = structured_obj if isinstance(structured_obj, StructuredAnswer) else self._build_structured(answer_text)

        return {
            "answer": answer_text,
            "structured": structured.model_dump() if structured else None,
            "sources": list(dict.fromkeys(sources)),
            "confidence": confidence,
        }

    @staticmethod
    def _build_structured(answer: str) -> StructuredAnswer | None:
        """Create a structured view (summary + bullets) from free text.

        Heuristics handled:
        - Numbered lists like `1. item`, `2) item` extracted as bullets.
        - Hyphen/• lists extracted as bullets.
        - Summary is the preamble (text before the list) or the first sentence.
        - Numeric-only bullets are dropped (e.g., stray "1", "2").
        """
        import re

        text = answer.strip()
        if not text:
            return None

        # First try to detect numbered list items
        numbered_pattern = re.compile(r"(?:^|[\n\r\s])(?:\d+)[\.)]\s+([^\n\r]+)")
        numbered = [m.group(1).strip() for m in numbered_pattern.finditer(text)]

        bullets: List[str] = []

        if numbered:
            bullets = numbered
        else:
            # Fallback: lines with '-' or '•'
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            for l in lines:
                if l.startswith("-") or l.startswith("•"):
                    bullets.append(l.lstrip("-• ").strip())

        # Compute summary
        summary: str
        if bullets:
            # Summary is the first sentence before the first bullet marker
            first_match = numbered_pattern.search(text)
            preamble = text[: first_match.start()] if first_match else text
            # naive sentence split
            first_sentence = re.split(r"(?<=[.!?])\s+", preamble.strip())
            summary = (first_sentence[0] if first_sentence and first_sentence[0] else preamble.strip()).rstrip(".")
        else:
            # No bullets found; split sentences and use the rest as bullets
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if s.strip()]
            if not sentences:
                return StructuredAnswer(summary=text, bullets=[])
            summary = sentences[0].rstrip(".")
            bullets = [s.rstrip(".") for s in sentences[1:]]

        # Clean bullets: drop numeric-only, trim, dedupe, cap
        cleaned: List[str] = []
        seen = set()
        for b in bullets:
            b2 = b.strip().strip("-• ")
            if not b2 or re.fullmatch(r"\d+[.)]?", b2):
                continue
            if b2 not in seen:
                cleaned.append(b2)
                seen.add(b2)

        return StructuredAnswer(summary=summary, bullets=cleaned[:8])
