from flask import Flask
from .config import Config
app = Flask(__name__)


@app.route('/')
def home():
    return 'This is Home!'


@app.route('/mypage')
def mypage():
    return 'This is My Page!'


if __name__ == '__main__':
    app.run(Config.HOST_IP, port=Config.PORT_NUMBER, debug=True)