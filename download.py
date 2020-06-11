#coding=gbk

import requests
import time
from time import sleep
import os
import datetime
import json
import urllib
import random
import logging

url = "http://127.0.0.1:0000/downloads/"
dst_path = "./download/"
file_list = ["block.xml"]


def download():
    session = requests.Session()

    for file_name in file_list:
        response = session.get(url + file_name)
        if response.ok == True:
            file_path = dst_path + file_name
            with open(file_path,'wb') as f:
                f.write(response.content)
            print("{} download success!".format(file_name))
        else:
            print("{} download fail!".format(file_name))


if __name__ == '__main__':
    if (not os.path.exists(dst_path)):
        os.mkdir(dst_path)

    download()
