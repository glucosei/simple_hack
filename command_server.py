import socket
import getpass

def start():
    # 서버 주소와 포트
    server_address = ('10.88.38.240', 1236)

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
        # 메시지 입력
        message = input("실행할 윈도우 명령어를 입력하세요: ")

        # 메시지 전송
        client_socket.sendall(message.encode())

        # 결과 수신
        result = client_socket.recv(4096).decode()

        # 결과 출력
        print("클라이언트로부터 받은 결과:")
        print(result)

    # 소켓 닫기
    client_socket.close()
    server_socket.close()

pw='glucose'
upw = getpass.getpass("pw: ")
if pw==upw:
    start()
else:
    print('잘못된 비밀번호')