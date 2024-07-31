from socket import *
from threading import *
import time
import struct

'''
 0  메세지인지(m),             파일이면(f)
 1  1:1메세지 : p, 1:n메세지:n  파일이름전송:s 데이터:d 데이터전송끝:e
 2
 3
 
 4   크기 고정
 5
 6
 7
'''
fmt = "=4si"
fmt_size = struct.calcsize(fmt)



def send(sock):
    while True:
        sendData = input('>')
        sock.send(sendData.encode('utf-8'))

def receive(sock):
    while True:
        recv_data_header = sock.recv(8)
        header = sruct.unpack(fmt, recv_data_header)
        recvData = sock.recv(header[1])
        
        if header[0][0] == b'm':
            if header[0][1] == b'p':
                print('개인용 메세지', recvData.decode())
            elif header[0][1] == b'n':
                print('1:n메세지 수신', recvData.decode())
        elif header[0][0] == b'f':
            
            
            
            
            
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