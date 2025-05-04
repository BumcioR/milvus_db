import os
import requests

# Definicje ścieżek
pdf_url = "https://www.iab.org.pl/wp-content/uploads/2024/04/Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf"
file_name = "Przewodnik-po-sztucznej-inteligencji-2024_IAB-Polska.pdf"
data_dir = "./data"
local_pdf_path = os.path.join(data_dir, file_name)

# Upewnij się, że katalog istnieje
os.makedirs(data_dir, exist_ok=True)

# Pobieranie pliku jeśli go jeszcze nie ma
if not os.path.exists(local_pdf_path):
    print(f"Pobieranie pliku PDF z {pdf_url}...")
    try:
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()  # podnosi wyjątek dla błędnych odpowiedzi HTTP
        with open(local_pdf_path, "wb") as f:
            f.write(response.content)
        print("Plik został pobrany i zapisany jako:", local_pdf_path)
    except requests.exceptions.RequestException as e:
        print("Błąd podczas pobierania pliku:", e)
else:
    print("Plik PDF już istnieje:", local_pdf_path)
