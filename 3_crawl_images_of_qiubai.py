import os
from bs4 import BeautifulSoup
import re
import urllib.request

#Python3不用写入'#encoding:utf-8'也可以写入中文注释，Python2就不可以*_*

def open_url(url):
  header = {}
  header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
  
  req = urllib.request.Request(url, None, header)
  response = urllib.request.urlopen(req)
  if response.getcode() != 200:
    return None

  html = response.read()
  return html

def collect_link(html):
  img_links = []
    
  a = html.find('src=')
  while a != -1:
    b = html.find('.jpg', a, a+255)     #限制一个查找范围，a-a+255，一开始忘记敲入a+255，报错“ValueError: unknown url type”
    if b != -1:
      img_links.append(html[a+5:b+4])
    else:
      b = a + 5

    a = html.find('src=', b)            #没敲入这行会陷入死循环

#方法2：用下面的方法获取的图片数量比上面的方法获取的少，因为下面的方法采用正则表达式，其限制的范围更小，上面的方法还会获取用户头像等页面上的所有图片
#       注意：在实际用BeautifulSoup解析页面，并查找，查找的正则表达式中的"11693"每天的值会改变
#soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
#links = soup.find_all('img', src=re.compile(r"http://pic.qiushibaike.com/system/pictures/11693/\d+/medium/app\d+.jpg"))
#for link in links:
#    a = link['src']
#    img_links.append(a)
    
  print(img_links)
  return img_links

def save_image(links):
  for link in links:
    filename = link.split('/')[-1]
    img = urllib.request.urlopen(link)
        
  with open(filename, 'wb') as f:
    f.write(img.read())
    
def download_image(dir, url):
  os.mkdir(dir)
  os.chdir(dir)
    
  html = open_url(url).decode('utf-8')    #没有decode('utf-8')会报错“a = html.find('src=') TypeError: 'str' does not support the buffer interface”
    
  links = collect_link(html)
    
  save_image(links)

    
if __name__=='__main__':
  url = 'http://www.qiushibaike.com/imgrank/'
    
  download_image("image", url)
