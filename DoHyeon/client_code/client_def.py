# 필요 패키지 import
import os
import time
import logging
import requests
import schedule
import cv2 as cv
from picamera2 import Picamera2
from config import Config

#-----------------------------------사진 촬영/저장/전송-----------------------------------

def capture_save(camera, output_size=(1024, 768), change_size=False):
    try:
        # 사진 촬영 및 크기 조정
        img = _img_capture(camera)

        # change_size=True인 경우 openCV를 이용하여 이미지 크기 조정
        if change_size:
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)        # OpenCV에서 사용하는 BGR 형식으로 변환
            img = cv.resize(img, output_size)

        # 이미지 폴더 생성 생성 및 파일 저장
        img_path = _img_save(img, Config.PHOTO_SAVE_PATH)
        logging.info(f"사진 저장 완료: {time.strftime('%Y%m%d_%H%M%S')}")

        # 이미지 전송
        _send_img(img_path)

    except Exception as e:
        logging.error(f"사진 촬영 중 오류 발생: {e}")

def _img_capture(camera):
    # 전체 해상도로 카메라 구성 및 시작
    camera.start()
    time.sleep(2)       # 카메라 초기화 대기

    img = camera.capture_array()    # 이미지 캡처(resize를 위해 numpy 배열로 저장)
    #img = cv.flip(img, 0)           # 이미지 상하반전
    
    camera.stop()

    return img

def _img_save(img, main_path):
    # 사진을 저장할 폴더가 없다면 생성
    img_folder = os.path.join(main_path, 'photos')
    if 'photos' not in os.listdir(main_path):
        os.mkdir(img_folder)

    # 사진을 날짜별 폴더에 저장(없으면 폴더 생성)
    save_path = os.path.join(img_folder, time.strftime('%Y%m%d'))
    if time.strftime('%Y%m%d') not in os.listdir(img_folder):
        os.mkdir(save_path)

    img_name = f"rsp_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
    cv.imwrite(os.path.join(save_path, img_name), img)

    return os.path.join(save_path, img_name)

def _send_img(img_path):
    try:
        SEND_URL = f"http://{Config.HOST_IP}:{Config.PORT_NUMBER}/upload"
        with open(img_path, 'rb') as img_file:
            files = {'image': img_file}
            response = requests.post(SEND_URL, files=files)
            response.raise_for_status()     # 오류가 발생하면 예외를 발생시킴
            logging.info(f"이미지 전송 성공: {img_path}")
    except Exception as e:
        logging.error(f"이미지 전송 실패: {e}")

#-----------------------------------스케줄 세팅-----------------------------------

# CPU 사용 최적을 위한 scheduler 실행 함수
def run_scheduler():
    while True:
        now = time.time()                   # 현재 시간을 가져옴
        next_run = schedule.next_run()      # 다음 작업까지의 시간을 계산

        if next_run is None:                # 예약된 작업이 없으면 1분 동안 대기
            time.sleep(60)
            continue

        # datetime 객체를 Unix timestamp로 변환
        next_run_timestamp = next_run.timestamp()
        
        # 다음 작업까지의 대기 시간을 계산
        wait_time = max(next_run_timestamp - now, 0)

        # 다음 작업까지 대기, 최대 대기 시간은 60초로 제한
        time.sleep(min(wait_time, 60))

        schedule.run_pending()