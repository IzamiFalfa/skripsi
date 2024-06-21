# Gunakan image Python sebagai base image
FROM python:3.10

# Set direktori kerja di dalam container
WORKDIR /app

# Salin semua file ke dalam container
COPY . /app

# Salin direktori shots, saved_model, dan templates ke dalam container
COPY templates /app/templates
COPY uploads /app/uploads
COPY static /app/static

#download weight
RUN wget https://github.com/serengil/deepface_models/releases/download/v1.0/arcface_weights.h5

# Membuat direktori .deepface dan weights
RUN mkdir -p /root/.deepface/weights

# Memindahkan file ke direktori yang baru dibuat
RUN mv arcface_weights.h5 /root/.deepface/weights/

# Instal dependensi lainnya
RUN pip install --no-cache-dir -r requirements.txt

# Install dependensi yang diperlukan, termasuk dependensi OpenGL
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Exposed port untuk Flask app
EXPOSE 8080

# Jalankan aplikasi Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]