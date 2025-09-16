import json
import chromadb

def test_qa_corpus_load():
    with open("data/rag_corpus/q&a.json", "r", encoding="utf-8") as f:
        qa_data = json.load(f)
    assert len(qa_data) > 0
    assert "question" in qa_data[0] and "answer" in qa_data[0]

def test_qa_corpus_in_chromadb():
    client = chromadb.Client()
    collection = client.create_collection("beeai_qa_test")
    qa_data = [
        {"question": "BeeAI nedir?", "answer": "BeeAI, konaklama ve ağırlama sektörüne özel yapay zeka ve robotik çözümler geliştiren bir ajanstır."}
    ]
    for item in qa_data:
        collection.add(
            documents=[item["answer"]],
            metadatas=[{"question": item["question"]}],
            ids=[item["question"]]
        )
    results = collection.query(query_texts=["BeeAI nedir?"], n_results=1)
    assert results["documents"][0][0] == "BeeAI, konaklama ve ağırlama sektörüne özel yapay zeka ve robotik çözümler geliştiren bir ajanstır."
