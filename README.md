# ChatBot Project

A modern, full-stack chatbot application built with a React frontend and Python FastAPI backend.

## 🚀 Features

- Interactive chat interface
- Real-time messaging
- Backend API for conversation handling
- Modern, responsive UI
- Easy deployment with Docker

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Vite
- **Backend**: Python, FastAPI
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

- Node.js (v16+)
- Python (3.9+)
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
Create a `.env` file in the `backend` directory:

```
# Backend configuration
APP_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-uri
```

### Frontend
Create a `.env` file in the `frontend` directory:

```
VITE_API_URL=http://localhost:8000
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

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Vite](https://vitejs.dev/)

---
