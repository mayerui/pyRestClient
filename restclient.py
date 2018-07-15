from urllib import request
import json
import hashlib
import base64
import sys

#修改全局参数即可
#3326及之前的版本采用old，之后版本采用new
#使用方法：在cmd中输入命令 python 绝对路径\restclient.py
method='GET'
ip = '208.208.70.131'
port = '8080'
uri = '/VIID/Cameras?XZQY=100000&offset=0&limit=1'
#uri = '/VIID/iac/sessionip?address={1.1.1.1}&count=1&online=1'
def main(argv='new'):
    url = 'http://' + ip + ':' + port + uri;
    req = request.Request(url = url, method = method)
    req.add_header("Content-type","application/json")

    if argv == 'old':
        Authorization = login_old()
    else:
        Authorization = login_new()

    if type(Authorization) is not str:
        print("restful fail.\n")
        print(Authorization)
        return
    
    req.add_header("Authorization",Authorization)
        
    print(json.loads(request.urlopen(req).read()))

def login_old():
    req_access_code = request.Request(url = 'http://' + ip + ':' + port + '/VIID/login',method='POST')
    req_access_code.add_header("Content-type","application/json")
    req_access_code.add_header("Accept","application/json")
    response = json.loads(request.urlopen(req_access_code).read())

    if('access_code' not in response):
        return response

    access_code = response['access_code']
    password_md5 = hashlib.md5('admin'.encode(encoding='UTF-8')).hexdigest()

    login_signature = base64.b64encode(b'admin').decode() + access_code + password_md5
    login_signature_md5 = hashlib.md5(login_signature.encode(encoding='UTF-8')).hexdigest()

    content_dic = {
	"username":"admin",
	"access_code":access_code,
	"login_signature":login_signature_md5
        }
    content = json.dumps(content_dic);

    response = json.loads(request.urlopen(req_access_code, data = content.encode(encoding = "UTF-8")).read())

    if('access_token' not in response):
        return response

    access_token = response['access_token']
    return(access_token)

def login_new():
    req_access_code = request.Request(url = 'http://' + ip + ':' + port + '/VIID/login',method='POST')
    req_access_code.add_header("Content-type","application/json")
    req_access_code.add_header("Accept","application/json")
    response = json.loads(request.urlopen(req_access_code).read())

    if('AccessCode' not in response):
        return response

    access_code = response['AccessCode']
    password_md5 = hashlib.md5('admin'.encode(encoding='UTF-8')).hexdigest()

    login_signature = base64.b64encode(b'admin').decode() + access_code + password_md5
    login_signature_md5 = hashlib.md5(login_signature.encode(encoding='UTF-8')).hexdigest()

    content_dic = {
	"UserName":"admin",
	"AccessCode":access_code,
	"LoginSignature":login_signature_md5
        }
    content = json.dumps(content_dic);

    response = json.loads(request.urlopen(req_access_code, data = content.encode(encoding = "UTF-8")).read())

    if('AccessToken' not in response):
        return response

    access_token = response['AccessToken']
    return(access_token)

if __name__ == '__main__':
    if len(sys.argv) >1:
        main(sys.argv[1])
    else:
        main()

    
