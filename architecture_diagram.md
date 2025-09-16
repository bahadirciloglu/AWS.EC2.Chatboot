# Chatbot - System Architecture Diagram

## Simple ASCII Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User/Client   │───▶│   Nginx Proxy    │───▶│   FastAPI App   │
│   (Browser)     │    │  (SSL/HTTPS)     │    │   (Port 8000)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Google Sheets │◀───│   Agent Module   │───▶│  LlamaIndex RAG │
│   (Logging)     │    │  (run_agent)     │    │    Pipeline     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Redis Cache   │◀───│   Session Mgmt   │    │   ChromaDB      │
│  (Optional)     │    │   & State        │    │ Vector Store    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  HuggingFace    │───▶│   Embeddings     │    │   AWS Bedrock   │
│  Transformers   │    │   Processing     │    │   Claude LLM    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Detailed Component Flow

### 1. Request Flow
```
User Request → Nginx → FastAPI → Agent Module → RAG Pipeline
```

### 2. RAG Processing Flow
```
Query → Embedding (HuggingFace) → Vector Search (ChromaDB) → 
Context Retrieval → LLM Processing (AWS Bedrock Claude) → Response
```

### 3. Data Storage & Logging
```
Session Data → Redis (Optional)
Chat Logs → Google Sheets
Vector Data → ChromaDB
System Logs → Local Files (with auto-cleanup)
```

## Key Components

### Frontend Layer
- **Nginx**: Reverse proxy, SSL termination, load balancing
- **CORS**: Configured for aws.chatbot domains

### API Layer
- **FastAPI**: REST API endpoints (/chat, /rag-query, /welcome, /health)
- **Pydantic**: Request/response validation
- **CORS Middleware**: Cross-origin request handling

### AI/ML Layer
- **LlamaIndex**: RAG pipeline orchestration
- **AWS Bedrock**: Claude 3.5 Sonnet LLM
- **HuggingFace**: Sentence transformers for embeddings
- **ChromaDB**: Vector database for semantic search

### Data Layer
- **ChromaDB**: Persistent vector storage
- **Redis**: Session state management (optional)
- **Google Sheets**: Chat logging and analytics
- **Local Storage**: Index persistence, log files

### Infrastructure Layer
- **EC2**: AWS compute instance
- **systemd**: Service management (chatbot.service)
- **Cron Jobs**: Automated log cleanup
- **Environment Variables**: Configuration management

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/welcome` | GET | Health check and welcome message |
| `/chat` | POST | Main chat interface with session management |
| `/rag-query` | POST | Direct RAG query without session |
| `/health` | GET | System health status |
| `/test-redis` | GET | Redis connectivity test |
| `/test-bedrock` | GET | AWS Bedrock connectivity test |

## Data Flow Example

1. **User sends message** via web interface
2. **Nginx forwards** request to FastAPI
3. **FastAPI validates** request and logs interaction
4. **Agent module processes** message through RAG pipeline
5. **HuggingFace creates** embeddings for semantic search
6. **ChromaDB retrieves** relevant context documents
7. **AWS Bedrock Claude** generates response using context
8. **Response logged** to Google Sheets
9. **Final response** returned to user via FastAPI

## Security & Compliance

- **KVKV/GDPR Compliant**: No personal data in logs
- **SSL/TLS**: Encrypted communication
- **AWS IAM**: Secure cloud resource access
- **Log Rotation**: Automated cleanup after 90 days
- **Data Masking**: PII removed from system logs