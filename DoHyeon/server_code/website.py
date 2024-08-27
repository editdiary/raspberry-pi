import logging
from config import Config
from flask import Flask, request
from detection_model import detect_objects
from save_def import img_save, save_detection_to_json

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def img_processing():
    # 전송된 이미지가 없을 경우 에러 메시지 반환
    if 'image' not in request.files:
        logging.error("No file part")
        return "No file part", 400

    file = request.files['image']

    # 이미지는 전송되었지만 파일 이름이 없을 경우 에러 메시지 반환
    if file.filename == '':
        logging.error("No selected file")
        return "No selected file", 400

    # 이미지 저장
    img_name, img_path = img_save(file, Config.MAIN_PATH)

    # 객체 탐지(Object detection) - 탐지 결과(box, conf, class_id)와 객체 수 반환
    try:
        detection_res, object_counts = detect_objects(img_path, min_confidence=0.4)

        # 객체 탐지 결과를 json 파일로 저장
        json_path = Config.MAIN_PATH + "detection_result.json"
        save_detection_to_json(img_name, detection_res, object_counts, json_path)

        return "File successfully detected and saved", 200

    except ValueError as e:
        logging.error(f"Error occurred during object detection: {str(e)}")
        return {str(e)}, 400

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}", 500