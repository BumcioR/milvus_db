import os
import json
from pymilvus import Collection
from sentence_transformers import SentenceTransformer

# Ścieżki i konfiguracja
data_dir = "./data"
file_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.json"
embeddings_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska-Embeddings.json"

# Model do embeddingów
model_name = "sentence-transformers/distiluse-base-multilingual-cased-v2"
model = SentenceTransformer(model_name)

# Zakładamy, że masz już działającego Milvusa i kolekcję "rag_texts_and_embeddings"
milvus_client = Collection("rag_texts_and_embeddings")  # ← to automatycznie odnajduje kolekcję po nazwie

# Funkcja do wyszukiwania
def search(model, query, client=milvus_client):
    print(f"Zapytanie: {query}")
    embedded_query = model.encode(query).tolist()
    
    results = client.search(
        data=[embedded_query],
        anns_field="embedding",
        param={"metric_type": "L2"},
        limit=1,
        output_fields=["text"]
    )
    
    matches = results[0]
    for match in matches:
        print(f"Znaleziony wynik (score={match.score}):")
        print(match.entity.get("text")[:500], "...")
    
    return matches

# Przykład wyszukiwania
if __name__ == "__main__":
    result = search(model, query="Czym jest sztuczna inteligencja")
