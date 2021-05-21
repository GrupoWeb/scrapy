import tweepy, json



class conection_api(tweepy.StreamListener):
  def __init__(self, api=None):
    super(conection_api, self).__init__()
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api