import MySQLdb

conn = MySQLdb.connect(localhost,'root','123456','test')
cur = conn.cursor()

def addUser(username,password):
  sql = "insert into test (username,password) values (%s,%s)" %(username,password)
  cur.execute(sql)
  cur.commit()
  cur.close()
