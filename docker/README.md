# 🐳 Infrastructure (Docker)

> **Zone:** Containerization & Services
> **Access:** DevOps

## Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| **Redis** | `redis:alpine` | 6379 | Real-time messaging bus. |
| **Worker** | `python:3.12` | - | Runs `run_production.py` loop. |
| **Dashboard**| `python:3.12` | 8501 | Streamlit UI. |

## Commands
```bash
# Start All
docker-compose up -d

# Rebuild Worker
docker-compose build worker
```
