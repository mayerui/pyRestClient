#encoding=UTF-8
import os
import sys
import time
import re

workspace = sys.argv[0][0:sys.argv[0].rfind('\\')]
newtime=time.strftime("%Y%m%d-%H:%M:%S.000", time.localtime(time.time()))
one_day_before_time=time.strftime("%Y%m%d-%H:%M:%S.000", time.localtime(time.time() - 24*60*60))
YYYY=newtime[0:4]
MM = newtime[4:6]
DD = newtime[6:8]
one_day_before_YYYY=one_day_before_time[0:4]
one_day_before_MM = one_day_before_time[4:6]
one_day_before_DD = one_day_before_time[6:8]

#mktdt00
def change_inside_time(filename):
    path=workspace + '\\'+filename
    file=open(path,'r')
    lines=file.readlines()
    file.close()

    header=lines[0]
    oldtime=header.split('|')[6]
    header=header.replace(oldtime, newtime, 1)
    lines[0]=header

    file = open(path, 'w', newline = '\n')
    file.writelines(lines)
    file.close()
    
change_inside_time('mktdt00.txt')
change_inside_time('mktdt01.txt')
change_inside_time('mktdt03.txt')

#改文件名
os.chdir(workspace)
fileList=os.listdir(workspace)
for fileName in fileList:
    pat = 'cpxx[0-9]{4}.txt'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        with open(fileName, 'a') as f:
            f.write('\n')
        os.rename(fileName, "cpxx" + MM+DD+'.txt')
        break

for fileName in fileList:
    pat = 'cpxx0202[0-9]{4}.txt'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        with open(fileName, 'a') as f:
            f.write('\n')
        os.rename(fileName, "cpxx0202" + MM+DD+'.txt')
        
        break
        
for fileName in fileList:
    pat = 'fjy*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + YYYY+MM+DD+'.txt')
        break
        
for fileName in fileList:
    pat = 'clpr03*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] +MM+DD+'.txt')
        break
        
for fileName in fileList:
    pat = 'reff03*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + MM+DD+'.txt')
        break

#沪伦通
for fileName in fileList:
    pat_list = ['se018cdr*',  'se053pqccbglj*','se038gdrjbxx*','se060gdrjbxx*']
    for pat in pat_list:
        dest = re.findall(pat, fileName)
        if len(dest) != 0:
            os.rename(fileName, dest[0] + YYYY+MM+DD+'001.txt')
        
for fileName in fileList:
    pat = 'Eod_sum_d_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + one_day_before_DD+one_day_before_MM + one_day_before_YYYY +'.csv')
        break
