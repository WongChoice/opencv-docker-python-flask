# app.py
from flask import Flask, render_template, request
import cv2
import numpy as np
import io
from PIL import Image
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Retrieve the uploaded image from the form
    uploaded_image = request.files['image'].read()
    nparr = np.fromstring(uploaded_image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process the image with OpenCV (e.g., apply a filter)
    # For this example, we'll just convert it to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert the processed image to a base64-encoded string for display in HTML
    _, buffer = cv2.imencode('.jpg', gray_image)
    gray_image_base64 = base64.b64encode(buffer).decode('utf-8')

    return render_template('result.html', gray_image_base64=gray_image_base64)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
