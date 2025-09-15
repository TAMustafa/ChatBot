# Chatbot Backend (FastAPI + LangChain + Pinecone)

Production-ready RAG backend providing `/api/chat` with structured output for a better UI.

## What this service does

- __Health__: `/api/health` returns `{ "status": "ok" }`.
- __RAG Chat__: `/api/chat` accepts `{ "query": string }` and returns:
  ```json
  {
    "answer": "free text answer",
    "structured": {
      "summary": "short summary for UI",
      "bullets": ["point 1", "point 2"]
    },
    "sources": ["source1.pdf"],
    "confidence": 0.9
  }
  ```
  The `structured` field is optional. When present, the frontend renders a concise summary with bullet points and source citations.

- __Ingestion__: Utilities parse PDF/Markdown/JSON into chunks, embed with OpenAI, and upsert into Pinecone.

## Configuration

Configure environment variables in `.env` (do not commit secrets). See project root `.env.example` for guidance.

Key variables:
- `OPENAI_API_KEY` – required.
- `PINECONE_API_KEY` – required.
- `PINECONE_INDEX` – Pinecone index name (must match embedding dimension).
- `PINECONE_NAMESPACE` – logical namespace within the index.
- `CHAT_MODEL`, `EMBEDDING_MODEL`, `TEMPERATURE`, `MAX_TOKENS` – model settings.

## Install & Run

Install with pip (editable) or your preferred workflow:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .

# Start the API with Uvicorn (development)
uvicorn src.main:app --reload
```

API available at http://localhost:8000

## Ingestion

1) Ensure Pinecone index is created with the correct __dimension__ for your embedding model.
   - For `text-embedding-3-small` the vector __dimension is 1536__.
   - Use the helper:
     ```bash
     python scripts/setup_pinecone.py
     ```
     If an existing index has a different dimension, delete it in Pinecone Console and re-run.

2) Ingest files (PDF/Markdown/JSON) under `backend/data/` or any path:
   ```bash
   python scripts/ingest.py ./data
   # or one file
   python scripts/ingest.py ./data/myfile.pdf
   ```

## Development Notes

- Settings in `src/config/settings.py` load `.env` from both repo root and backend directory.
- RAG modules:
  - `src/core/embedding.py` – OpenAI embeddings
  - `src/core/retrieval.py` – Pinecone vector store + chunking
  - `src/core/prompt.py` – prompt construction
  - `src/core/llm_client.py` – ChatOpenAI
  - `src/core/rag.py` – RAG pipeline and structured formatting
  - `src/core/ingest.py` – ingestion helpers

## Testing

```bash
uv run pytest -q
```

## Docker

```bash
docker build -t chatbot-backend ./backend
docker run --env-file .env -p 8000:8000 chatbot-backend
```

The server will start on `http://localhost:8000`. Endpoints:

- `GET /api/health` – health check
- `POST /api/chat` – chat with body `{ "query": "..." }`

