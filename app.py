import os
from flask import Flask, render_template, request, send_from_directory, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
from deepface_pred import predict as pred, save_image_to_db

app = Flask(__name__)

app.secret_key = 'asoy'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'uploads/images/')
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
    execution_path = target
    image,name = pred(os.path.join(execution_path, filename))
    save_image_to_db(image,name)
    predicted_path = os.path.join(APP_ROOT,'uploads/predicted_images')
    predicted_image = cv2.imwrite(os.path.join(predicted_path,  "flask"+filename), image)
    print('flask'+filename)
    return render_template("result.html", original_image_name=filename ,predicted_image_name="flask"+filename)

@app.route('/upload/ori/<filename_ori>')
def original_image(filename_ori):
     return send_from_directory("uploads/images", filename_ori)

@app.route('/upload/pred/<filename_pred>')
def predicted_image(filename_pred):
    return send_from_directory("uploads/predicted_images", filename_pred)

if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=8080)