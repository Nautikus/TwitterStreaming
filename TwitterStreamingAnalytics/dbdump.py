#Exports database to csv

import settings
import dataset
import tweepy
import datafreeze
from datafreeze import freeze

db = dataset.connect(settings.CONNECTION_STRING)
#Export the tweet table
result = db[settings.TWEET_TABLE].all()
datafreeze.freeze(result, format='csv', filename=settings.CSV_NAME)