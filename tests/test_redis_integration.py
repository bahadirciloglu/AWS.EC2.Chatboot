import pytest
from app.agent.agent import add_user_message, get_user_history, clear_user_history

def test_redis_user_history():
    user_id = "pytestuser"
    clear_user_history(user_id)
    add_user_message(user_id, "Hello")
    add_user_message(user_id, "World")
    history = get_user_history(user_id)
    assert history == ["Hello", "World"]
    clear_user_history(user_id)
    assert get_user_history(user_id) == []
