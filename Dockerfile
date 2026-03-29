FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app/backend

COPY backend/pyproject.toml backend/uv.lock ./
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN uv sync --frozen --no-dev

COPY backend/ .
COPY docs/ /app/docs/
COPY assets/ /app/assets/

ENV PATH="/app/backend/.venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
