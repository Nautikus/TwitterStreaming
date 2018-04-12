import settings
import sqlite3
import datetime

conn = sqlite3.connect('tweetstest.db')

c = conn.cursor()

#c.execute('select created, polarity, subjectivity from tweet')
#record = c.fetchall()

#print(type(record[0][0]))
#print(record.strftime("%d"))

c.execute("SELECT strftime('%d', 'record') from tweet")
thing = c.fetchall
print(thing)