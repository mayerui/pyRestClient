#encoding=GBK

import os
import sys
import datetime
import time

g_day_list = [20191028,20191029,20191030,20191031,20191101]

code2guben = dict()
dic_block = dict()
dic_minkline = dict()
dic_block_prepx = dict()
dic_mem_prepx = dict()


def calcPx(pre_px, memberlist, m):
    pre_px = int(pre_px)
    sum_up = 0
    sum_down = 0
    _minkline = MinKline(None)
    for membercode in memberlist:
        if membercode in dic_minkline and membercode in code2guben and membercode in dic_mem_prepx:
            minkline = MinKline(dic_minkline[membercode][m])
            _minkline.addDelta(minkline)
            sum_up +=(float(code2guben[membercode]) * minkline.close)
            sum_down +=(float(code2guben[membercode]) * dic_mem_prepx[membercode])
            
    if sum_down == 0:
        print("sum_down = 0\n")
    else:
        px = int(pre_px*(sum_up/sum_down))
        _minkline.open = px
        _minkline.high = px
        _minkline.low = px
        _minkline.close = px
        _minkline.open = px
    
    return _minkline


class Kline:
    code = 0
    date = 0
    open = 0
    high = 0
    low = 0
    close = 0
    vol = 0
    value = 0

    day = 0
    week = 0
    month = 0
    year = 0
    
    def __init__(self, line):
        if line is not None:
            self.setKline(str(line))

    def __str__(self):
        return str(self.code)+","+str(self.date)+","+str(self.open)+","+str(self.high)+","+str(self.low)+","+str(self.close)+","+str(self.vol)+","+str(self.value)+",,,,,\n"

    def setKline(self, line):
        cols = line.split(",")
        self.code = cols[0]
        self.setDate(int(cols[1]))
        self.open = int(cols[2])
        self.high = int(cols[3])
        self.low = int(cols[4])
        self.close = int(cols[5])
        self.vol = float(cols[6])
        self.value = float(cols[7])

    def setDate(self, date):
        self.date = date
        self.week = int(time.strftime("%W", time.strptime(str(date), "%Y%m%d")))
        self.day = date % 100
        self.month = int(date / 100) % 100
        self.year = int(date / 10000)

    def addDelta(self, kline):
        self.timestamp = kline.timestamp
        self.date = kline.date
        self.day = kline.day
        self.week = kline.week
        self.month = kline.month
        self.year = kline.year
        if self.open == 0:
            self.open = kline.open
        self.high = max(self.high, kline.high)
        if self.low == 0:
            self.low = kline.low
        else:
            self.low = min(self.low, kline.low)
        self.close = kline.close
        self.vol += kline.vol
        self.value += kline.value


class MinKline(Kline):
    timestamp = 0
    def __init__(self, line):
        if line is not None:
            self.setKline(str(line))

    def __str__(self):
        return str(self.code)+","+str(self.timestamp)+","+str(self.open)+","+str(self.high)+","+str(self.low)+","+str(self.close)+","+str(self.vol)+","+str(self.value)+",,,,,\n"

    def setKline(self, line):
        cols = line.split(",")
        self.timestamp = int(cols[0])
        self.setDate(int(cols[0]))
        self.open = int(cols[1])
        self.high = int(cols[2])
        self.low = int(cols[3])
        self.close = int(cols[4])
        self.value = float(cols[5])*1000
        self.vol = float(cols[6])*100
    
    def setDate(self, date):
        date = int(date / 10000 + 19900000)
        self.date = date
        self.week = int(time.strftime("%W", time.strptime(str(date), "%Y%m%d")))
        self.day = date % 100
        self.month = int(date / 100) % 100
        self.year = int(date / 10000)


def min2day(date):
    workspace = "D:/工具/winner_protocol_test/workspace.x64/response/"
    os.chdir(workspace + str(g_day_list[date - 1]))
    fileList = os.listdir(workspace + str(g_day_list[date - 1]))
    for filename in fileList:
        with open(filename, "r",encoding = "GBK") as f:
            pos = filename.find("TechdataRange_") + len("TechdataRange_")
            code = filename[pos : pos + 6]
            lines = f.readlines()
            if len(lines) < 2:
                print(code+" no minkline")
                continue
            dic_mem_prepx[code] = MinKline(lines[len(lines) - 1]).close

    os.chdir(workspace + str(g_day_list[date]))
    fileList = os.listdir(workspace + str(g_day_list[date]))
    for filename in fileList:
        with open(filename, "r",encoding = "GBK") as f:
            pos = filename.find("TechdataRange_") + len("TechdataRange_")
            code = filename[pos : pos + 6]
            lines = f.readlines()
            if len(lines) < 2:
                print(code+" no minkline")
                continue
            dic_minkline[code] = list()
            for i in range(1, len(lines)):
                dic_minkline[code].append(lines[i].strip())

    block_list = dic_block.items()
    for block in block_list:
        memberlist = block[1]
        with open("D:/需求/32国金板块K线修复20191031/" + "result/day/" + str(block[0]) + "_day.csv","a") as f:
            kline = Kline(None)
            kline.code = block[0]
            with open("D:/需求/32国金板块K线修复20191031/" + "result/min/" + str(block[0]) + "_min1.csv", "a") as f_min:
                for m in range(0, 240):
                    minkline = MinKline(None)
                    minkline.code = block[0]
                    curminkline = calcPx(dic_block_prepx[block[0]], memberlist, m)
                    curminkline.code = block[0]
                    f_min.write(str(curminkline))
                    minkline.addDelta(curminkline)
                    kline.addDelta(minkline)
            
            f.write(str(kline))
            dic_block_prepx[block[0]] = kline.close

    with open("prepx_" + str(g_day_list[date]) + ".csv", "w") as f:
        f.writelines(dic_block_prepx)


if __name__ == '__main__':
    with open("流通股本.csv","r") as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            cols = line.split(",")
            code2guben[cols[0]] = cols[1].strip()

    with open("block.csv","r") as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            cols = line.split(",")
            memberlist = list()
            for j in range(1, len(cols)):
                memberlist.append(cols[j].strip())
            dic_block[cols[0]] = memberlist

    #读取昨收价
    os.chdir("D:/需求/32国金板块K线修复20191031/")
    # filelist = os.listdir()
    # for filename in filelist:
    #     with open(filename,"r") as f:
    #         lines = f.readlines()
    #         line = lines[2].strip().split(",")
    #         dic_block_prepx[line[0]] = line[5]
    with open("prepx.csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(',')
            dic_block_prepx[line[0]] = line[1]

    day_list = [2,3,4]
    for date in day_list:
        print(date)
        min2day(date)
