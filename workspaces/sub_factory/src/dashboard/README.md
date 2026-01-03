# 🖥️ YBIS Dashboard

> **Zone:** User Interface
> **Tech:** Streamlit (Python)

## How to Run
Usually managed by `docker-compose`. To run manually:
```bash
streamlit run src/dashboard/app.py
```

## Features
- **Task Board:** Visualizes `Knowledge/LocalDB/tasks.db`.
- **System Health:** Shows status of Redis, Git, and storage.
- **Agent Logs:** Streams logs from `logs/system.json.log`.

## TODO
- [ ] Migrate from JSON to SQLite (See Task `DASHBOARD-UPDATE`).
