import os
import time
from config import Config
from flask import Flask, request
from detect_model import _detect_objects

app = Flask(__name__)
#app.config.from_object(Config)

@app.route('/upload', methods=['POST'])
def img_processing():
    # 전송된 이미지가 없을 경우 에러 메시지 반환
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']

    # 이미지는 전송되었지만 파일 이름이 없을 경우 에러 메시지 반환
    if file.filename == '':
        return "No selected file", 400

    # 이미지 저장
    save_path = _img_save(file, Config.MAIN_PATH)

    # !객체 탐지(Object detection) - 구현 필요
    detection_result = _detect_objects(save_path)

    return "File successfully uploaded", 200

def _img_save(img, main_path):
    # 사진을 저장할 폴더가 없다면 생성
    img_folder = os.path.join(main_path, 'photos')
    if 'photos' not in os.listdir(main_path):
        os.mkdir(img_folder)

    # 사진을 날짜별 폴더에 저장(없으면 폴더 생성)
    save_path = os.path.join(img_folder, time.strftime('%Y%m%d'))
    if time.strftime('%Y%m%d') not in os.listdir(img_folder):
        os.mkdir(save_path)
    
    img_path = os.path.join(save_path, img.filename)
    img.save(img_path)

    return img_path