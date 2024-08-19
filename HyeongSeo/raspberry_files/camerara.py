from picamera2 import Picamera2
from time import sleep
from datetime import datetime
import os
import cv2
from .config import Config

# 카메라 초기화
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# 사진 저장 디렉토리 설정
SAVE_DIR = Config.SAVE_PATH

# 디렉토리가 없으면 생성
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def take_photo():
    # 현재 날짜와 시간을 파일명에 포함
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"strawberry_{current_time}.jpg"
    file_path = os.path.join(SAVE_DIR, file_name)
    
    # 사진 촬영
    picam2.capture_file(file_path)
    
    # 사진을 상하 반전시키기
    image = cv2.imread(file_path)
    flipped_image = cv2.flip(image, 0)  # 상하 반전 (0: x축 방향)

    # 상하 반전된 사진 저장
    flipped_file_path = os.path.join(SAVE_DIR, f"flipped_{file_name}")
    cv2.imwrite(flipped_file_path, flipped_image)
    
    print(f"Photo saved: {file_path}")
    print(f"Flipped photo saved: {flipped_file_path}")

# 메인 루프
try:
    print("Starting photo capture schedule. Press CTRL+C to exit.")
    while True:
        take_photo()
        # 다음 촬영 시간을 1시간 후로 설정
        sleep(3600)
except KeyboardInterrupt:
    print("Photo capture stopped.")
finally:
    picam2.stop()
