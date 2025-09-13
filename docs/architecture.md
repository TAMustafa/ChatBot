# Architecture

This project implements a production-ready Retrieval-Augmented Generation (RAG) system with a FastAPI backend and a Next.js (TypeScript) frontend.

## High-level design

- Backend (`backend/`)
  - FastAPI app exposing `/api/health` and `/api/chat`.
  - LangChain orchestrates the RAG pipeline.
  - OpenAI embeddings + chat models.
  - Pinecone vector store for retrieval.
  - Ingestion utilities for PDF/Markdown/JSON.
  - Configuration via `.env` + Pydantic settings (`src/config/settings.py`).

- Frontend (`frontend/`)
  - Next.js 14 (React 18) with Tailwind.
  - Simple chat UI with `ChatWindow`, `Message`, `InputBox`.
  - Calls backend via `src/services/apiClient.ts`.
  - Renders structured answers (summary + bullets) and source citations.

## Data flow

1. Ingestion
   - Files in `backend/data/` (PDF/Markdown/JSON) are parsed by `src/core/ingest.py`.
   - Text is chunked with `RecursiveCharacterTextSplitter`.
   - OpenAI embeddings are generated and upserted into Pinecone under the configured namespace.

2. Retrieval + Generation
   - `/api/chat` receives a `query`.
   - Top-K relevant chunks are retrieved from Pinecone (cosine similarity).
   - A prompt is built (`src/core/prompt.py`) combining system instructions, context, and question.
   - LLM produces an answer; a lightweight formatter derives `structured.summary` and `structured.bullets`.

3. Frontend rendering
   - UI shows the assistant answer as a short summary with bullets when available.
   - Sources and a confidence indicator are shown below the answer.

## Components overview

- `src/core/embedding.py`: wraps OpenAI embeddings.
- `src/core/retrieval.py`: Pinecone-based retriever and splitter.
- `src/core/prompt.py`: prompt templates.
- `src/core/llm_client.py`: Chat LLM client.
- `src/core/rag.py`: RAG pipeline and output formatting (structured answer).
- `src/api/endpoints/chat.py`: `/api/chat` endpoint.
- `src/core/ingest.py`: ingestion utilities for PDF/Markdown/JSON.

## Security considerations

- API keys are never committed; use `.env` only. `.env.example` is for placeholders.
- CORS is currently permissive for local development. Restrict in production.
- Consider adding auth (e.g., API keys) and rate-limiting if exposing publicly.

## Scaling considerations

- Pinecone handles vector similarity at scale.
- Stateless API instances scale horizontally.
- Add caching for frequent queries or pre-embeddings of common FAQs.
- Add streaming (SSE) to improve UX on slow responses.

## RAG best practices (ingestion)

- **Chunking strategy** (`CHUNK_SIZE`, `CHUNK_OVERLAP` in `.env`)
  - Lists and procedures often span paragraphs. Prefer smaller chunks with higher overlap (e.g., 700/300) to keep bullets together.
  - PDFs vary widely; try 500–1000 with 150–300 overlap. Re-ingest after tuning.
- **Metadata**
  - Preserve `source` and `page`. The app already carries `page` for PDFs via `pypdf`. These power per-page citations and targeted augmentation.
- **Data normalization**
  - Remove boilerplate (headers/footers) to reduce noise. Consider stripping page numbers that appear in running text.
- **Model choice**
  - Embeddings: `text-embedding-3-small` (1536-d) is cost-effective. Use an index with matching dimension in Pinecone.
  - If you need multilingual retrieval or very long contexts, consider larger or domain-tuned embedding models.
- **Re-ingestion**
  - Any change to chunk settings requires re-ingestion. The `scripts/ingest.py` script is idempotent and additive.

## RAG best practices (retrieval)

- **MMR (Max Marginal Relevance)**
  - Enabled by default in `RAGPipeline` to increase coverage across topics and avoid redundant chunks.
  - Tune `TOP_K` and the candidate `fetch_k` (see `Retriever.mmr_search`) for breadth vs. latency.
- **Same-page augmentation**
  - After initial retrieval, the pipeline fetches additional chunks from the same `source` and `page` to capture full lists broken across chunk boundaries.
- **Prompting for completeness**
  - The system prompt instructs the LLM to enumerate ALL items across snippets and include page numbers if present.
- **Confidence**
  - Current confidence is a heuristic based on retrieved count. Replace with calibrated metrics if needed (e.g., retrieval score aggregation or answerability classifiers).

## Enterprise readiness checklist

- **Security**
  - Place secrets in `.env` only; never commit to VCS. Use different env files per environment and inject via your orchestrator (Docker/K8s/Vercel/etc.).
  - Restrict CORS and add authentication (API key or OAuth) before exposing publicly.
  - Consider request/response redaction to avoid logging sensitive data.
- **Observability**
  - Add structured logging and trace IDs. Connect to your APM (e.g., OpenTelemetry) to trace latency through retrieval and LLM calls.
  - Log retrieval metadata (top-k scores, sources, pages) to evaluate coverage.
- **Evaluation**
  - Build a small eval set of Q&A and run regression checks when changing chunk sizes, models, or prompts.
  - Track answer completeness (did all expected bullets appear?), citation accuracy, and latency.
- **Cost control**
  - Cache embeddings for unchanged documents. Use Pinecone upsert only when content changes.
  - Use smaller chat models when acceptable and increase `MAX_TOKENS` judiciously.
- **Data governance**
  - Keep an inventory of sources and versions. Rebuild the index when source versions change.
  - For regulated data, consider encrypting documents at rest and implementing access control in your API layer.

## Business adoption guide

1. **Prepare your knowledge base**
   - Collect your FAQs, policies, product docs as PDF/Markdown/JSON.
   - Ensure file names are meaningful; they become `sources` in citations.

2. **Configure environment**
   - Copy `.env.example` to `.env` and fill `OPENAI_API_KEY`, `PINECONE_API_KEY`.
   - Set `PINECONE_INDEX` and ensure the index dimension matches your embedding model (1536 for `text-embedding-3-small`).
   - Tune `TOP_K`, `CHUNK_SIZE`, `CHUNK_OVERLAP` for your content.

3. **Create Pinecone index**
   - Run `uv run python scripts/setup_pinecone.py`. If an index exists with the wrong dimension, delete and re-run.

4. **Ingest documents**
   - Place files under `backend/data/` and run `uv run python scripts/ingest.py ./data`.
   - Verify the summary output (files/docs/chunks) and that your index vector count increases in Pinecone.

5. **Run the app**
   - Backend: `uv run python -m src.main`
   - Frontend: `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 npm run dev`
   - Ask representative business questions and inspect:
     - Completeness of answers
     - Citations and page numbers
     - Latency

6. **Iterate**
   - If lists are truncated, decrease `CHUNK_SIZE` and increase `CHUNK_OVERLAP`, then re-ingest.
   - If context blends unrelated sections, increase MMR diversity (lower `lambda_mult`, raise `fetch_k`).
   - If latency is high, reduce `TOP_K` slightly, cache, or consider streaming.

7. **Harden for production**
   - Add authentication, rate limiting, and request size limits in FastAPI.
   - Implement CI (lint/tests/type-check) and deployment pipelines.
   - Add a `/feedback` endpoint to collect user corrections and continuously improve sources.
