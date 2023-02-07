import socket

# 서버1의 IP주소, 포트 번호
IP = '127.0.0.1'
port = 8010

try:
    # 서버용 TCP 소켓 생성
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((IP, port))
    print("~~서버1 접속완료~~")

    while True:
        print("exit 입력시 프로그램 종료!")
        Expression = input("계산식을 입력하세요: ")

        # Expression 소문자 변환--> checkinput에 저장.
        checkinput = Expression.lower()
        if 'exit' in checkinput:
            clientSocket.sendall(checkinput.encode('utf-8'))
            print("client 프로그램을 종료합니다.")
            break

        # 서버1에게 사용자로부터 입력받은 메시지 송신
        clientSocket.sendall(Expression.encode('utf-8'))

        recvData = clientSocket.recv(1024)
        result = recvData.decode()

        if result == "N":
            print("계산식이 잘못되었습니다! 다시 입력하세요.")
            continue

        print("결과값: ", float(result), "\n")

except:
    clientSocket.close()

clientSocket.close()
