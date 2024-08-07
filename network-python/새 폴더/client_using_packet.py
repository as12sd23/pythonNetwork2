from socket import *
from threading import *
import time
import struct
from tkinter import filedialog
import os

fmt = '=4si'
fmt_size = struct.calcsize(fmt)

FILE_READ_DATA = 1024
HEADER_SIZE = 8

def send(sock):
    while True:
        sendData = input('>')
        if sendData[0].lower() == 'm':  
            send_data_header = struct.pack(fmt, b'mp00', len(sendData.encode('utf-8')))
            sock.send(send_data_header + sendData.encode('utf-8'))
        elif sendData[0].lower() == 'f':
            filepath = filedialog.askopenfilename()
            filesize = os.path.getsize(filepath)
            filename = os.path.basename(filepath).encode('utf-8')
            filepath = filepath.replace('/', '\\')
            with open(filepath, 'rb') as f:
                send_data_header = struct.pack(fmt, b'fps0', len(filename))
                sock.send(send_data_header + filename)
                while True:
                    data = f.read(FILE_READ_DATA)
                    filesize = filesize - FILE_READ_DATA
                    if not data:
                        break
                    if filesize <= 0:
                        send_data_header = struct.pack(fmt, b'fpe0', len(data))
                    else:
                        send_data_header = struct.pack(fmt, b'fpd0', len(data))
                    sock.send(send_data_header + sendData.encode())
                print('파일 전송 완료')
        
RECV_FILE_NAME = ''
RECV_FILE_PATH = ''
def receive(sock):
    while True:
        recv_data_header = sock.recv(HEADER_SIZE)
        header = struct.unpack(fmt, recv_data_header)
        recvData = sock.recv(header[1])
        print(header)
        print(header[0][0])
        print(header[0][1])
        print(header[0][2])
        print(recvData)
        
        
        if header[0][0] == b'm':
            if header[0][1] == b'p':
                print('상대방 : ', recvData.decode())
            elif header[0][1] == b'n':
                print('1:n메세지 수신', recvData.decode())
        elif header[0][0] == b'f':
            if header[0][1] == b'p':
                if header[0][2] == b's':
                    RECV_FILE_PATH = filedialog.askdirectory()
                    RECV_FILE_NAME = recvData.decode()
                elif header[0][2] == b'd':
                    with open(RECV_FILE_PATH + '/' + RECV_FILE_NAME, 'wb') as f:
                        f.write(recvData)
                elif header[0][2] == b'e':
                    with open(RECV_FILE_PATH + '/' + RECV_FILE_NAME, 'wb') as f:
                        f.write(recvData)
                    RECV_FILE_PATH = ''
                    RECV_FILE_NAME = ''
                    
            print('파일 들어옴')
        
port = 8888

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('localhost', port))

print('접속 완료')

sender = Thread(target = send, args = (clientSock, ))
receiver = Thread(target = receive, args = (clientSock, ))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    
    pass
