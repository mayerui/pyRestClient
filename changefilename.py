import os
import sys
import time
import re

workspace = sys.argv[0][0:sys.argv[0].rfind('\\')]
path=workspace + '\\mktdt00.txt'
file=open(path,'r')
lines=file.readlines()
file.close()

header=lines[0]
oldtime=header.split('|')[6]
newtime=time.strftime("%Y%m%d-%H:%M:%S.000", time.localtime(time.time()))
header=header.replace(oldtime, newtime, 1)
lines[0]=header

file = open(path, 'w', newline = '\n')
file.writelines(lines)
file.close()

os.chdir(workspace)
fileList=os.listdir(workspace)
for fileName in fileList:
    pat = 'cpxx*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[4:8]+'.txt')
        break

for fileName in fileList:
    pat = 'fjy*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.txt')
        break

workspace += '/se_cdr'
os.chdir(workspace)
fileList = os.listdir(workspace)

for fileName in fileList:
    pat = 'se018cdr*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'001.txt')
        break
        
for fileName in fileList:
    pat = 'se053pqccbglj*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'001.txt')
        break
