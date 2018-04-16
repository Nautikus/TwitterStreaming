#This will calculate the sentiment average for tweets for the entire tweet table

import sqlite3
import datetime
import settings
import pandas

conn = sqlite3.connect('tweetstest.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

df = pandas.read_sql_query("select created, polarity, subjectivity from tweet",conn)

df['created'] = pandas.to_datetime(df['created'], format="%Y-%m-%d %H:%M:%S")
df.sort_values(by=['created'])

#print(type(df))
#print(df['created'].dt.hour) returns the hours
#print(df.dtypes) returns "created = datetime64, polarity = float64, subject = float64)"

#test = df['created'].dt.hour.iloc[index]
starttime = df['created'].dt.strftime("%Y-%m-%d %H").iloc[0] #returns first record as yyyy-mm-dd HH as a str

count = 0
totalrows = df.shape[0]
print(totalrows)

while count < totalrows:
    for index, row in df.iterrows():
        #created = df['created'].dt.hour.iloc[index]
        created = df['created'].dt.strftime("%Y-%m-%d %H").iloc[index] #returns yyyy-mm-dd HH as a str

        if created == starttime:        
            print(created)        
            count = count + 1

        else:
            print("no match")
    
    
    #print(df['created'].dt.hour.iloc[index]) #returns the hour at index 

    print(count)
    starttime = df['created'].dt.strftime("%Y-%m-%d %H").iloc[count]