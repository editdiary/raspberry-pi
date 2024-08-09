import time
import schedule

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