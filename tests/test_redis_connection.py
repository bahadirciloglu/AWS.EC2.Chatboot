import redis

def test_redis_connection():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        pong = r.ping()
        print("Redis bağlantısı başarılı:", pong)
    except Exception as e:
        print("Redis bağlantı hatası:", e)

if __name__ == "__main__":
    test_redis_connection()
