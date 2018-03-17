import settings
import tweepy
from tweepy.streaming import StreamListener
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import datetime, pytz


db = dataset.connect(settings.CONNECTION_STRING)

AUTH = tweepy.OAuthHandler(settings.TWITTER_CON_TOK, settings.TWITTER_CON_SEC)
AUTH.set_access_token(settings.TWITTER_ACC_TOK, settings.TWITTER_ACC_SEC)
API = tweepy.API(AUTH)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):        
        if (not status.retweeted) and ('RT @' not in status.text) and ('https://t.co/' not in status.text) and (status.lang == 'en'):            
            description = status.user.description
            loc = status.user.location
            text = status.text
            source = status.source
            name = status.user.screen_name
            coords = status.coordinates
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_str = status.id_str
            created = status.created_at
            retweets = status.retweet_count  
            blob = TextBlob(text)
            sent = blob.sentiment
            lang = status.lang
            #polarity - -1, 1. -1 is very negative.
            #subjectivity is 0 to 1. 0 is objective, 1 is subjective
            polarity = sent.polarity            
            subjectivity = sent.subjectivity

            #Adds the tzinfo to the creeated_at object, and then converts it to MST
            utc = pytz.utc
            mountain = pytz.timezone('US/Mountain')
            utctime = status.created_at.replace(tzinfo=utc)
            mtntime = utctime.astimezone(mountain)
           
            print(text)

            if coords is not None:
                coords = json.dumps(coords)


            table = db[settings.TABLE_NAME]          
            try:
                table.insert(dict(
                  user_description = description,
                  user_location = loc,
                  user_name = name,
                  created = mtntime,
                  source = source,
                  text = text,                  
                  coordinates = coords,
                  user_created = user_created,
                  user_followers = followers,
                  id_str = id_str,                  
                  #retweet_count = retweets,
                  polarity = sent.polarity,
                  subjectivity = sent.subjectivity,
                  language = lang,
                  ))
            except ProgrammingError as err:
                print(err)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=API.auth, listener=MyStreamListener())
stream.filter(track=settings.TRACK_TERMS)
