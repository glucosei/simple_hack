import socket
import pyautogui
import pickle
import time

# 서버 주소와 포트
server_address = ( '192.168.123.101', 1235)

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect(server_address)

while True:
    # 화면 캡처
    screenshot = pyautogui.screenshot()

    # 캡처된 이미지를 바이트로 변환
    screenshot_bytes = pickle.dumps(screenshot)

    # 이미지 크기 전송
    image_size = len(screenshot_bytes)
    client_socket.sendall(image_size.to_bytes(4, byteorder='big'))

    # 이미지 데이터 전송
    client_socket.sendall(screenshot_bytes)

    time.sleep(10)
    
# 소켓 닫기
client_socket.close()
