# API Specification

Base URL: `http://localhost:8000`

## Health

- Method: GET
- Path: `/api/health`
- Response: `200 OK`
```json
{ "status": "ok" }
```

## Chat

- Method: POST
- Path: `/api/chat`
- Request Body:
```json
{
  "query": "string (required)"
}
```
- Response: `200 OK`
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

Notes:
- `structured` is optional. When present, the UI renders `summary` and `bullets` plus `sources` and `confidence`.
- `sources` contain the document identifiers (e.g., filenames) used for the answer.
- `confidence` is a lightweight heuristic in this demo and should not be treated as a calibrated score.
