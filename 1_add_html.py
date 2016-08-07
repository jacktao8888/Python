
#根目录下客户端执行指令“python -m CGIHTTPServer 8081”
#Serving HTTP on 0.0.0.0 port 8081 ...  即开启本地localhost（127.0.0.1）的8081端口
#开启python自带的HTTP服务之后，浏览器URL输入localhost:8081/cgi-bin/add_html.py
import cgi,cgitb
from view_img import *

form1 = cgi.FieldStorage()
num1 = form1.getvalue("Num1")
num2 = form1.getvalue("Num2")
num3 = None

if not num1 is None and not num2 is None:
    num1 = int(num1)
    num2 = int(num2)
    num3 = num1 + num2


print start_response()
print start_div("center","margin-top:60px;")
print img("../views/add.png")
print end_div()

print start_div("center","margin-top:60px;")
print start_form()
if num1 is None:
    print input_label("Num1","adder1")
else:
    print input_label("Num1","adder1",str(num1))
print "+"
if num2 is None:
    print input_label("Num2","adder2")
else:
    print input_label("Num2","adder2",str(num2))
print "="
if num3 is None:
    print input_label("Num3","result","","readonly")
else:
    print input_label("Num3","result",str(num3),"readonly")
print end_form()
print end_div()
