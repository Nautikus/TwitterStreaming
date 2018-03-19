import settings
import dataset
import tweepy
import datafreeze
from datafreeze import freeze

db = dataset.connect(settings.CONNECTION_STRING)

result = db[settings.TABLE_NAME].all()
datafreeze.freeze(result, format='csv', filename=settings.CSV_NAME)