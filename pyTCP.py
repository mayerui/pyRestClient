import socket
import os
import time

address = ('192.168.46.217', 25729)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

with open( 'RT_LOGIN.bin', 'rb') as f:
    s.send(f.read())

data = s.recv(1024)
print(bytes(data))

os.chdir("./request")
fileList = os.listdir()
dataList = list()
for fileName in fileList:
    with open(fileName, 'rb') as f:
        data = f.read()
        dataList.append(data)

while 1:
    for i in range(0, len(dataList)):
        s.send(dataList[i])    
        data = s.recv(1024)
        print(bytes(data))
    
    #time.sleep(0.01)
    
s.close()