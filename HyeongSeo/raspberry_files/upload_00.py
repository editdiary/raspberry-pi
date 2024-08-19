import requests
import os
import time
from datetime import datetime, timedelta
from .config import Config

server_ip = Config.SERVER_IP
server_port = Config.PORT_NUMBER
photo_dir = Config.SAVE_PATH

def find_latest_photo():
    files = os.listdir(photo_dir)
    print(f"Found files: {files}")  # 디버깅용 출력
    paths = [os.path.join(photo_dir, file) for file in files if file.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not paths:
        return None
    
    latest_file = max(paths, key=os.path.getmtime)
    print(f"Latest file: {latest_file}")  # 디버깅용 출력
    return os.path.basename(latest_file)

def upload_photo():
    filename = find_latest_photo()
    
    if filename:
        url = f'http://{server_ip}:{server_port}/upload'
        file_path = os.path.join(photo_dir, filename)
        print(f"Uploading file: {file_path}")  # 디버깅용 출력
        
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (filename, file)}
                response = requests.post(url, files=files)
            
            if response.status_code == 200:
                print(f"Successfully uploaded {filename} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"Failed to upload {filename}: {response.status_code}")
        except Exception as e:
            print(f"Error occurred while uploading: {e}")
    else:
        print("No files found to upload.")

def wait_for_next_hour():
    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    time_to_wait = (next_hour - now).total_seconds()
    print(f"Waiting for {time_to_wait} seconds until the next hour...")  # 디버깅용 출력
    time.sleep(time_to_wait)

while True:
    upload_photo()
    wait_for_next_hour()
