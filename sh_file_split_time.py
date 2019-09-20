#二分法找时间

import sys, socket, time, struct, os, threading

pre_file_path = "D:\\沪深\\SHFAST20190820\\"
filename= 'SHFAST20190820'
lastname = ".dat"
begin_time = 9150000   #必须8位 HHMMSSss

STEP_BYTE = bytes("8=STEP.1.0.0", encoding="utf8")
TIME_BYTE = bytes("779=", encoding = "utf8")
TIME_LEN = 8

filepath = pre_file_path + filename +lastname
fo = open(filepath, 'rb')
count = os.path.getsize(filepath)
print("filesize = " + str(count))

l_percent = 0
r_percent = 1
seek_pos = 0
while True:
    percent = (l_percent + r_percent) / 2
    seek_pos = int(count * percent)
    if abs(l_percent - r_percent) < 0.0001:
        break

    fo.seek(seek_pos, 0)
    filedata = fo.read(10240)

    time_pos = filedata.find(TIME_BYTE)
    time = filedata[time_pos + len(TIME_BYTE) : time_pos + len(TIME_BYTE) + TIME_LEN]
    time = int(time)
    if time > begin_time:
        r_percent = percent
    elif time < begin_time:
        l_percent = percent
    else:
        seek_pos = seek_pos + time_pos
        break

#命中时
seek_pos = seek_pos - 10240
if seek_pos < 0:
    print("所需时间未找到")
    sys.exit(0)

print("time:" + str(time))
fo.seek(seek_pos)
filedata = fo.read(10240)

stepsize = filedata.rfind(STEP_BYTE)
seek_pos = (int)(seek_pos) + stepsize
print("str(seeksize) " + str(seek_pos) )
fo.seek(seek_pos, 0)

write_path = pre_file_path + filename + '_' + str(int(begin_time / 10000)) + "_" + lastname
wirte_file = open(write_path, "wb")

try:
    while True:
         filedata = fo.read(1024)
         if not filedata:
            break

         wirte_file.write(filedata)
finally:
    wirte_file.close( )



