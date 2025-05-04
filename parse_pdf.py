import fitz  # PyMuPDF
import json

def parse_pdf_to_json(pdf_path, output_json):
    doc = fitz.open(pdf_path)
    pages = [{"page": i, "text": page.get_text()} for i, page in enumerate(doc)]
    with open(output_json, "w") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)

# Przykład użycia
parse_pdf_to_json(
    "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf",
    "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.json"
)
