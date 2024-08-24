import os
import json
import cv2 as cv
import numpy as np
from config import Config

def show_detection_result(index=0):
    with open("models/coco_names.txt", "r") as f:
        class_names = [line.strip() for line in f.readlines()]

    with open(Config.MAIN_PATH+"detection_result.json", "r") as file:
        origin_data = json.load(file)
        data = origin_data[index]

    img_path = os.path.join(Config.MAIN_PATH, 'photos', data["date"], data["file_name"])
    img = cv.imread(img_path)
    
    # 클래스별 색상 랜덤 생성
    np.random.seed(0xC0FFEE)
    colors = np.random.uniform(0, 255, size=(len(class_names), 3))

    # detection 결과 GUI 시각화
    detection_data = data["detection_result"]
    obj_count = len(detection_data["bouding_box"])

    for i in range(obj_count):
        x1, y1, x2, y2 = detection_data["bouding_box"][i]
        conf = detection_data["confidence"][i]
        class_id = detection_data["class_id"][i]

        label = f"{class_names[class_id]}:{conf:.2f}"
        cv.rectangle(img, (x1, y1), (x2, y2), colors[class_id], 2)
        cv.putText(img, label, (x1, y1-5), cv.FONT_HERSHEY_PLAIN, 1.5, colors[class_id], 2)
    
    text = f"Number of objects: {obj_count}"
    cv.putText(img, text, (30, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv.imshow("detection result", img)

    cv.waitKey()
    cv.destroyAllWindows()


show_detection_result(index=-1)