import os
import time
import json
import logging

# 이미지 저장 함수
def img_save(img, main_path):
    # 사진을 저장할 폴더가 없다면 생성
    img_folder = os.path.join(main_path, 'photos')
    if 'photos' not in os.listdir(main_path):
        os.mkdir(img_folder)

    # 사진을 날짜별 폴더에 저장(없으면 폴더 생성)
    save_path = os.path.join(img_folder, time.strftime('%Y%m%d'))
    if time.strftime('%Y%m%d') not in os.listdir(img_folder):
        os.mkdir(save_path)
    
    img_path = os.path.join(save_path, img.filename)
    img.save(img_path)

    logging.info(f"File successfully saved: {img.filename}")

    return img.filename, img_path


# 데이터 저장 함수(json)
def save_detection_to_json(img_name, detection_result, object_counts, json_file):
    # 기존 파일이 있다면 읽어오기, 없으면 새 리스트 생성
    try:
        with open(json_file, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # 새로운 데이터 추가
    total_data = {
        "date": time.strftime('%Y%m%d'),
        "time": time.strftime('%H:%M:%S'),
        "file_name": img_name,
        "object_counts": object_counts,
        "detection_result": detection_result
    }
    existing_data.append(total_data)

    # json 파일로 저장
    with open(json_file, 'w') as file:
        json.dump(existing_data, file, indent=4)
    
    logging.info(f"Detection result successfully saved: detection_result.json")


# # 데이터 저장 함수(csv)
# def save_detection_to_csv(img_name, detection_result, csv_file):
#     # 기존에 csv 파일이 있는지 확인
#     try:
#         df_existing = pd.read_csv(csv_file)
#     except FileNotFoundError:
#         df_existing = pd.DataFrame()

#     # detection 결과를 df로 변환 후 기존의 파일에 합치기
#     df_detection = pd.DataFrame([{
#         "date": time.strftime('%Y%m%d'),
#         "time": time.strftime('%H:%M:%S'),
#         "file_name": img_name,
#         **detection_result
#     }])
#     df_combined = pd.concat([df_existing, df_detection], axis=0, ignore_index=True)
#     df_combined.fillna(0, inplace=True)     # NaN 값은 0으로 대체

#     # csv 파일로 저장
#     df_combined.to_csv(csv_file, index=False)