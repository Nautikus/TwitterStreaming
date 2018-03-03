
import settings
import tweepy
from tweepy.streaming import StreamListener
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError

db = dataset.connect(settings.CONNECTION_STRING)

AUTH = tweepy.OAuthHandler(settings.TWITTER_CON_TOK, settings.TWITTER_CON_SEC)
AUTH.set_access_token(settings.TWITTER_ACC_TOK, settings.TWITTER_ACC_SEC)
API = tweepy.API(AUTH)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        
        if (not status.retweeted) and ('RT @' not in status.text) and ('https://t.co/' not in status.text):
            
            description = status.user.description
            loc = status.user.location
            text = status.text           
            name = status.user.screen_name
            coords = status.coordinates
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_str = status.id_str
            created = status.created_at
            retweets = status.retweet_count  
            blob = TextBlob(text)
            sent = blob.sentiment
            polarity = sent.polarity
            subjectivity = sent.subjectivity
            
            table = db[settings.TABLE_NAME]          
            try:
                table.insert(dict(
                  user_description = description,
                  user_location = loc,
                  text = text,
                  user_name = name,
                  coordinates = coords,
                  user_created = user_created,
                  user_followers = followers,
                  id_str = id_str,
                  created  = created,
                  retweet_count = retweets,
                  polarity = sent.polarity,
                  subjectivity = sent.subjectivity,
                  ))
            except ProgrammingError as err:
                print(err)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=API.auth, listener=MyStreamListener())
stream.filter(track=settings.TRACK_TERMS)
