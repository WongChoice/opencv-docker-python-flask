#app.py
from flask import Flask, render_template, request
import cv2
import numpy as np
import io
from PIL import Image
import base64
import os

app = Flask(__name__)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.realpath(__file__ + "\\.."))

# Specify the templates directory path
app.config['TEMPLATE_FOLDER'] = os.path.join(script_dir, 'templates')

# Load the face detection cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Retrieve the uploaded image from the form
    uploaded_image = request.files['image'].read()
    nparr = np.fromstring(uploaded_image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect faces in the image
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Convert the processed image to a base64-encoded string for display in HTML
    _, buffer = cv2.imencode('.jpg', img)
    processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

    return render_template('result.html', processed_image_base64=processed_image_base64)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
