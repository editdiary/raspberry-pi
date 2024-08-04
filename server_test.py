# 서버 코드
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    save_path = '{Path to save the file}'
    file.save(save_path + file.filename)
    return "File successfully uploaded", 200

if __name__ == '__main__':
    app.run(host='{0.0.0.0 #Server IP}', port='{#Port_number}')