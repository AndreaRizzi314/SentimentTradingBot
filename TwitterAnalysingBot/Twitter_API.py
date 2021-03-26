from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
from textblob import TextBlob
from datetime import date
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')


date = date.today()
TickerFilePath = "BotData/TickerScores{Date}.json"


#Make a list of all the ticker symbols in the 'MoreTickers' file
with open(r'TwitterAnalysingBot\MoreTickers.txt', 'r') as f:
        lines = f.readlines(1663)
    
        lines = [x.strip() for x in lines]

#Create a python dictionary with the reset hypescores of all the stocks
Tickers = {}
for Ticker in lines:
    Tickers[Ticker] = 0


                                                                                                                                                                    
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)

 
        #Refresh the 'TickerScores' File
        with open(TickerFilePath.format(Date = date), 'w') as f:
            json.dump(Tickers, f)


        #Finding user data and tweet text within the json output
        Object = json.loads(data)
        user = Object['user'] 
        text = (Object['text'])
        followers = user['followers_count']
        

        #Determining the influence factor
        with open('Configuration.json', 'r') as f:
            Data = f.read()
            Object = json.loads(Data) 
        Hypescore = followers/Object['Hypescore_Formula']


        #Print text of the tweet
        print(text)

        #Determine what company the tweet refers to 
        for word in text.split():

            for Ticker in lines:

                if word.find(Ticker) == -1:
                    pass
    
                else:
                    print(Ticker)
                    if TextBlob(text).sentiment.polarity > 0: #If Sentiment is Positive
                        Tickers[Ticker] = Tickers[Ticker] + Hypescore #Add the Hypescore to the total

                    if TextBlob(text).sentiment.polarity < 0: #If Sentiment is Negative
                        Tickers[Ticker] = Tickers[Ticker] - Hypescore #Subtract the Hypescore to the total
                    
                    if TextBlob(text).sentiment.polarity == 0: #If Sentiment is neutral
                        Tickers[Ticker] = Tickers[Ticker] + Hypescore #Add the Hypescore to the total

        return True



    def on_error(self, status):
        print(status)

#Authentication
if __name__ == "__main__":
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)


    print(lines)




    stream.filter(track=lines)
