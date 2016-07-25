import MySQLdb

conn = MySQLdb.connect(localhost,'root','123456','test')
cur = conn.cursor()

def addUser(username,password):
  sql = "insert into test (username,password) values (%s,%s)" %(username,password)
  cur.execute(sql)
  cur.commit()
  cur.close()

def isExisted(username,password):
  sql = "select * from test where username='%s' and password='%s'" %(username,password)
  cur.execute(sql)
  result = cur.fetchall()
  cur.close()
  if (len(result)==0):
    return False
  else:
    return True
