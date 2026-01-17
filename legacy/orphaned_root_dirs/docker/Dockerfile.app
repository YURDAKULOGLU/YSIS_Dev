FROM python:3.12-slim

WORKDIR /repo

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Keep dependencies minimal; install from pyproject with pip for now.
COPY pyproject.toml README.md /repo/
RUN pip install --no-cache-dir -U pip \
  && pip install --no-cache-dir ".[dev]" || true

# Copy source last (better caching once deps are stable)
COPY . /repo

