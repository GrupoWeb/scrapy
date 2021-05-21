import tweepy, json
import pandas as pd
import word_text
import matplotlib.pyplot as plt
import seaborn as sns


class cachePool():
  def Stream(auth,tweepyListener):
    transform = word_text.Transform()
    stream = tweepy.Stream(auth, tweepyListener)
    filter = ['mitsubishi','mazda','toyota','audi']
    stream.filter(track=filter)
    tweets_data_path = 'tweets.txt'
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
      tweet = json.loads(line)
      tweets_data.append(tweet)

    tweets_file.close()

    print(tweets_data[0].keys())

    rows = [] 

    for data in tweets_data: 
      data_row = data['user'] 
      rows.append(data_row)

    df = pd.DataFrame(rows)
    df2 = pd.DataFrame(tweets_data, columns=['text'])
    df = df.join(df2)
    # print(df[['screen_name','text']]) 

    # print(df)

    # [p, q, r, s] = [0, 0, 0, 0]

    # for index, row in df.iterrows():
    #   print(row)
    #   # p += transform.word_in_text(a, row['text'])
    #   # q += transform.word_in_text(b, row['text'])
    #   # r += transform.word_in_text(c, row['text'])
    #   # s += transform.word_in_text(d, row['text'])

    # # Set seaborn style
    # sns.set(color_codes=True)

    # # Create a list of labels:cd
    # cd = [a, b, c, d]

    # # Plot the bar chart
    # ax = sns.barplot(cd, [p,q,r,s])
    # ax.set(ylabel="count")
    # plt.show()

