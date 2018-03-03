import dataset
import tweepy
import datafreeze
from datafreeze import freeze
db = dataset.connect("sqlite:///tweets.db")

result = db["tweets"].all()
datafreeze.freeze(result, format='csv', filename="tweets.csv")