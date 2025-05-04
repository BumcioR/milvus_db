import os
import json
import torch
import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer

# Konfiguracja
data_dir = "./data"
file_name = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf"
file_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.json"
embeddings_json = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska-Embeddings.json"

local_pdf_path = os.path.join(data_dir, file_name)
local_json_path = os.path.join(data_dir, file_json)
local_embeddings_path = os.path.join(data_dir, embeddings_json)

# Wczytanie modelu
model_name = "ipipan/silver-retriever-base-v1.1"
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(model_name, device=device)

# Funkcja do wyodrębniania tekstu z PDF-a, strona po stronie
def extract_text_from_pdf(pdf_path, file_json):
    document = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text().strip()
        pages.append({"page_num": page_num, "text": text})

    with open(os.path.join(data_dir, file_json), "w", encoding="utf-8") as file:
        json.dump(pages, file, indent=4, ensure_ascii=False)

# Funkcja do generowania embeddingów
def generate_embeddings(file_json, embeddings_json, model):
    with open(os.path.join(data_dir, file_json), "r", encoding="utf-8") as file:
        data = json.load(file)

    pages = [page["text"] for page in data]
    embeddings = model.encode(pages, show_progress_bar=True)

    embeddings_paginated = []
    for page_num in range(len(embeddings)):
        embeddings_paginated.append({
            "page_num": page_num,
            "embedding": embeddings[page_num].tolist()
        })

    with open(os.path.join(data_dir, embeddings_json), "w", encoding="utf-8") as file:
        json.dump(embeddings_paginated, file, indent=4, ensure_ascii=False)

# Główna logika
if __name__ == "__main__":
    if not os.path.exists(local_pdf_path):
        raise FileNotFoundError(f"Brakuje pliku PDF: {local_pdf_path}")

    print("Ekstrahowanie tekstu z PDF...")
    extract_text_from_pdf(local_pdf_path, file_json)

    print("Generowanie embeddingów...")
    generate_embeddings(file_json, embeddings_json, model)

    print("Zakończono. Pliki zapisane:")
    print(" - JSON z tekstami:", local_json_path)
    print(" - JSON z embeddingami:", local_embeddings_path)
