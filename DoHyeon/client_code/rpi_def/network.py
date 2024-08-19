import requests
import logging
from .config import Config

def send_img(img_path):
    try:
        SEND_URL = f"http://{Config.HOST_IP}:{Config.PORT_NUMBER}/upload"
        with open(img_path, 'rb') as img_file:
            files = {'image': img_file}
            response = requests.post(SEND_URL, files=files)
            response.raise_for_status()     # 오류가 발생하면 예외를 발생시킴
            logging.info(f"이미지 전송 성공: {img_path}")
    except Exception as e:
        logging.error(f"이미지 전송 실패: {e}")