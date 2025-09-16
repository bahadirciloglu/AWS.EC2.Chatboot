from llama_index import load_index_from_storage, StorageContext
from llama_index.llm_predictor import LangchainLLMPredictor # type: ignore
from app.llm.bedrock import llm
from app.rag.loaders import load_documents

# LLM predictor ile service context oluştur
llm_predictor = LangchainLLMPredictor(llm=llm)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

storage_context = StorageContext.from_defaults(persist_dir="my_index")
index = load_index_from_storage(storage_context, service_context=service_context)

# Sorgulama fonksiyonu örneği
def query_knowledge_base(query: str):
    query_engine = index.as_query_engine()
    return query_engine.query(query)
