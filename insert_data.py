import json
from pymilvus import MilvusClient

# Połączenie z Milvusem
milvus_client = MilvusClient(host="localhost", port="19530")

# Ścieżki do plików z tekstem i embeddingami
file_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.json"
embeddings_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska-Embeddings.json"

def insert_embeddings(file_json, embeddings_json, client=milvus_client):
    rows = []
    with open(file_json, "r") as t_f, open(embeddings_json, "r") as e_f:
        text_data, embedding_data = json.load(t_f), json.load(e_f)
        text_data =  list(map(lambda d: d["text"], text_data))
        embedding_data = list(map(lambda d: d["embedding"], embedding_data))

        for page, (text, embedding) in enumerate(zip(text_data, embedding_data)):
            rows.append({"text":text, "embedding": embedding})

    # Insert danych do kolekcji
    client.insert(collection_name="rag_texts_and_embeddings", data=rows)

# Wstawianie danych do Milvusa
insert_embeddings(file_json, embeddings_json)
