import os
from flask import Flask, render_template, request, send_from_directory, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
from deepface_pred import predict as pred
from check import absen
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skripsi-3"
)

app = Flask(__name__)

app.secret_key = 'asoy'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'uploads/images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
    execution_path = target
    print(execution_path)
    image,name = pred(os.path.join(execution_path, filename))
    absen(name)
    print(image.shape)
    print('predicted')
    predicted_path = os.path.join(APP_ROOT,'uploads/predicted_images')
    predicted_image = cv2.imwrite(os.path.join(predicted_path,  "flask"+filename), image)
    print('wrote out the image')
    print('flask'+filename)
    return render_template("result.html", original_image_name=filename ,predicted_image_name="flask"+filename)

@app.route('/upload/ori/<filename_ori>')
def original_image(filename_ori):
     return send_from_directory("uploads/images", filename_ori)

@app.route('/upload/pred/<filename_pred>')
def predicted_image(filename_pred):
    return send_from_directory("uploads/predicted_images", filename_pred)

@app.route('/cek-absen')
def cek_absen():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM nama_tabel")
    data = cursor.fetchall()
    return render_template('cek-absen.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)