#python3整合了urllib和urllib2,而且urllib只有用python3作解释器才不会报错：
#import urllib.request
#ImportError: No module named request


import urllib.request
import urllib.parse
import json
import time

while True:
    var = input("请输入需要翻译的内容: ")
    if var == 'q!' or var == '':
        break
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=http://www.youdao.com/'
    data = {}
    data['type'] = 'AUTO'
    data['i'] = var
    data['doctype'] = 'json'
    data['xmlVersion'] = '1.8'
    data['keyfrom'] = 'fanyi.web'
    data['ue'] = 'UTF-8'
    data['action'] = 'FY_BY_CLICKBUTTON'
    data['typoResult'] = 'true'
    data = urllib.parse.urlencode(data).encode('utf-8')

    #o = urllib.parse.urlparse(url)
    #print (o)

    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    req = urllib.request.Request(url, data, header)
    response = urllib.request.urlopen(req)
    #response = urllib.request.urlopen(url, data)

    html = response.read().decode('utf-8')
     
    target = json.loads(html)


    print ("翻译结果：%s"%target['translateResult'][0][0]['tgt'])
    print (req.headers)
    time.sleep(2)


