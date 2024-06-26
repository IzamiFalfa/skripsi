import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from deepface import DeepFace
import numpy as np
import cv2
from sql_connector import db,cursor

face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

cursor.execute("SELECT image, name FROM known_faces")
results = cursor.fetchall()

known_faces = []
known_face_names = []

# Memproses setiap hasil dari database
for result in results:
    image_data = np.asarray(bytearray(result[0]), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    known_faces.append(image)
    known_face_names.append(result[1])

# Mendefinisikan fungsi untuk melakukan verifikasi menggunakan VGG-Face
def predict(img_path):
    image = cv2.imread(img_path)
    # Mengubah gambar menjadi grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_location = face_detector.detectMultiScale(gray, 1.1, 4)
    models = ["VGG-Face"]  # Hanya menggunakan model VGG-Face
    name = "Unknonwn"
    matches = []
    face_names = []
    for known_face in known_faces:
        result = DeepFace.verify(img_path, known_face, model_name=models[0], enforce_detection=False)
        matches.append(result)
    
    for index,match in enumerate(matches):
        if match['verified']:
            first_match_index = index
            name = known_face_names[first_match_index]
    face_names.append(name)

    for (x, y, w, h), name in zip(face_location, face_names):
        # Menggambar kotak merah
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Menggambar label dan nama di dalam label
        cv2.rectangle(image, (x, y + h), (x + w, y + h + 35), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX

        # Menghitung lebar teks
        text_width, _ = cv2.getTextSize(name, font, 0.8, 2)[0]  # Access only the first element (width)

        # Menghitung koordinat x untuk memposisikan teks di tengah
        text_x = x + int(w // 2) - int(text_width // 2)  # Convert to integer for floor division

        # Menampilkan nama di tengah label
        cv2.putText(image, name, (text_x, y + h + 25), font, 0.8, (255, 255, 255), 2)
    
    return image,name

# Fungsi untuk menyimpan gambar ke database
def save_image_to_db(image, name):
    # Mengkonversi gambar ke format binary
    _, encoded_image = cv2.imencode('.jpg', image)
    binary_image = encoded_image.tobytes()

    # SQL query untuk menyisipkan data
    sql_query = "INSERT INTO hasil_vgg (name, image) VALUES (%s, %s)"
    data_tuple = (name, binary_image)

    # Eksekusi query
    cursor.execute(sql_query, data_tuple)
    db.commit()