#encoding=GBK
import os
import sys
import datetime
import time
import kline

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append("D:/需求/32国金板块K线修复20191031/result/day")
    
    workspace = sys.argv[1]
    os.chdir(workspace)
    filelist = os.listdir(workspace)
    for file_name in filelist:
        kline.dealDayCsv(workspace+file_name)
