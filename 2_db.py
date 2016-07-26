import MySQLdb  #MySQLdb只支持Python2.X，不支持Python3.X

conn = MySQLdb.connect("localhost","root","123456","sakila")
cur = conn.cursor()

def addUser(username,password):
    sql = "insert into user (username,password) values('%s','%s');" %(username,password)    #注意：%s要加引号"'"，否则会提示
                                                                                            #     unknown column "xxx" xxx为
                                                                                            #     传进来的username
    cur.execute(sql)
    conn.commit()         #这里注意是conn.commit,而不是cur.commit()!!!!
    #conn.close()

def isExisted(username,password):
    sql = "select * from user where username='%s' and password='%s';" %(username,password)  #注意：这里也要加单引号"'"
    cur.execute(sql)
    result = cur.fetchall()
    #conn.close()
    if (len(result)==0):
        return False
    else:
        return True
