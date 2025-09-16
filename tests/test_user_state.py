import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def add_user_message(user_id, message):
    r.rpush(f"user:{user_id}:history", message)

def get_user_history(user_id):
    return [msg.decode() for msg in r.lrange(f"user:{user_id}:history", 0, -1)]

def clear_user_history(user_id):
    r.delete(f"user:{user_id}:history")

def test_user_state():
    user_id = "testuser"
    clear_user_history(user_id)
    add_user_message(user_id, "Merhaba")
    add_user_message(user_id, "Nasılsın?")
    history = get_user_history(user_id)
    assert history == ["Merhaba", "Nasılsın?"]
    print("Kullanıcı geçmişi okuma-yazma başarılı:", history)
    clear_user_history(user_id)
    assert get_user_history(user_id) == []
    print("Kullanıcı geçmişi temizleme başarılı.")

if __name__ == "__main__":
    test_user_state()
