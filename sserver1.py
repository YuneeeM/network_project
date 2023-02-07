import socket

clientIP = '127.0.0.1'
clientport = 8010

server2IP = '127.0.0.1'
server2port = 8020

server3IP = '127.0.0.1'
server3port = 8030

try:
    # TCP 소켓 생성 / 클라이언트 연결
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server1.bind((clientIP, clientport))

    server1.listen()
    print('~~server1 연결~~')
    server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2.connect((server2IP, server2port))

    server3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server3.connect((server3IP, server3port))

    client_Socket, addr = server1.accept()

    print("클라이언트 ->  접속 완료: ", addr)

    while True:
        result = 0
        recvData = client_Socket.recv(1024)

        # 서버2, 서버3에 exit 송신 - 서버1 종료.
        recvData = recvData.decode()
        if recvData == 'exit':
            server2.sendall(recvData.encode('utf-8'))
            server3.sendall(recvData.encode('utf-8'))
            print("~~서버1 종료~~")
            break

        # "*" 또는 "/" 이면 서버2로 값을 전송
        if ("*" in recvData) or ("/" in recvData):
            print("서버3 --> 계산식: ", recvData)
            server2.sendall(recvData.encode('utf-8'))
            result = server2.recv(1024)
            result = result.decode()
            print("서버2 --> 결과 값: ", result)

        # "+" 또는 "-" 이면 서버3로 값을 전송
        elif ("+" in recvData) or ("-" in recvData):
            print("서버3 --> 계산식: ", recvData)
            server3.sendall(recvData.encode('utf-8'))
            result = server3.recv(1024)
            result = result.decode()
            print("서버3 --> 결과 값: ", result)

        else:
            print("계산식 에러")
            result = "N"

        # 서버2 or 서버3 결과값 --> 클라이언트로 전송.
        client_Socket.sendall(result.encode('utf-8'))


except:
    client_Socket.close()
    server1.close()
    server2.close()
    server3.close()

client_Socket.close()
server1.close()
server2.close()
server3.close()
