import cv2 as cv
import numpy as np

def detect_objects(img_path, min_confidence=0.4):
    model, output_layers, class_names = _construct_yolo_v3()        # YOLO 모델 생성
    
    img = cv.imread(img_path)

    # COCO dataset에서 동물 class만 추출
    res = _yolo_detect(img, model, output_layers, min_confidence)

    # class별 객체 수 count
    object_count = {}
    for i in range(len(res)):
        object_name = class_names[res[i][-1]]
        print(object_name)
        if object_name in object_count:
            object_count[object_name] += 1
        else:
            object_count[object_name] = 1
    
    print(object_count)

    # 객체 탐지 결과 bounding box 및 label 표시 + GUI로 표시
    np.random.seed(42)
    colors = np.random.uniform(0, 255, size=(len(class_names), 3))  # 클래스별 색상 랜덤 생성

    for i in range(len(res)):
        x1, y1, x2, y2, confidence, id = res[i]
        label = f"{class_names[id]}:{confidence:.2f}"
        cv.rectangle(img, (x1, y1), (x2, y2), colors[id], 2)
        cv.putText(img, label, (x1, y1-5), cv.FONT_HERSHEY_PLAIN, 1.5, colors[id], 2)

    text = f"Number of objects: {len(res)}"
    cv.putText(img, text, (30, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv.imshow("YOLOv3-spp", img)

    cv.waitKey()
    cv.destroyAllWindows()

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
    indexes = cv.dnn.NMSBoxes(box, conf, min_confidence, 0.5)
    objects = [box[i]+[conf[i]]+[id[i]] for i in range(len(box)) if i in indexes]
    return objects


detect_objects("imgs/horse.jpg")