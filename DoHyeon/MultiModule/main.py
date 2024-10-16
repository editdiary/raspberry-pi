import os
import time
from config import Config
import RPi.GPIO as gp
from picamera2 import Picamera2

# 카메라별 GPIO는 설명서를 참고하여 설정
adapter_info = {  
    "A" : {   
        "i2c_cmd":"i2cset -y 1 0x70 0x00 0x04",
        "gpio_sta":[0,0,1],
    }, "B" : {
        "i2c_cmd":"i2cset -y 1 0x70 0x00 0x05",
        "gpio_sta":[1,0,1],
    }, "C" : {
        "i2c_cmd":"i2cset -y 1 0x70 0x00 0x06",
        "gpio_sta":[0,1,0],
    },"D" : {
        "i2c_cmd":"i2cset -y 1 0x70 0x00 0x07",
        "gpio_sta":[1,1,0],
    }
}

# GPIO 설정 (모듈의 Pin output이 7, 11, 12번이다)
def setup_gpio():
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)
    gp.setup(7, gp.OUT)
    gp.setup(11, gp.OUT)
    gp.setup(12, gp.OUT)

def _select_channel(channel):
    gpio_sta = adapter_info[channel]["gpio_sta"]
    os.system(adapter_info[channel]["i2c_cmd"])
    gp.output(7, gpio_sta[0])
    gp.output(11, gpio_sta[1])
    gp.output(12, gpio_sta[2])
    time.sleep(0.5)

def capture_image(channel):
    _select_channel(channel)
    filename = f"image_camera{channel}.jpg"

    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration(main={"size": (1920, 1080)}))
    picam2.start()

    time.sleep(3)

    picam2.capture_file(Config.MAIN_PATH + filename)
    picam2.close()

    print(f"Captured image from camera {channel}: {filename}")


def main():
    setup_gpio()

    try:
        for channel in adapter_info.keys():
            capture_image(channel)
            time.sleep(0.5)
    finally:
        gp.cleanup()

if __name__ == "__main__":
    main()
