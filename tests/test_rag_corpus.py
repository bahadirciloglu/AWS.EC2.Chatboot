import json
import chromadb

def test_qa_corpus_load():
    with open("data/rag_corpus/q&a.json", "r", encoding="utf-8") as f:
        qa_data = json.load(f)
    assert len(qa_data) > 0
    assert "soru" in qa_data[0] and "cevap" in qa_data[0]

def test_qa_corpus_in_chromadb():
    client = chromadb.Client()
    collection = client.create_collection("kartal_ai_qa_test")
    collection.add(
        {"soru": "Kartal.AI nedir?", "cevap": "Kartal.AI, konaklama ve ağırlama sektörüne özel yapay zeka ve robotik çözümler geliştiren bir ajanstır."}
    )
    results = collection.query(query_texts=["Kartal.AI nedir?"], n_results=1)
    assert results["documents"][0][0] == "Kartal.AI, konaklama ve ağırlama sektörüne özel yapay zeka ve robotik çözümler geliştiren bir ajanstır."