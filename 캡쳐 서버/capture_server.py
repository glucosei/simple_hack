# -*- coding: euc-kr -*-
import socket
import pickle
from PIL import Image
from datetime import datetime
import getpass


def start():
    # ���� �ּҿ� ��Ʈ
    server_address = ('192.168.123.101', 1235)

    # ���� ����
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ���� ���ε�
    server_socket.bind(server_address)

    # Ŭ���̾�Ʈ�� ���� ���
    server_socket.listen(1)
    print("Ŭ���̾�Ʈ�� ������ ��ٸ��� ��...")

    # Ŭ���̾�Ʈ ���� ����
    client_socket, client_address = server_socket.accept()
    print("Ŭ���̾�Ʈ�� ����Ǿ����ϴ�:", client_address)

    while True:
        # �̹��� ũ�� ����
        image_size_bytes = client_socket.recv(4)
        image_size = int.from_bytes(image_size_bytes, byteorder='big')

        # �̹��� ������ ����
        screenshot_bytes = b''
        while len(screenshot_bytes) < image_size:
            data = client_socket.recv(image_size - len(screenshot_bytes))
            if not data:
                break
            screenshot_bytes += data

        # ����Ʈ�κ��� �̹����� ��ȯ
        screenshot = pickle.loads(screenshot_bytes)

        # �̹��� ���
        screenshot.show()

        # ���� �ð��� ������� �̹��� ���� �̸� ����
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"captured_image_{current_time}.jpg"

        # �̹��� ����
        screenshot.save(file_name, 'JPEG')
        print(f"�̹��� ����: {file_name}")

    # ���� �ݱ�
    client_socket.close()
    server_socket.close()

pw='glucose'
upw = getpass.getpass("pw: ")
if pw==upw:
    start()
else:
    print('�߸��� ��й�ȣ')
