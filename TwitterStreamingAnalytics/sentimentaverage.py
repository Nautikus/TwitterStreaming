import settings
import sqlite3
import datetime

conn = sqlite3.connect('tweetstest.db')

c = conn.cursor()

c.execute('select created from tweet where id = 1')
record = c.fetchall()
print(type(c.fetchall()))
#print(record.strftime("%d"))

#c.execute("SELECT strftime('%d', 'record') from tweet")

#print(c.fetchall())