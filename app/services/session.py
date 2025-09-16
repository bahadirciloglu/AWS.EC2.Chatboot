from typing import Dict

# Basit in-memory session store (production için uygun değildir!)
session_store: Dict[str, dict] = {}

def get_user_session(session_id: str) -> dict:
    return session_store.get(session_id, {})

def update_user_session(session_id: str, data: dict):
    session_store[session_id] = data

def clear_user_session(session_id: str):
    if session_id in session_store:
        del session_store[session_id]
