from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
import json
from charset_normalizer import from_path

# HuggingFace embedding modelini ayarla
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# data/ klasöründeki tüm dosyaları oku
documents = []
data_dir = "data"
for filename in os.listdir(data_dir):
    file_path = os.path.join(data_dir, filename)
    if os.path.isfile(file_path):
        # Sadece .json ve .md dosyalarını işle
        if filename.lower().endswith('.md'):
            # .md dosyasını metin olarak oku
            result = from_path(file_path).best()
            if result is not None:
                content = str(result)
                documents.append(Document(text=content))
            else:
                print(f"Uyarı: {file_path} dosyasının kodlaması tespit edilemedi, atlanıyor.")
        elif filename.lower().endswith('.json'):
            # .json dosyasını oku ve metin olarak indexle
            result = from_path(file_path).best()
            if result is not None:
                try:
                    json_content = json.loads(str(result))
                    # Tüm json'u metin olarak indexlemek için:
                    content = json.dumps(json_content, ensure_ascii=False, indent=2)
                    documents.append(Document(text=content))
                except Exception as e:
                    print(f"Uyarı: {file_path} dosyası JSON olarak parse edilemedi: {e}")
            else:
                print(f"Uyarı: {file_path} dosyasının kodlaması tespit edilemedi, atlanıyor.")

# Index oluştur ve storage/ klasörüne kaydet
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir="storage")
print("Index başarıyla oluşturuldu ve storage/ klasörüne kaydedildi.")
