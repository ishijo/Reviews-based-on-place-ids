import sqlite3

conn= sqlite3.connect('greviewdb.sqlite')
cur=conn.cursor()
cur.execute("SELECT * FROM Reviews;")
rows=cur.fetchall()

for row in rows:
    print(row)
