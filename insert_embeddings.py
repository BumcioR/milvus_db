import os
import json
from pymilvus import connections, Collection

# Ścieżki i dane
data_dir = "./data"
file_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.json"
embeddings_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska-Embeddings.json"
collection_name = "rag_texts_and_embeddings"

# Połączenie z Milvus
connections.connect(alias="default", host="localhost", port="19530")

# Załaduj kolekcję
collection = Collection(name=collection_name)

def insert_embeddings(file_json, embeddings_json, client=collection):
    rows = []

    with open(os.path.join(data_dir, file_json), "r", encoding="utf-8") as t_f, \
         open(os.path.join(data_dir, embeddings_json), "r", encoding="utf-8") as e_f:

        text_data = json.load(t_f)
        embedding_data = json.load(e_f)

        text_data = [d["text"] for d in text_data]
        embedding_data = [d["embedding"] for d in embedding_data]

        for text, embedding in zip(text_data, embedding_data):
            rows.append({"text": text, "embedding": embedding})

    print(f"📥 Wstawianie {len(rows)} rekordów do kolekcji '{collection_name}'...")
    client.insert(rows)
    print("✅ Wstawiono dane.")

# Wstaw dane i załaduj kolekcję do pamięci
insert_embeddings(file_json, embeddings_json)
collection.load()
print("✅ Kolekcja załadowana do pamięci.")
