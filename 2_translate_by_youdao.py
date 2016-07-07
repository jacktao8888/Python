import urllib.request
import urllib.parse
import json

var = input("请输入需要翻译的内容: ")

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

#o = urllib.parse.urlparse(url)
#print (o)

data = urllib.parse.urlencode(data).encode('utf-8')

response = urllib.request.urlopen(url, data)

html = response.read().decode('utf-8')
 
target = json.loads(html)


print ("翻译结果：%s"%target['translateResult'][0][0]['tgt'])
