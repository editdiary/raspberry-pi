from rpi_def import capture_save, run_scheduler
from picamera2 import Picamera2
import schedule
import logging

# 로깅 설정
logging.basicConfig(filename='/YOUR_SAVE_PATH/camera_log.txt',
                    level=logging.INFO, format='%(asctime)s - %(message)s')

# Picamera2의 로그 레벨을 ERROR로 설정하여 불필요한 로그 제거
logging.getLogger('picamera2').setLevel(logging.ERROR)

cam = Picamera2()
config = cam.create_still_configuration()
cam.configure(config)

# 정각을 기준으로 30분마다 사진 촬영 스케줄링
for minute in range(0, 60, 30):
    schedule.every().hour.at(f":{minute:02d}").do(lambda: capture_save(camera=cam))

# 메인 루프 실행
if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logging.info("프로그램이 사용자에 의해 종료되었습니다.")
    except Exception as e:
        logging.error(f"예기치 못한 오류로 프로그램이 종료됨: {str(e)}")
    finally:
        cam.close()