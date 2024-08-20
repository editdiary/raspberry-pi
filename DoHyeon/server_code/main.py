from website import app
from config import Config

if __name__ == '__main__':
    app.run(host=Config.HOST_IP, port=Config.PORT_NUMBER)