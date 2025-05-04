import os
import json
import fitz  # pymupdf

# Ścieżki
data_dir = "./data"
pdf_file = os.path.join(data_dir, "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf")
json_output = os.path.join(data_dir, "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.json")

# Parsowanie PDF-a
def parse_pdf_to_json(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:  # pomiń puste strony
            pages.append({"page": i + 1, "text": text})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)

    print(f"Zapisano {len(pages)} stron do {output_path}")

# Uruchom funkcję
parse_pdf_to_json(pdf_file, json_output)
