import logging
from logging.handlers import RotatingFileHandler
from llama_index.core import Settings, load_index_from_storage, StorageContext, VectorStoreIndex, Document
from llama_index.llms.bedrock import Bedrock
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from fastapi import FastAPI, Request, Body, Depends, HTTPException
# from app.api.routes import router as api_router
from app.agent.agent import run_agent
from app.schemas.chat import ChatRequest, ChatResponse
from app.logger import logger
import os
from charset_normalizer import from_path
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# LLM ve embedding ayarları
Settings.llm = Bedrock(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-west-2"
)
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.aws.chatbot", "https://aws.chatbot"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ChromaDB client ve koleksiyon
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("aws_chatbot_rag")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Var olan index'i yükle
storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

class SoruModel(BaseModel):
    soru: str

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

@app.post("/rag-query")
async def rag_query(payload: dict = Body(...)):
    yanit = query_engine.query(payload.get("soru", ""))
    return {"yanit": str(yanit)}

@app.get("/welcome")
def welcome():
    return {"response": "AWS.Chatbot Chatbot'a hoş geldiniz!"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test-redis")
def test_redis():
    # Redis bağlantı testi kodu
        return {"redis": "ok"}

@app.get("/test-bedrock")
def test_bedrock():
    # Bedrock bağlantı testi kodu
        return {"bedrock": "ok"}

@app.post("/endpoint")
def endpoint(payload: dict = Body(...)):
    text = payload.get("text", "")
    # ... mevcut kod ...
    return {"result": text}

@app.post("/ornek")
def ornek():
    return {"result": "ornek başarılı"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logging.info(
        f"User: {request.user_id}, Session: {request.session_id}, Message: {request.message}"
    )
    response_text = run_agent(request.message)
    # Google Sheet'e hem kullanıcı mesajını hem cevabı yaz
    log_to_google_sheet(request.user_id, request.session_id, request.message, response_text)
    return ChatResponse(response=response_text, session_id=request.session_id)

# Diğer endpoint'ler ve yardımcı fonksiyonlar burada aynı şekilde kalabilir.

def initialize_index():
    if not os.path.exists("storage/docstore.json"):
        documents = []
        data_dir = "data"
        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="latin-1") as f:
                    documents.append(Document(text=f.read()))
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir="storage")
        print("Index başarıyla oluşturuldu ve storage/ klasörüne kaydedildi.")
    else:
        print("Var olan index bulundu, tekrar embed/index yapılmadı.")

def log_to_google_sheet(user_id, session_id, user_message, bot_response):
    import gspread
    from google.oauth2.service_account import Credentials

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'gen-lang-client-0894486414-5b3a5036e609.json'
    SPREADSHEET_ID = '140rnsQd4rZrK2YMPW_XUT2TAq0tWso2her-xqfpjLiI'

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    worksheet.append_row([user_id, session_id, user_message, bot_response])
