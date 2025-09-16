# Kartal.AI Chatbot Geliştirici Kılavuzu

## 1. Proje Mimarisi ve Yapısı
- FastAPI tabanlı backend
- Gradio tabanlı frontend (opsiyonel)
- LlamaIndex ile RAG pipeline
- ChromaDB vektör veritabanı
- AWS Bedrock (Claude) LLM entegrasyonu
- Redis (opsiyonel)

## 2. Kurulum ve Geliştirme Ortamı
- Python 3.9+ gereklidir.
- Sanal ortam oluşturun ve bağımlılıkları yükleyin:
  ```sh
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Ortam değişkenlerini `.env` dosyasında tanımlayın.

## 3. Kod Standartları ve Katkı Kuralları
- PEP8 kodlama standartlarına uyun.
- Fonksiyon ve sınıflar için docstring ekleyin.
- PR ve issue açmadan önce testlerinizi çalıştırın.

## 4. API ve Modül Dokümantasyonu
- Tüm endpoint'ler için [http://localhost:8000/docs](http://localhost:8000/docs) adresinde otomatik API dokümantasyonu mevcuttur.
- Ana modüller: `app/main.py`, `app/agent/`, `app/schemas/`, `app/utils/`

## 5. Test ve CI/CD
- Testler `tests/` klasöründe yer alır.
- Testleri çalıştırmak için:
  ```sh
  PYTHONPATH=. pytest tests/
  ```
- CI/CD için GitHub Actions veya benzeri bir sistem entegre edilebilir.

## 6. Yayın ve Bakım
- EC2 üzerinde deployment, Nginx reverse proxy ve SSL kurulumu için dokümantasyonu takip edin.
- Otomatik log temizliği için cron job:
  ```
  0 3 * * * /usr/bin/python3 /home/ec2-user/ec2-c/app/utils/delete_old_logs.py
  ```
- Yedekleme ve felaket kurtarma prosedürlerini uygulayın.

## 7. Geliştiriciye Yönelik SSS
- **S: API neden 405/500 hatası veriyor?**
  - C: Endpoint ve istek formatını kontrol edin, backend'in çalıştığından emin olun.
- **S: Loglar neden silinmiyor?**
  - C: Cron job ve scriptin doğru çalıştığından emin olun.
- **S: AWS Bedrock erişim hatası alıyorum.**
  - C: AWS kimlik bilgilerinizi ve erişim izinlerinizi kontrol edin.

## 8. Katkı ve Lisans
- Katkı sağlamak isteyenler için PR ve issue süreçleri aktiftir.
- Lisans: MIT 