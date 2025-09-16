from llama_index import SimpleDirectoryReader

def load_documents(data_path: str = "data/knowledge_base/"):
    """
    Belirtilen dizindeki dokümanları yükler ve döner.
    """
    reader = SimpleDirectoryReader(data_path)
    docs = reader.load_data()
    return docs
