from socket import *
from threading import *
import time
import struct
from tkinter import filedialog
import os

fmt = '=4si'
fmt_size = struct.calcsize(fmt)

        
def send(sock):
    while True:
        sendData = input('>')
        if sendData[0].lower() == 'm':  
            send_data_header = struct.pack(fmt, b'mp00', len(sendData))
            sock.send(send_data_header + sendData.encode())
        elif sendData[0].lower() == 'f':
            filepath = filedialog.askopenfilename()
            filesize = os.path.getsize(filepath)
            filepath = filepath.replace('/', '\\')
            sock.send()
            with open(filepath, 'wb') as f:
                while True:
                    data = f.read(1024)
                    filesize = filesize - 1024
                    if not data:
                        break
                    if filesize <= 0:
                        send_data_header = struct.pack(fmt, b'fpe0', len(sendData))
                    else:
                        send_data_header = struct.pack(fmt, b'fpd0', len(sendData))
                    sock.send(send_data_header + sendData.encode())
                print('파일 전송 완료')
        

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('상대방 :', recvData)
        
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
