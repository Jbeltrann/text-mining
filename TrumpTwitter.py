import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

class TwitterClient(object): 
    def __init__(self): 
        access_token = '2175131634-pdEy2xUxwxvEvismR75hQsa9WX8uOcjgZRVsSkq'
        access_token_secret = 'nQxKMc9qFXYlWWi4OmnDY6cZyOmcApb9a6Q2vMM8yF2DG'
        consumer_key = 'uTFEHJmvF9BsGElxvsXcVlbnc'
        consumer_secret = 'dvwDMUyR0BlUXM4Muu2hEuVMKO7ZNd3B6dyxt5mWfEPwkuT810'
         
        try:  
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet): 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        tweets = [] 
        try: 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            for tweet in fetched_tweets: 
                parsed_tweet = {} 
   
                parsed_tweet['text'] = tweet.text  
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            return tweets 
  
        except tweepy.TweepError as e:  
            print("Error : " + str(e)) 



  
def main(): 
    api = TwitterClient()  
    tweets = api.get_tweets(query = '#Trump', count = 200) 
  
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))  
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    

# print(plt.show())

  # printing first 2 positive tweets 
    print("\n\positive tweets:") 
    for tweet in ptweets[:2]: 
        print(tweet['text']) 
  
    # printing first 2 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:2]: 
        print(tweet['text']) 

if __name__ == "__main__": 
    main()

objects = ('Positive', 'Negative')
y_pos = np.arange(len(objects))
sentiment = [ 27.848101265822784, 24.050632911392405]

plt.bar(y_pos, sentiment, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Percent of Total Responses')
plt.title('Twitter User Sentiment on Trump')
plt.show() 