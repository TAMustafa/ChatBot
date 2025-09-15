# Chatbot Frontend (Next.js + TypeScript + Tailwind)

A modern chat UI that connects to the backend `/api/chat` endpoint and renders structured answers (summary + bullets), sources, and a confidence indicator.

## What this app does

- Calls the backend with the user's question.
- Displays the assistant's response using:
  - A concise summary (when available)
  - Bullet points for key details
  - Source citations and confidence
- Falls back to full text if no structured summary is present.

## Configure & Run

1) Configure backend URL (recommended via `.env.local`):

Create `frontend/.env.local` with:

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

2) Install and start the dev server:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

Ensure the backend is running and has ingested content for relevant answers.

## Components

- `src/components/ChatWindow/ChatWindow.tsx` – main container
- `src/components/Message/Message.tsx` – renders messages with structured formatting
- `src/components/InputBox/InputBox.tsx` – user input
- `src/hooks/useChat.ts` – chat state and API integration
- `src/services/apiClient.ts` – HTTP client and types

## Testing & Linting

```bash
npm run test
npm run lint
npm run typecheck
```

## Docker

```bash
docker build -t chatbot-frontend ./frontend
docker run -p 3000:3000 -e NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 chatbot-frontend
```
