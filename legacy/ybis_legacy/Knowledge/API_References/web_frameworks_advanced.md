# FASTAPI & STREAMLIT ADVANCED MANUAL

## 1. FastAPI: Dependency Injection
Standard way to share logic (DB sessions, Auth, etc.).
```python
from typing import Annotated
from fastapi import Depends

async def get_db():
    db = Database()
    yield db
    db.close()

@app.get("/")
def read(db: Annotated[Database, Depends(get_db)]):
    return db.query()
```

## 2. Streamlit: Session State
Persist data across re-runs.
```python
import streamlit as st

if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button("Add"):
    st.session_state.counter += 1
```
Use `st.rerun()` to force an immediate update of the UI after state change.
