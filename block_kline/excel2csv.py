#coding=GBK

import sys
import requests
import xlrd
import xlwt
import time
from time import sleep
import os
from xml.dom import minidom
import datetime
from bs4 import BeautifulSoup
import json
import urllib
import random
import demjson


def row2line(row):
    ret = str()
    for i in range(0, len(row)):
        ret += str(row[i]).replace("\n", "")
        if i < (len(row) - 1):
            ret += ","

    ret += "\n"
    return ret


def excl2csv(input_path, output_path):
    workbook = xlrd.open_workbook(input_path)
    sheet = workbook.sheet_by_index(0)
    count = sheet.nrows
    
    with open(output_path, "w+",encoding = "GBK") as f:
        for i in range(0,count):
            row = sheet.row_values(i)
            line = row2line(row)
            f.write(line)
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append("全部A股.xlsx")
    
    if len(sys.argv) < 3:
        sys.argv.append("result.csv")
        
    input_file  = sys.argv[1]
    output_file  = sys.argv[2]
    excl2csv(input_file, output_file)
