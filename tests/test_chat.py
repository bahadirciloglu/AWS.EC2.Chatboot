import requests

def test_api_chat():
    url = "http://34.222.232.114:8000/chat"
    payload = {"message": "Merhaba, test mesajı!", "user_id": "test_user"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "response" in response.json()

if __name__ == "__main__":
    url = "http://34.222.232.114:8000/chat"
    data = {
        "message": "Merhaba, test mesajı!",
        "user_id": "test_user"
    }
    try:
        response = requests.post(url, json=data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Hata oluştu: {e}") 