import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from deepface import DeepFace
import mysql.connector
import numpy as np
import cv2

face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skripsi-3"
)

cursor = db.cursor()
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


# print(known_faces)
# print(type(known_faces[0]))
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


# hasil,name = vgg("./db-test/Fahmi.jpg")
# print(name)

# # Display the image
# cv2.imshow("Image", hasil)
 
# # Wait for the user to press a key
# cv2.waitKey(0)
 
# # Close all windows
# cv2.destroyAllWindows()
