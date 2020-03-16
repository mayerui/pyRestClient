#encoding=GBK
import os
import sys
import time
import re

workspace = sys.argv[0][0:sys.argv[0].rfind('\\')]
newtime=time.strftime("%Y%m%d-%H:%M:%S.000", time.localtime(time.time()))

#改文件名
os.chdir(workspace)
fileList=os.listdir(workspace)
for fileName in fileList:
    pat = 'bonddistributionparams_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
        
for fileName in fileList:
    pat = 'cashauctionparams_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break

for fileName in fileList:
    pat = 'cashsecurityclosemd_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
        
for fileName in fileList:
    pat = 'evoteparams_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
        
for fileName in fileList:
    pat = 'indexinfo_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break

for fileName in fileList:
    pat = 'issueparams_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
        
for fileName in fileList:
    pat = 'negotiationparams_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
        
for fileName in fileList:
    pat = 'rightsissueparams_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
        
for fileName in fileList:
    pat = 'securities_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
        
        
for fileName in fileList:
    pat = 'stat_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break

for fileName in fileList:
    pat = 'cnindex_*'
    pattern = re.findall(pat, fileName)
    if len(pattern) != 0:
        os.rename(fileName, pattern[0] + newtime[0:8]+'.xml')
        break
