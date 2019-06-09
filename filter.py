import os
import sys
import time
import re

workspace = sys.argv[0][0:sys.argv[0].rfind('\\')]

os.chdir(workspace)
fileList = os.listdir(workspace)
for fileName in fileList:
    if ".csv" not in fileName:
        continue
    f = open(fileName, mode="r", encoding="GBK")
    lines = f.readlines()
    s3 = lines[3].split(sep=',')
    s4 = lines[4].split(sep=',')
    f.close()
    if float(s3[len(s3) - 1]) < 0.6 or float(s4[len(s4) - 1]) < 0.45:
        os.remove(fileName)
