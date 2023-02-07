import socket

IP_1 = '127.0.0.1'
PORT1 = 8030

try:
    # TCP 소켓 생성 /서버2 연결
    server3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server3.bind((IP_1, PORT1))
    server3.listen()
    print('~~server3 연결성공~~')
    server3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 서버 1 연결
    server1, addr = server3.accept()

    print("연결 :", addr)

    while True:
        num_value = []
        result = 0

        # 서버1 -> 메시지 수신
        recvData = server1.recv(1024)
        recvData = recvData.decode()

        print("서버1 -> 계산식", addr, ':', recvData)

        if ("exit" in recvData) or "" == recvData:
            print("~~서버3 종료~~")
            break

        if '+' in recvData:
            num_value = recvData.split('+')
            result = float(num_value[0]) + float(num_value[1])
            result = str(result)
            server1.sendall(result.encode('utf-8'))

        elif '-' in recvData:
            num_value = recvData.split('-')
            result = float(num_value[0]) - float(num_value[1])
            result = str(result)
            server1.sendall(result.encode('utf-8'))


except:
    server1.close()
    server3.close()

server1.close()
server3.close()
