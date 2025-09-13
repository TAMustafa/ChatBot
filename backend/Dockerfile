# syntax=docker/dockerfile:1.7-labs
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

# Copy project metadata
COPY pyproject.toml README.md ./
COPY src ./src

# Install dependencies and project
RUN uv sync --frozen --no-cache

ENV PYTHONPATH=/app
ENV PORT=8000
EXPOSE 8000

# Default command
CMD ["uv", "run", "python", "-m", "src.main"]
