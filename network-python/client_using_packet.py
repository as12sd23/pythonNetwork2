from socket import *
from threading import *
import time
import struct
from tkinter import filedialog
from tkinter import * 
import os

fmt = '=4si'
fmt_size = struct.calcsize(fmt)

FILE_READ_DATA = 8
HEADER_SIZE = 8        
RECV_FILE_NAME = ''
RECV_FILE_PATH = 'C:/Users/c404/Desktop/sangjin/새 폴더'
SEND_FILE_PATH = ''

def send(sock): 
    while True:
        sendData = input('\n > ')
        if sendData[0].lower() == 'm':  
            send_data_header = struct.pack(fmt, b'mp00', len(sendData.encode('utf-8')))
            sock.send(send_data_header + sendData.encode('utf-8'))
        elif sendData[0].lower() == 'f':
            root = Tk()
            filepath = filedialog.askopenfilename()
            root.withdraw()
            root.destroy()
            filename = os.path.basename(filepath).encode('utf-8')
            
            send_data_header = struct.pack(fmt, b'fps0', len(filename))
            sock.send(send_data_header + filename)
        
def receive(sock):
    global SEND_FILE_PATH
    global RECV_FILE_NAME
    global RECV_FILE_PATH
    while True:
        recv_data_header = sock.recv(HEADER_SIZE)
        header = struct.unpack(fmt, recv_data_header)
        recvData = sock.recv(header[1])
        
        
        if header[0][0] == 109:
            if header[0][1] == 112:
                print('\n상대방 : ', recvData.decode())
            elif header[0][1] == 110:
                print('1:n메세지 수신', recvData.decode())
        elif header[0][0] == 102:
            if header[0][1] == 112:
                if header[0][2] == 115:
                    RECV_FILE_NAME = recvData.decode()
                    root = Tk()
                    RECV_FILE_PATH = filedialog.askdirectory()
                    root.withdraw()
                    root.destroy()
                    print(RECV_FILE_NAME)
                    '''
                    accept = str(input('yes or no\n > '))
                    if accept == 'yes':
                        file_send_header = struct.pack(fmt, b'fpa0', len(accept.encode('utf-8')))
                    elif aceept == 'no':
                        file_send_header = struct.pack(fmt, b'fpr0', len(accept.encode('utf-8')))
                        '''
                    file_send_header = struct.pack(fmt, b'fpa0', 0)
                    sock.send(file_send_header)
                    print('소켓 전송 완료')
                elif header[0][2] == 97:
                    print(SEND_FILE_PATH)
                    filesize = os.path.getsize(SEND_FILE_PATH)
                    SEND_FILE_PATH = SEND_FILE_PATH.replace('/', '\\')
                    with open(SEND_FILE_PATH, 'rb') as f:
                        while True:
                            print('#')
                            data = f.read(FILE_READ_DATA)
                            filesize = filesize - FILE_READ_DATA
                            
                            if not data:
                                break
                            
                            if filesize <= 0:
                                send_data_header = struct.pack(fmt, b'fpe0', len(data))
                            else:
                                send_data_header = struct.pack(fmt, b'fpd0', len(data))
                            sock.send(send_data_header + data)
                            sleep(1)
                        print('파일 전송 완료')
                elif header[0][2] == 114:
                    SEND_FILE_PATH = ''
                elif header[0][2] == 100:
                    print('파일 전송 중')
                    with open(RECV_FILE_PATH + '/' + RECV_FILE_NAME, 'wb') as f:
                        f.write(recvData)
                elif header[0][2] == 101:
                    print('파일 전송  완료 중')
                    with open(RECV_FILE_PATH + '/' + RECV_FILE_NAME, 'wb') as f:
                        f.write(recvData)
                    RECV_FILE_PATH = 'C:/Users/c404/Desktop/sangjin/새 폴더'
                    RECV_FILE_NAME = ''
                    print('파일 전송  완료')
                    
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
