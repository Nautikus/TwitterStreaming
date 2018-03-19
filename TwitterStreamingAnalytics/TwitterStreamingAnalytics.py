import datetime, pytz
import json
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import settings

db = dataset.connect(settings.CONNECTION_STRING)

AUTH = tweepy.OAuthHandler(settings.TWITTER_CON_TOK, settings.TWITTER_CON_SEC)
AUTH.set_access_token(settings.TWITTER_ACC_TOK, settings.TWITTER_ACC_SEC)
API = tweepy.API(AUTH)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
#This will take the tweets, and insert them into the sqlite DB
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
            
            #Prints to console for monitoring
            print(text)

            #Dumps coordinates if there are any
            if coords is not None:
                coords = json.dumps(coords)

            tweettable = db[settings.TWEET_TABLE]
            try:
                tweettable.insert(dict(
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
                    polarity = polarity,
                    subjectivity = subjectivity,
                    language = lang,
                  ))
            except ProgrammingError as err:
                print(err)

#This will grab the tweet text, pull the hashtags from it and add it to the DB
            tweettxt = text
            tweettxt = tweettxt.replace('#',' #')

            for punct in '.!",;:%<>/~`()[]{}?':
                tweettxt = tweettxt.replace(punct,' ')
            
            tweettxt = tweettxt.split()

            hashtable = db[settings.HASHTAG_TABLE]
            for word in tweettxt:
                if word[0] == '#':
                    hashtag = word.lower()
                    if len(hashtag) > 0:
                        try:
                            hashtable.insert(dict(
                                id_str = id_str,
                                user_name = name,
                                hashtag = hashtag,
                                used = mtntime
                            ))
                        except ProgrammingError as err:
                            print(err)

#This will grab the @ mentions. Who the person is tweeting at.

            atmention = text
            atmention = atmention.replace('@',' @')

            atmention = atmention.split()
            mentiontable = db[settings.MENTION_TABLE]
            for mention in atmention:
                if mention[0] == "@":
                    atmention = mention.lower()
                    if len(atmention) > 0:
                        try:
                            mentiontable.insert(dict(
                                id_str = id_str,
                                user_name = name,
                                atmention = atmention,
                                used = mtntime
                            ))                       
                        except ProgrammingError as err:
                            print(err)          

        
    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=API.auth, listener=MyStreamListener())
stream.filter(track=settings.TRACK_TERMS)
