# Base Image: Python 3.12 (Slim for size, but full features needed)
FROM python:3.12-slim

# Metdata
LABEL maintainer="YBIS Team"
LABEL description="YBIS Cloud-Native Agent Runtime (The Dog)"

# Environment Variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    WORKDIR=/app \
    AIDER_ANALYTICS=false \
    AIDER_CHECK_UPDATE=false

# System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Work Directory
WORKDIR ${WORKDIR}

# Install uv (The High-Performance Installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install Frameworks using uv
ENV VIRTUAL_ENV=/app/.venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN uv pip install \
    langgraph \
    langchain \
    langchain-openai \
    crewai \
    pyautogen \
    aider-chat \
    fastmcp \
    redis \
    chromadb \
    pysqlite3-binary \
    pytest \
    flake8 \
    radon \
    black \
    isort \
    mypy

# Fix for ChromaDB requiring SQLite > 3.35
ENV LD_LIBRARY_PATH=/usr/local/lib

# Copy Project Files
# Context is Project Root. We copy .YBIS_Dev to /app/.YBIS_Dev
COPY .YBIS_Dev/ ${WORKDIR}/.YBIS_Dev/
COPY .git/ ${WORKDIR}/.git/ 

# Set Python Path
# Includes Project Root and the new Python Core location
ENV PYTHONPATH="${WORKDIR}:${WORKDIR}/.YBIS_Dev/20_WORKFORCE/01_Python_Core"

# Default Command (The Dog's Heartbeat)
CMD ["tail", "-f", "/dev/null"]