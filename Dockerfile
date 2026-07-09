FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.4.1

# System deps (needed for Poetry + builds)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy dependency definitions first (better caching)
COPY pyproject.toml poetry.lock* /app/

# Prevent Poetry from creating venv inside container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy source code
COPY . /app

# Default command (your exact execution path)
CMD ["poetry", "run", "python", "src/resume_generator/resume_generator.py"]