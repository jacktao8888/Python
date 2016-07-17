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
