from __future__ import annotations

from typing import List

from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """
You are a helpful support assistant. Answer the user's question using the provided context from the FAQ knowledge base. 
- If the answer is not in the context, say you don't know and suggest contacting support.
- Be concise and factual.
- When the question requests requirements, rules, or lists, provide an EXHAUSTIVE list from the context. Do not omit items that appear in other context snippets.
- If page numbers are present in the context, include the page number next to the relevant item like (p.X).
- Cite sources by their titles or file names when available.
""".strip()


def build_rag_prompt(context_chunks: List[str], question: str) -> ChatPromptTemplate:
    """Construct a chat prompt with context and user question."""
    context_text = "\n\n".join(context_chunks)
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Use the following context to answer the question. Merge information across all snippets. If the question implies a list, enumerate ALL items found.\n\nContext:\n{context}\n\nQuestion: {question}",
            ),
        ]
    ).partial(context=context_text, question=question)
