from app.agent.agent import add_user_message, get_user_history, clear_user_history

def test_add_and_get_user_message():
    user_id = "testuser"
    clear_user_history(user_id)
    add_user_message(user_id, "Merhaba")
    assert get_user_history(user_id) == ["Merhaba"]
