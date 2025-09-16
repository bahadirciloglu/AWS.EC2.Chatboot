# Kartal.AI Chatbot - Teknik Dokümantasyon

## Genel Bakış

Kartal.AI Chatbot, FastAPI tabanlı bir backend, Gradio tabanlı bir frontend, LlamaIndex ile RAG pipeline, ChromaDB vektör veritabanı ve AWS Bedrock (Claude) LLM entegrasyonundan oluşur. Redis, kullanıcı session'larını ve cache'i yönetir. Google Sheets, tüm etkileşimleri loglar.

## API Endpoints

### 1. Welcome Endpoint
- **URL:** `/welcome`
- **Method:** GET
- **Açıklama:** Sistem sağlık kontrolü ve karşılama mesajı
- **Yanıt:** `{ "response": "Kartal.AI Chatbot'a hoş geldiniz!" }`

### 2. Chat Endpoint
- **URL:** `/chat`
- **Method:** POST
- **Açıklama:** Ana sohbet arayüzü
- **Request Body:**
```json
{
    "message": "Merhaba, nasılsınız?",
    "session_id": "user_123"
}
```

### 3. RAG Query Endpoint
- **URL:** `/rag-query`
- **Method:** POST
- **Açıklama:** Doğrudan RAG sorgusu
- **Request Body:**
```json
{
    "query": "Kartal.AI nedir?",
    "context": "optional_context"
}
```
- **Yanıt:** `{ "yanit": "Kartal.AI, konaklama ve ağırlama sektörüne özel yapay zeka..." }`

### 4. Health Check Endpoint
- **URL:** `/health`
- **Method:** GET
- **Açıklama:** Sistem durumu kontrolü
- **Yanıt:** Sistem sağlık bilgileri

### 5. Redis Test Endpoint
- **URL:** `/test-redis`
- **Method:** GET
- **Açıklama:** Redis bağlantı testi
- **Yanıt:** Redis durum bilgileri

### 6. Bedrock Test Endpoint
- **URL:** `/test-bedrock`
- **Method:** GET
- **Açıklama:** AWS Bedrock bağlantı testi
- **Yanıt:** Bedrock durum bilgileri

## Sistem Mimarisi

### Backend (FastAPI)
- **Port:** 8000
- **Framework:** FastAPI + Python 3.9+
- **Async Support:** Evet
- **CORS:** Aktif
- **Rate Limiting:** Aktif

### Frontend (Gradio)
- **Port:** 7860
- **Framework:** Gradio
- **Real-time Updates:** WebSocket
- **Responsive Design:** Evet

### AI Engine
- **RAG Pipeline:** LlamaIndex
- **LLM:** AWS Bedrock (Claude)
- **Embeddings:** HuggingFace Transformers
- **Vector DB:** ChromaDB

### Data Storage
- **Cache:** Redis (Port 6379)
- **Vector DB:** ChromaDB (Port 8001)
- **Logging:** Google Sheets API
- **Sessions:** Redis Streams

### Infrastructure
- **Proxy:** Nginx (Port 80/443)
- **SSL:** Let's Encrypt
- **Process Manager:** systemd
- **Auto-restart:** Aktif

## Kurulum ve Çalıştırma

### Gereksinimler
```bash
Python 3.9+
Redis Server
PostgreSQL (opsiyonel)
AWS Bedrock Access
Google Sheets API
```

### Kurulum
```bash
# Repository klonla
git clone <repository-url>
cd AWS-EC2-Chatboot

# Bağımlılıkları yükle
pip install -r requirements.txt

# Environment variables ayarla
cp .env.example .env
# .env dosyasını düzenle

# Redis başlat
redis-server

# Uygulamayı başlat
python main.py
```

### Environment Variables
```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
GOOGLE_SHEETS_ID=your_sheet_id

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## Performans Metrikleri

### Response Time
- **Average:** < 2 seconds
- **95th Percentile:** < 5 seconds
- **99th Percentile:** < 10 seconds

### Throughput
- **Concurrent Users:** 100+
- **Requests/Second:** 50+
- **Memory Usage:** < 2GB

### Accuracy
- **RAG Response Quality:** > 90%
- **LLM Response Relevance:** > 95%
- **Context Retrieval:** > 85%

## Güvenlik

### Authentication
- API Key authentication
- Rate limiting
- CORS protection
- Input validation

### Data Protection
- PII masking
- Secure logging
- Data encryption
- GDPR compliance

### Infrastructure
- SSL/TLS encryption
- Firewall rules
- Regular security updates
- Access control

## Monitoring ve Logging

### Health Checks
- System status monitoring
- Service availability
- Resource usage tracking
- Error rate monitoring

### Logging
- Request/response logging
- Error tracking
- Performance metrics
- User interaction logs

### Alerts
- Service down notifications
- Performance degradation alerts
- Error rate thresholds
- Resource usage warnings

## Troubleshooting

### Common Issues
1. **Redis Connection Error**
   - Redis server status kontrol et
   - Port 6379 açık mı kontrol et
   - Firewall ayarlarını kontrol et

2. **AWS Bedrock Error**
   - AWS credentials kontrol et
   - Region ayarlarını kontrol et
   - IAM permissions kontrol et

3. **ChromaDB Error**
   - Vector database status kontrol et
   - Disk space kontrol et
   - Permissions kontrol et

### Debug Commands
```bash
# Redis status
redis-cli ping

# FastAPI logs
tail -f app.log

# System resources
htop
df -h
free -h

# Network ports
netstat -tulpn | grep :8000
```

## Geliştirme ve Deployment

### Development
- Local development environment
- Hot reload support
- Debug mode
- Testing framework

### Staging
- Staging environment
- Integration testing
- Performance testing
- Security testing

### Production
- Production deployment
- Load balancing
- Auto-scaling
- Backup strategies

## API Documentation

### Swagger UI
- **URL:** `http://localhost:8000/docs`
- **Interactive API testing**
- **Request/response examples**
- **Schema validation**

### ReDoc
- **URL:** `http://localhost:8000/redoc`
- **Alternative documentation view**
- **Better for complex schemas**

## Support ve İletişim

### Technical Support
- **Email:** tech@kartal.ai
- **Documentation:** https://docs.kartal.ai
- **GitHub Issues:** Repository issues
- **Slack:** #kartal-ai-support

### Business Inquiries
- **Email:** info@kartal.ai
- **Website:** https://www.bahadir.ai
- **Phone:** +90 (212) XXX XX XX

---

*Kartal.AI - Transforming Hospitality with AI & Robotics*
