from flask import Flask, request
import os
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    main_path = app.config['MAIN_PATH']

    save_path = os.path.join(main_path, 'photos/')
    if 'photos' not in os.listdir(main_path):
        os.mkdir(save_path)
    
    file.save(save_path + file.filename)
    return "File successfully uploaded", 200