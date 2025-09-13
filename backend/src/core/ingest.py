from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable, List

from langchain_community.docstore.document import Document

from core.retrieval import Retriever

logger = logging.getLogger(__name__)


def _doc(source: str, text: str, metadata: dict | None = None) -> Document:
    md = {"source": source}
    if metadata:
        md.update(metadata)
    return Document(page_content=text, metadata=md)


def load_markdown(path: Path) -> List[Document]:
    text = path.read_text(encoding="utf-8")
    return [_doc(source=str(path.name), text=text)]


def load_pdf(path: Path) -> List[Document]:
    try:
        from pypdf import PdfReader
    except Exception as e:  # noqa: BLE001
        raise RuntimeError("pypdf is required to load PDFs") from e

    reader = PdfReader(str(path))
    docs: List[Document] = []
    for i, page in enumerate(reader.pages):
        content = page.extract_text() or ""
        if content.strip():
            docs.append(_doc(source=str(path.name), text=content, metadata={"page": i + 1}))
    return docs


def load_json_faq(path: Path) -> List[Document]:
    """Load a JSON FAQ file. Expected schema examples:
    - {"faqs": [{"question": str, "answer": str, "source": Optional[str]}]}
    - or a list: [{"q": str, "a": str}]
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    items: Iterable[dict]
    if isinstance(data, dict) and "faqs" in data:
        items = data["faqs"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("Unsupported JSON FAQ schema")

    docs: List[Document] = []
    for it in items:
        q = it.get("question") or it.get("q")
        a = it.get("answer") or it.get("a")
        if not q or not a:
            continue
        text = f"Q: {q}\nA: {a}"
        src = it.get("source") or path.name
        docs.append(_doc(source=str(src), text=text))
    return docs


def ingest_paths(paths: List[Path]) -> dict:
    """Ingest one or more files into the vector store.

    Supports .md/.markdown, .pdf, .json FAQ schema.
    Returns a summary with counts.
    """
    retriever = Retriever()
    loaded: List[Document] = []
    for p in paths:
        suffix = p.suffix.lower()
        if suffix in {".md", ".markdown"}:
            loaded.extend(load_markdown(p))
        elif suffix == ".pdf":
            loaded.extend(load_pdf(p))
        elif suffix == ".json":
            loaded.extend(load_json_faq(p))
        else:
            logger.warning("Skipping unsupported file type: %s", p)

    chunks, added = retriever.add_documents(loaded) if loaded else (0, 0)
    return {"files": len(paths), "docs": len(loaded), "chunks": chunks, "added": added}
