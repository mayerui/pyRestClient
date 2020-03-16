#encoding=GBK
import os
import sys
import time
import re

workspace = sys.argv[0][0:sys.argv[0].rfind('\\')]
newtime = time.strftime("%Y%m%d-%H:%M:%S.000", time.localtime(time.time()))
YYYY=newtime[0:4]
YY=newtime[2:4]
MM = newtime[4:6]
DD = newtime[6:8]

#改文件名
os.chdir(workspace)
fileList=os.listdir(workspace)

for fileName in fileList:
    pat = 'FC*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + YY + MM + DD +'.001')
        break

#NQHQ.dbf NQXX.dbf
def change_inside_time_dbf(filename):
    line = bytes()
    with open(filename, mode="rb+") as f:
        line = f.read()
        enter_pos = line.find(b'\x0d') #换行符
        date_pos = enter_pos + 8
        date = line[date_pos : date_pos + 8]
        line = line.replace(date, bytes((YYYY + MM + DD).encode("utf-8")), 1)

    if len(line) > 0:
        with open(filename, mode="wb+") as f:
            f.write(line)

change_inside_time_dbf("NQHQ.dbf")
change_inside_time_dbf("NQXX.dbf")