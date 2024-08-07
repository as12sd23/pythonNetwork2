from socket import *
from threading import *
import time

def send(sock):
    while True:
        sendData = input('>')
        sock.send(sendData.encode('utf-8'))

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('상대방 :', recvData.decode('utf-8'))

port = 8888
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print('%d번 포트로 접속 대기중...'%port)

connectionSock, addr = serverSock.accept()

print(str(addr), '에서 접속 완료')

sender = Thread(target = send, args = (connectionSock, ))
receiver = Thread(target = receive, args = (connectionSock, ))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass