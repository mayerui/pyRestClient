#encoding=GBK

import os
import sys
import datetime
import time
from enum import Enum
import copy

class COL_INDEX(Enum):
    CODE = 0
    TIMESTAMP = 1
    OPEN = 2
    HIGH = 3
    LOW = 4
    CLOSE = 5
    VOL = 6
    VALUE = 7


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
        self.setKline(str(line))

    def __str__(self):
        return "{},{},{},{},{},{},{},{},,,,,\n".format(self.code, self.date, self.open, self.high, self.low, self.close, self.vol, self.value)

    def setKline(self, line):
        cols = line.strip().split(",")
        self.code = cols[COL_INDEX.CODE.value]
        self.setDate(int(cols[COL_INDEX.TIMESTAMP.value]))
        self.open = int(cols[COL_INDEX.OPEN.value])
        self.high = int(cols[COL_INDEX.HIGH.value])
        self.low = int(cols[COL_INDEX.LOW.value])
        self.close = int(cols[COL_INDEX.CLOSE.value])
        self.vol = float(cols[COL_INDEX.VOL.value])
        self.value = float(cols[COL_INDEX.VALUE.value])

    def setDate(self, date):
        self.date = date
        self.week = int(time.strftime("%W", time.strptime(str(date), "%Y%m%d")))
        self.day = date % 100
        self.month = int(date / 100) % 100
        self.year = int(date / 10000)

    def addDelta(self, kline):
        if self.code != kline.code:
            raise Exception("add two different codes.")

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
        self.low = min(self.low, kline.low)
        self.close = kline.close
        self.vol += kline.vol
        self.value += kline.value

class MinKline(Kline):
    timestamp = 0

    def __init__(self, line):
        self.setKline(str(line))

    def __str__(self):
        return "{},{},{},{},{},{},{},{},,,,,\n".format(self.code, self.timestamp, self.open, self.high, self.low, self.close, self.vol, self.value)

    def setKline(self, line):
        cols = line.split(",")
        self.code = cols[COL_INDEX.CODE.value]
        self.setMinutes(int(cols[COL_INDEX.TIMESTAMP.value]))
        self.setDate(int(cols[COL_INDEX.TIMESTAMP.value]))
        self.open = int(cols[COL_INDEX.OPEN.value])
        self.high = int(cols[COL_INDEX.HIGH.value])
        self.low = int(cols[COL_INDEX.LOW.value])
        self.close = int(cols[COL_INDEX.CLOSE.value])
        self.value = float(cols[COL_INDEX.VALUE.value])*1000
        self.vol = float(cols[COL_INDEX.VOL.value])*100
    
    def setDate(self, date):
        Kline.setDate(self, int(date / 10000 + 19900000))

    def setMinutes(self, timestamp):
        self.timestamp = timestamp

    def addDelta(self, kline):
        self.timestamp = kline.timestamp
        Kline.addDelta(self, kline)


#由一天的1分钟K线生成相应的5、15、30、60分钟K线
#注意：必须是完整一天的1分钟K线；目前仅支持一个文件对应一个代码
def dealMin1Csv(filename):
    src_file = open(filename, "r+", encoding="UTF-8")
    lines = src_file.readlines()
    
    kline = MinKline(str(lines[0]))
    min5kline = MinKline(kline)
    min15kline = MinKline(kline)
    min30kline = MinKline(kline)
    min60kline = MinKline(kline)
    daykline = Kline(kline)

    f_min5kline = open(kline.code+"_min5.csv","w+")
    f_min15kline = open(kline.code+"_min15.csv","w+")
    f_min30kline = open(kline.code + "_min30.csv", "w+")
    f_min60kline = open(kline.code + "_min60.csv", "w+")
    f_daykline = open(kline.code + "_day.csv", "w+")

    for i in range(1, len(lines)):
        line = lines[i]
        cur_min = i + 1
        kline = MinKline(str(line))

        min5kline.addDelta(kline)
        if cur_min % 5 == 0:
            f_min5kline.write(str(min5kline))
            min5kline = MinKline(kline)

        min15kline.addDelta(kline)
        if cur_min % 15 == 0:
            f_min15kline.write(str(min15kline))
            min15kline = MinKline(kline)

        min30kline.addDelta(kline)
        if cur_min % 30 == 0:
            f_min30kline.write(str(min30kline))
            min30kline = MinKline(kline)

        min60kline.addDelta(kline)
        if cur_min % 60 == 0:
            f_min60kline.write(str(min60kline))
            min60kline = MinKline(kline)

        daykline.addDelta(kline)

    f_daykline.write(str(daykline))

    f_min5kline.close()
    f_min15kline.close()
    f_min30kline.close()
    f_min60kline.close()
    f_daykline.close()


#由日K线生成相应的周、月、年K线
#注意：目前仅支持一个文件对应一个代码；周、月、年K线的生成过程较复杂，需要根据实际情况修改代码
def dealDayCsv(filename):
    src_file = open(filename, "r+", encoding="UTF-8")
    lines = src_file.readlines()
    
    kline = Kline(str(lines[0]))
    week_kline = Kline(kline)
    month_kline = Kline(kline)
    year_kline = Kline(kline)

    f_weekkline = open(kline.code+"_week.csv","w+")
    f_monthkline = open(kline.code+"_month.csv","w+")
    f_yearkline = open(kline.code + "_year.csv", "w+")
    
    for line in lines:
        kline = Kline(str(line))
        if  kline.week != week_kline.week:
            f_weekkline.write(str(week_kline))
            week_kline = Kline(kline)
        elif kline.date != week_kline.date:
            week_kline.addDelta(kline)

        if  kline.month != month_kline.month:
            f_monthkline.write(str(month_kline))
            month_kline = Kline(kline)
        elif kline.date != month_kline.date:
            month_kline.addDelta(kline)

        if  kline.year != year_kline.year:
            f_yearkline.write(str(year_kline))
            year_kline = Kline(kline)
        elif kline.date != year_kline.date:
            year_kline.addDelta(kline)

    f_weekkline.write(str(week_kline))
    f_monthkline.write(str(month_kline))
    f_yearkline.write(str(year_kline))
    f_weekkline.close()
    f_monthkline.close()
    f_yearkline.close()