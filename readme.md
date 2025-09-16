# Kartal.AI Chatbot Backend & RAG Platform

## Proje Açıklaması

Kartal.AI, konaklama ve ağırlama sektörüne özel yapay zeka ve robotik çözümler sunan, RAG (Retrieval Augmented Generation) tabanlı bir chatbot ve bilgi tabanı platformudur. Proje, AWS Bedrock (Claude), LlamaIndex, ChromaDB ve FastAPI teknolojilerini kullanarak geliştirilmiştir.

## Özellikler

- **RAG Pipeline**: LlamaIndex ile gelişmiş bilgi tabanı sorgulama
- **LLM Integration**: AWS Bedrock Claude modeli entegrasyonu
- **Vector Database**: ChromaDB ile vektör tabanlı arama
- **Real-time Chat**: WebSocket destekli gerçek zamanlı sohbet
- **Multi-language Support**: Türkçe ve İngilizce dil desteği
- **Session Management**: Redis ile kullanıcı oturum yönetimi
- **Analytics**: Google Sheets entegrasyonu ile etkileşim logları

## Teknoloji Stack

- **Backend**: FastAPI + Python 3.9+
- **AI/ML**: LlamaIndex, HuggingFace Transformers
- **LLM**: AWS Bedrock (Claude)
- **Database**: ChromaDB (Vector), Redis (Cache)
- **Frontend**: Gradio + React
- **Infrastructure**: AWS EC2, Nginx, Docker

## Kurulum

```bash
# Repository klonla
git clone <repository-url>
cd AWS-EC2-Chatboot

# Bağımlılıkları yükle
pip install -r requirements.txt

# Environment variables ayarla
cp .env.example .env

# Redis başlat
redis-server

# Uygulamayı başlat
python main.py
```

## API Endpoints

### Welcome
```bash
GET /welcome
# Yanıt: { "response": "Kartal.AI Chatbot'a hoş geldiniz!" }
```

### Chat
```bash
POST /chat
# İstek: { "user_id": "...", "session_id": "...", "message": "..." }
# Yanıt: { "response": "...", "session_id": "..." }
```

### RAG Query
```bash
POST /rag-query
# İstek: { "soru": "Kartal.AI nedir?" }
# Yanıt: { "yanit": "Kartal.AI, konaklama ve ağırlama sektörüne özel yapay zeka..." }
```

## Kullanım

1. **Sistem Başlatma**: `python main.py`
2. **Web Arayüzü**: `http://localhost:8000`
3. **API Dokümantasyonu**: `http://localhost:8000/docs`
4. **Health Check**: `http://localhost:8000/health`

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

- **Website**: https://www.bahadir.ai
- **Email**: info@kartal.ai
- **GitHub**: [Repository Link]

---

*Kartal.AI - Transforming Hospitality with AI & Robotics*
