import requests
import base64

# Ganti nama file dan path sesuai kebutuhan
gambar_file = "D:\\KULIAH\\SILABUS SEMESTER 8\\Skripsi\\Dataset Wajah\\bush_10\\George_W_Bush_0006.jpg"

# Baca file gambar sebagai binary data
with open(gambar_file, "rb") as f:
    gambar_biner = f.read()

# Enkode data gambar ke base64
gambar_base64 = base64.b64encode(gambar_biner).decode("utf-8")

# Siapkan data request
data = {
    "file": gambar_base64
}

# Lakukan request POST ke API
url = "http://localhost:5000/upload"
response = requests.post(url, json=data)

# Periksa status response
if response.status_code == 200:
    print("Gambar berhasil diunggah")
else:
    print(f"Gagal mengunggah gambar: {response.status_code}")
