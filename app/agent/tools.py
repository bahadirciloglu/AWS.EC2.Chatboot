from langchain.agents import Tool
import logging
import json
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.bedrock import Bedrock
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Sadece kök dizindeki app.log
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app.agent.tools")

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

Settings.llm = Bedrock(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    region="us-west-2"
)

# JSON dosyasını oku
with open("data/rag_corpus/q&a.json", "r", encoding="utf-8") as f:
    qa_pairs = json.load(f)

# Her soru-cevap çiftini bir doküman olarak ekle
documents = []
for pair in qa_pairs:
    doc_text = f"Soru: {pair['soru']}\nCevap: {pair['cevap']}"
    documents.append(Document(text=doc_text))

# Vektör index oluştur
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

def get_weather(city: str) -> str:
    # Basit örnek, gerçek API entegrasyonu da olabilir
    logger.info(f"Tool çağrıldı: get_weather, city: {city}")
    return f"{city} için hava durumu: Güneşli"

def my_tool(input):
    logger.info(f"Tool çağrıldı: my_tool, input: {input}")
    # ... tool işlemleri ...

def another_tool(param1, param2):
    logger.info(f"Tool çağrıldı: another_tool, param1: {param1}, param2: {param2}")
    # ... tool işlemleri ...

def search_knowledge_base(query: str) -> str:
    logger.info(f"Tool çağrıldı: search_knowledge_base, query: {query}")
    response = query_engine.query(query)
    return str(response)

tools = [
    {
        "name": "get_weather",
        "description": "Şehir için hava durumu bilgisini döner.",
        "func": get_weather
    },
    {
        "name": "search_knowledge_base",
        "description": "Bilgi tabanında arama yapar.",
        "func": search_knowledge_base
    }
]

prompts_dir = "data/prompts"  # c/data/prompts/ kök dizine göre
prompt_files = [f for f in os.listdir(prompts_dir) if f.endswith(".txt") or f.endswith(".json")]

prompts = []
for fname in prompt_files:
    with open(os.path.join(prompts_dir, fname), "r", encoding="utf-8") as f:
        prompts.append(f.read())

with open("data/context.md", "r", encoding="utf-8") as f:
    context = f.read()

prompt_template = prompts[0]  # veya uygun bir prompt seçimi
final_prompt = f"{prompt_template}\n\nEk Bağlam:\n{context}"
print(final_prompt)

logger.info(f"LLM'e gönderilen prompt:\n{final_prompt}")

for prompt_template in prompts:
    combined = f"{prompt_template}\n\nEk Bağlam:\n{context}"
    print("Kombinasyon:\n", combined)

assert len(prompts) > 0
assert "iletişim" in context  # örnek bir anahtar kelime
