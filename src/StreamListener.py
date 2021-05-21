import tweepy, json




class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open("tweets.txt", "w")
        

    def on_status(self, status):
        tweet = status._json
        data = json.dumps(tweet)
        # data = json.loads(data)
        print(data['user'])
        # for item in tweet:
        #     print(json.dumps(item))
        self.file.write( json.dumps(tweet) + '\n' )
        self.num_tweets += 1
        if self.num_tweets < 3:
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)