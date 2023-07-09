# -*- coding: euc-kr -*-
import socket
import pickle
from PIL import Image
from datetime import datetime
import getpass


def start():
    # 서버 주소와 포트
    server_address = ('192.168.123.101', 1235)

    # 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 서버 바인딩
    server_socket.bind(server_address)

    # 클라이언트의 연결 대기
    server_socket.listen(1)
    print("클라이언트의 연결을 기다리는 중...")

    # 클라이언트 연결 수락
    client_socket, client_address = server_socket.accept()
    print("클라이언트가 연결되었습니다:", client_address)

    while True:
        # 이미지 크기 수신
        image_size_bytes = client_socket.recv(4)
        image_size = int.from_bytes(image_size_bytes, byteorder='big')

        # 이미지 데이터 수신
        screenshot_bytes = b''
        while len(screenshot_bytes) < image_size:
            data = client_socket.recv(image_size - len(screenshot_bytes))
            if not data:
                break
            screenshot_bytes += data

        # 바이트로부터 이미지로 변환
        screenshot = pickle.loads(screenshot_bytes)

        # 이미지 출력
        screenshot.show()

        # 현재 시간을 기반으로 이미지 파일 이름 생성
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"captured_image_{current_time}.jpg"

        # 이미지 저장
        screenshot.save(file_name, 'JPEG')
        print(f"이미지 저장: {file_name}")

    # 소켓 닫기
    client_socket.close()
    server_socket.close()

pw='glucose'
upw = getpass.getpass("pw: ")
if pw==upw:
    start()
else:
    print('잘못된 비밀번호')
