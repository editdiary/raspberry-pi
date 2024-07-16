from picamera2 import Picamera2
import time
from PIL import Image
import schedule
import os
import logging
import gc

# 로깅 설정
logging.basicConfig(filename='/home/ldh/Desktop/camera_test/camera_log.txt',
                    level=logging.INFO, format='%(asctime)s - %(message)s')

# Picamera2의 로그 레벨을 ERROR로 설정하여 불필요한 로그 제거
logging.getLogger('picamera2').setLevel(logging.ERROR)

# Picamera2 객체 생성
camera = Picamera2()

# 사진을 캡처 후 크기 조정
def capture_and_resize(output_size=(1024, 768)):
    try:
        # 전체 해상도로 카메라 구성 및 시작
        config = camera.create_still_configuration()
        camera.configure(config)
        
        camera.start()
        time.sleep(2)  # 카메라 초기화 대기

        # 이미지 캡처
        full_img = camera.capture_array()
        
        # NumPy 배열을 PIL Image로 변환 및 해상도 조정
        with Image.fromarray(full_img) as img:
            img_resized = img.resize(output_size)
        
            # 파일 저장
            img_root = "/home/ldh/Desktop/camera_test/photos/"
            resized_filename = f"resized_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
            img_resized.save(os.path.join(img_root, resized_filename))
        
        logging.info(f"사진 저장 완료: {resized_filename}")
    
    except Exception as e:
        logging.error(f"사진 촬영 중 오류 발생: {e}")
    
    finally:
        camera.stop()
        # 메모리 관리를 위해 명시적으로 큰 객체 삭제
        del full_img
        gc.collect()

# 정각을 기준으로 10분마다 사진 촬영 스케줄링
for minute in range(0, 60, 2):      # !test로 2분 간격으로 설정
    schedule.every().hour.at(f":{minute:02d}").do(capture_and_resize)

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


# 메인 루프 실행
if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logging.info("프로그램이 사용자에 의해 종료되었습니다.")
    except Exception as e:
        logging.error(f"예기치 못한 오류로 프로그램이 종료됨: {str(e)}")
    finally:
        camera.close()