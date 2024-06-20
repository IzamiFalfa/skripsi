import requests
import time
from pathlib import Path

# URL endpoint untuk mengunggah gambar
url_upload = "http://127.0.0.1:5000/upload"

# Jalur folder yang berisi file gambar
folder_gambar = "D:\KULIAH\SILABUS SEMESTER 8\Skripsi\Dataset Wajah\bush_10"

# Iterasi melalui semua file di folder gambar
for file_path in Path(folder_gambar).glob("*.*"):
    # Membuka file gambar dalam mode biner
    with open(file_path, "rb") as file:
        # Membuat payload dengan file dan kunci "file"
        payload = {
            "file": (file_path.name, file, "image/" + file_path.suffix[1:])
        }

        # Mengirimkan permintaan POST ke endpoint upload
        response = requests.post(url_upload, files=payload)

        # Memeriksa status respons
        if response.status_code == 200:
            print(f"Gambar {file_path.name} berhasil diunggah.")
        else:
            print(f"Gagal mengunggah gambar {file_path.name}. Status code: {response.status_code}")

    # Jeda 1 detik sebelum mengirimkan permintaan berikutnya
    time.sleep(1)