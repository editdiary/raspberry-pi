from server_def import app
from server_def.config import Config

if __name__ == '__main__':
    app.run(host=Config.HOST_IP, port=Config.PORT_NUMBER)