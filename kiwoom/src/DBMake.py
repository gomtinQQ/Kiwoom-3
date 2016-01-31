# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect("D:\\OneDrive\\python\\sqlite3\\kosdaq.db")

print(type(conn))

cursor = conn.cursor()

# cursor.execute("CREATE TABLE kosdaq1(StockCode text, StockName int)")
# cursor.executemany('''insert into kosdaq values(?,?)''',("한",'한양'))

cursor.execute("insert into kosdaq ('StockCode','StockName') values(?,?)",(900090,'gg'))

cursor.execute("select * from kosdaq")
conn.commit()

print(cursor.fetchall())
conn.close()