from flask import Flask
from flask import request，render_template,url_for,abort
from models import User

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin',methods=['GET'])
def signin_home():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin',methods=['POST'])
def signin():
    if request.form['username']=='admin' and request.form['password']=='123456':
        return '<h3>Hello,admin!</h3>'
    return '<h3>Bad username or password</h3>'

@app.route('/user')             #从后端向前端传数据
def user():
    user = User(1,'jikexueyuan')
    return render_template('index.html',user=user)

@app.route('/users/<id>')        #请求格式如：127.0.0.1:5000/users/Jerry
def user_id(id):    
    return 'hello '+id

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/users/<user_id>')
def users(user_id):
    if int(user_id) == 1:
        return 'hello user:'+user_id
    else:
        abort(404)

@app.route('/query_user')       #请求格式如：127.0.0.1:5000/query_user?id=Tom
def query_user():
    id = request.args.get('id')
    return 'hello user:'+id

@app.route('/query_url')        #flask反向路由，得出query_user路由函数的url地址
def query_url():
    return 'query url: '+url_for('query_user')

if __name__=='__main__':
    app.run()             #默认5000端口
