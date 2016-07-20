import MySQLdb

conn = MySQLdb.connect("localhost","root","123456","sakila")

cur = conn.cursor()

name = raw_input()

sql = "select * from student"
#insert_sql = "insert into sakila.student (name) values ('%s')"%(name)

#cur.execute(insert_sql)
#cur.commit()
cur.execute(sql)

result = cur.fetchall()

for row in result:
    print row[0]
    print row[1]

conn.close()
