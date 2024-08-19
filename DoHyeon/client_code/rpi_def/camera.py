from picamera2 import Picamera2
import time
import cv2 as cv
import os
import logging
from .network import send_img

def capture_save(camera, output_size=(1024, 768), change_size=False):
    # 사진 찍기
    try:
        img = _capture_resize(camera, output_size, change_size)

        ## ! 함수로 만들자(파일 생성 및 저장)
        # main 코드의 경로
        main_path = os.path.dirname(os.path.abspath(__file__))

        # 사진 폴더가 없다면 생성
        img_root = os.path.join(main_path, 'photos')
        if 'photos' not in os.listdir(main_path):
            os.mkdir(img_root)

        # 사진을 저장할 폴더(날짜)가 없을 경우 생성
        save_path = os.path.join(img_root, time.strftime('%Y%m%d'))
        if time.strftime('%Y%m%d') not in os.listdir(img_root):
            os.mkdir(save_path)

        photo_name = f"img_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
        img_path = os.path.join(save_path, photo_name)
        img.save(img_path)

        logging.info(f"사진 저장 완료: {photo_name}")

        # 이미지 전송
        send_img(img_path)

    except Exception as e:
        logging.error(f"사진 촬영 중 오류 발생: {e}")


def _capture_resize(camera, output_size, change_size):
    # 전체 해상도로 카메라 구성 및 시작
    camera.start()
    time.sleep(2)  # 카메라 초기화 대기

    # 이미지 캡처
    img = camera.capture_image()

    if change_size:
        # openCV를 이용한 이미지 크기 조정
        img = cv.resize(img, output_size)
    
    camera.stop()

    return img