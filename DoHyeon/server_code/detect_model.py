import cv2 as cv
import numpy as np

def detect_objects(img_path, min_confidence=0.4):
    model, output_layers, class_names = _construct_yolo_v3()        # YOLO 모델 생성
    
    img = cv.imread(img_path)

    # 이미지 전송은 성공했으나 정상적으로 읽어오지 못했을 경우 에러 반환
    if img is None:
        raise ValueError("File is successfully uploaded, but could not read the image.")
    
    # COCO dataset에서 동물 class만 추출
    detection_res = _yolo_detect(img, model, output_layers, min_confidence)

    # class별 객체 수 count
    object_counts = {}
    for i in range(len(detection_res["class_id"])):
        object_name = class_names[detection_res["class_id"][i]]
        if object_name in object_counts:
            object_counts[object_name] += 1
        else:
            object_counts[object_name] = 1

    return detection_res, object_counts

# YOLO 모델 생성
def _construct_yolo_v3():
    # coco_names에서 class 이름 읽기
    with open("models/coco_names.txt", "r") as f:
        class_names = [line.strip() for line in f.readlines()]

    # YOLO 모델 로드
    model = cv.dnn.readNet("models/yolov3-spp.weights", "models/yolov3-spp.cfg")

    # YOLO 모델의 출력 레이어 이름 가져오기(['yolo_82', 'yolo_94', 'yolo_106'])
    layer_names = model.getLayerNames()
    output_layers = [layer_names[i-1] for i in model.getUnconnectedOutLayers()]

    return model, output_layers, class_names

# YOLO 모델을 이용하여 객체 탐지
def _yolo_detect(img, yolo_model, output_layers, min_confidence):
    # 이미지 크기 정보 확인
    height, width, channels = img.shape

    # 이미지 전처리(blob: Binary Large Object - 입력 이미지를 전처리하여 딥러닝 모델에 입력할 수 있는 형태로 변환된 4차원 배열)
    blob = cv.dnn.blobFromImage(img, 1.0/255, (608, 608), (0, 0, 0), swapRB=True, crop=False)
    yolo_model.setInput(blob)                       # YOLO 모델에 blob을 입력
    output3 = yolo_model.forward(output_layers)     # YOLO 모델의 forward 연산 수행(결과가 output_layers에 저장)

    # 객체 탐지 결과 추출
    box, conf, id = [], [], []
    for output in output3:
        for vec85 in output:
            # 모델의 출력 결과는 총 85차원(x, y, w, h, objectness score, class scores)
            scores = vec85[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # COCO dataset에서 동물 class만 추출
            # 14(bird), 15(cat), 16(dog), 17(horse), 18(sheep), 19(cow), 20(elephant), 21(bear), 22(zebra), 23(giraffe)
            animal_class = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            if (class_id in animal_class) and (confidence > min_confidence):
                # dection box 좌표 계산
                center_x, center_y = int(vec85[0]*width), int(vec85[1]*height)
                w, h = int(vec85[2]*width), int(vec85[3]*height)
                x, y = int(center_x - w/2), int(center_y - h/2)
                box.append([x, y, x+w, y+h])
                conf.append(float(confidence))
                id.append(class_id)

    # 비최대 억제(NMS) 수행 - 겹치는 box 제거
    indexes = cv.dnn.NMSBoxes(box, conf, min_confidence, 0.4)

    detection_res = {
        "bouding_box": [box[i] for i in range(len(box)) if i in indexes],
        "confidence": [conf[i] for i in range(len(box)) if i in indexes],
        "class_id": [int(id[i]) for i in range(len(box)) if i in indexes]
    }

    return detection_res