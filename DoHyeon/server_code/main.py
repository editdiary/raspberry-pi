import logging
from website import app
from config import Config

# logging 설정
log_file = Config.MAIN_PATH + "server.log"
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s] %(message)s')

# Flask 관련 로거의 레벨을 ERROR로 설정하여 불필요한 로그 출력 방지
logging.getLogger('werkzeug').setLevel(logging.ERROR)


if __name__ == '__main__':
    logging.info("Flask server start")

    # Flask 웹 서버 실행
    app.run(host=Config.HOST_IP, port=Config.PORT_NUMBER)