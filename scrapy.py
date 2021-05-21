#pip install tweepy
import tweepy, json
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

print("procesando, tardará..., lo más probable...")

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
        self.file.write( json.dumps(tweet) + '\n' )
        self.num_tweets += 1
        if self.num_tweets < 1000:
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)

    if match:
        return True
    return False
# Initialize Stream listener
l = MyStreamListener()


# Create your Stream object with authentication
stream = tweepy.Stream(auth, l)

# Filter Twitter Streams to capture data by the keywords:
a = 'mitsubishi'
b = 'mazda'
c = 'toyota'
d = 'audi'
stream.filter(track=[a,b,c,d])

# String of path to file: tweets_data_path
tweets_data_path = 'tweets.txt'

# Initialize empty list to store tweets: tweets_data
tweets_data = []

# Open connection to file
tweets_file = open(tweets_data_path, "r")


# Read in tweets and store in list: tweets_data
for line in tweets_file:
    tweet = json.loads(line)
    tweets_data.append(tweet)

# Close connection to file
tweets_file.close()

# Print the keys of the first tweet dict
print(tweets_data[0].keys())

# rows list initialization , que pasa cuando hay json anidado???
rows = [] 
  
# appending rows 
for data in tweets_data: 
    data_row = data['user'] 
    rows.append(data_row)

# using data frame 
df = pd.DataFrame(rows)
df2 = pd.DataFrame(tweets_data, columns=['text'])
df = df.join(df2)
print(df[['screen_name','text']]) 

# Print head of DataFrame
print(df)

# Initialize list to store tweet counts
[p, q, r, s] = [0, 0, 0, 0]

# Iterate through df, counting the number of tweets in which
# each candidate is mentioned
for index, row in df.iterrows():
    p += word_in_text(a, row['text'])
    q += word_in_text(b, row['text'])
    r += word_in_text(c, row['text'])
    s += word_in_text(d, row['text'])

# Set seaborn style
sns.set(color_codes=True)

# Create a list of labels:cd
cd = [a, b, c, d]

# Plot the bar chart
ax = sns.barplot(cd, [p,q,r,s])
ax.set(ylabel="count")
plt.show()

