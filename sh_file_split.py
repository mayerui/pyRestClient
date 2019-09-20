import socket, time, struct, os, threading


pre_file_path = "D:\\沪深\\SHFAST20190820\\"
filename= 'SHFAST20190820'
lastname = ".dat"
filepath = pre_file_path + filename +lastname

stepfile = "8=STEP.1.0.0"

fo = open(filepath, 'rb')
count = os.path.getsize(filepath)
print("filesize = " + str(count))
count  = count * 0.9
print("after filesize = " + str(count))
fo.seek((int)(count), 0)
filedata = fo.read(10240)
print(type(filedata))
#stepsize = str(filedata).find(stepfile)
stepbyte = bytes(stepfile, encoding="utf8")
stepsize = filedata.find(stepbyte)
print("str(filedata) " + str(filedata)+ "stepsize " + str(stepsize))

seeksize = (int)(count) + stepsize
print("str(seeksize) " + str(seeksize) )
fo.seek(seeksize, 0)

write_path = pre_file_path + filename + '_second' + lastname
wirte_file = open(write_path, "wb")

try:
    while True:
         filedata = fo.read(1024)
         if not filedata:
            break

         wirte_file.write(filedata)
finally:
    wirte_file.close( )



