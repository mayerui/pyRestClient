from urllib import request
import json

#修改全局参数即可
#使用方法：在cmd中输入命令 python 绝对路径\restclient.py
host = "172.0.0.1:8080"
uri = 'xxxx'
method='GET'
def main():
    url = host + uri;
    req = request.Request(url = url, method = method)
    req.add_header("Content-type","application/json")

    print(json.loads(request.urlopen(req).read()))


if __name__ == '__main__':
        main()
