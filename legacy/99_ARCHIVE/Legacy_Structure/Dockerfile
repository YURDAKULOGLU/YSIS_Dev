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
# git: for Aider/Version Control
# curl/wget: for healthchecks
# build-essential: for compiling python packages (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Work Directory
WORKDIR ${WORKDIR}

# Install uv (The High-Performance Installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install Frameworks using uv (Much faster resolution)
# We create a virtual environment first, as uv prefers it
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
# This ensures we use the pysqlite3-binary instead of system sqlite
ENV LD_LIBRARY_PATH=/usr/local/lib

# Copy Project Files
# We only copy the .YBIS_Dev directory as that is our scope
COPY .YBIS_Dev/ ${WORKDIR}/.YBIS_Dev/
COPY .git/ ${WORKDIR}/.git/

# Set Python Path
ENV PYTHONPATH="${WORKDIR}:${WORKDIR}/.YBIS_Dev"

# Default Command (The Dog's Heartbeat)
CMD ["tail", "-f", "/dev/null"]
