from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from db import *

app = Flask(__name__)

from wtforms import Form,TextField,PasswordField,validators

class LoginForm(Form):
    username = TextField("username",[validators.Required()])
    password = PasswordField("password",[validators.Required()])

@app.route("/login",methods=['GET','POST'])
def login():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        if isExisted(myForm.username.data,myForm.password.data):
            return "Login Successfully"
        else:
            message = "Login Failed"
            return render_template('index.html',message=message,form=myForm)
    return render_template('index.html',form=myForm)

@app.route("/register",methods=['GET','POST'])
def register():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        addUser(myForm.username.data,myForm.password.data)
        return "Register Successfully"
    return render_template('index.html',form=myForm)

if __name__=='__main__':
    app.run(port=8080)
    
