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

 
        #Update the 'TickerScores' File
        with open(TickerFilePath.format(Date = date), 'w') as f:
            json.dump(Tickers, f)


        #Finding user data and tweet text within the json output
        Tweet_Object = json.loads(data)
        user = Tweet_Object['user'] 
        text = (Tweet_Object['text'])
        followers = user['followers_count']
        

        #Determining the influence factor by finding the hypescore formula in the configuration file
        with open('Configuration.json', 'r') as f:
            Data = f.read()
            Configuration_Object = json.loads(Data) 
        Hypescore = followers/Configuration_Object['Hypescore_Formula']


        #Print text of the tweet
        print(text)
        found = False
        #Determine what company the tweet refers to with the first 100 characters
        for word in text.split():

            for Ticker in lines:

                if word.find(Ticker) == -1:
                    pass

                else:
                    print("\nThis tweet is talking about", Ticker)
                    found = True
                    if TextBlob(text).sentiment.polarity > 0: #If Sentiment is Positive
                        Tickers[Ticker] = Tickers[Ticker] + Hypescore #Add the Hypescore to the total

                    if TextBlob(text).sentiment.polarity < 0: #If Sentiment is Negative
                        Tickers[Ticker] = Tickers[Ticker] - Hypescore #Subtract the Hypescore to the total
                    
                    if TextBlob(text).sentiment.polarity == 0: #If Sentiment is neutral
                        Tickers[Ticker] = Tickers[Ticker] + Hypescore #Add the Hypescore to the total

        #If the tweet couldnt be identified by the first 100 characters the extended text needs to be found  
        if found == False:
            try:
                print("\nLooking for full tweet text under retweeted status")
                full_text = Tweet_Object['retweeted_status']["extended_tweet"]['full_text']
            except:
                print("\nFull text in the retweeted status not found")
                try:
                    print("\nLooking for full tweet under extended tweet")
                    full_text = Tweet_Object["extended_tweet"]['full_text']
                except:
                    print("\nFull text in the extended tweet not found")
                    return
            for word in full_text.split():

                for Ticker in lines:

                    if word.find(Ticker) == -1:
                        pass

                    else:
                        print("\nThis tweet is talking about", Ticker)
                        found = True
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
