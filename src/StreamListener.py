import tweepy, json
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


consumer_key='gaITkllOhLp20v0jYoO94VF2C'
consumer_key_secret='CjYjIV2186FVV7qZcedSs1yvajgGSclFE4hW1uejKmyFnJMBR9'
access_token='142910198-ot2XMelum0ZVIsPQR1n4W8Rqqe2yDt46ax7yDcpQ'
access_token_secret='jzsWgrMJtEf0eWhGV6MBhQeP4Um06acNl3Hc7DNvaFfUn'
auth=tweepy.OAuthHandler(consumer_key,consumer_key_secret)
auth.set_access_token(access_token,access_token_secret)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open("tweets.txt", "w")
    
    def on_status(self, status):
        tweet = status._json
        data = json.dumps(tweet)
        self.file.write( json.dumps(tweet) + '\n' )
        self.num_tweets += 1
        if self.num_tweets < 10:
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)