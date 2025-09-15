# Q&AChatBot

A modern, full-stack chatbot application built with a React frontend and Python FastAPI backend.

## 🚀 Features

- Interactive chat interface
- Real-time messaging
- Backend API for conversation handling
- Modern, responsive UI
- Easy deployment with Docker

## 🛠️ Tech Stack

- **Frontend**: Next.js (React + TypeScript), Tailwind CSS
- **Backend**: Python, FastAPI, Langchain
- **Database**: Pinecone
- **Containerization**: Docker

## 📦 Project Structure

```
ChatBot/
├── backend/           # FastAPI backend
│   ├── src/           # Source code
│   ├── Dockerfile     # Backend Docker configuration
│   └── pyproject.toml # Python dependencies
├── frontend/          # React frontend
│   ├── src/           # Source code
│   └── Dockerfile     # Frontend Docker configuration
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (3.12+)
- Docker (**optional**, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ChatBot
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -e .
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

### Running Locally

1. **Start the backend**
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```

2. **Start the frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🐳 Docker Deployment

To run the application using Docker:

```bash
docker-compose up --build
```

## 📝 Environment Variables

### Backend
Create a `.env` file in either the repo root or the `backend/` directory (both are loaded; `backend/.env` overrides root during dev):

```
# App
APP_ENV=development
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

# Providers
OPENAI_API_KEY=your-openai-key

# Pinecone
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX=chatbot-faq-index
PINECONE_NAMESPACE=default

# Models (optional overrides)
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
TEMPERATURE=0.2
MAX_TOKENS=512
```

### Frontend
Create a `.env.local` file in the `frontend` directory (Next.js will load this automatically):

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Windsurf](https://windsurf.com/)

---
