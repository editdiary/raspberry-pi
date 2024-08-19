from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
import os
from .config import Config

app = Flask(__name__)

# 사진 저장 경로
upload_folder = Config.FILE_PATH
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
@app.route('/')
def index():
    return 'Welcome to the File Upload Server!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    return 'File uploaded successfully', 200

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host=Config.HOST_IP, port=Config.PORT_NUMBER)
