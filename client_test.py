# 클라이언트 코드
import requests

SERVER_URL = 'http://{0.0.0.0 #Server IP}:{#Port number}/upload'

# 이미지 파일 전송
img_path = '{Path to send the file}'
with open(img_path, 'rb') as img_file:
    files = {'image': img_file}
    response = requests.post(SERVER_URL, files=files)
print("Server response:", response.text)
