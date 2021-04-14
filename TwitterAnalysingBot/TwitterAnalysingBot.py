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
TickerScoresFilePath = "BotData/TickerScores{Date}.json"
CandidateTickersFilePath = 'CandidateTickers.txt'
MaxCandidateSizeBytes = 1663


#Make a list of all the ticker symbols in the 'MoreTickers' file
with open(CandidateTickersFilePath, 'r') as f:
    lines = f.readlines(MaxCandidateSizeBytes)
    
    Candidate_Tickers = [x.strip() for x in lines]

#Create a python dictionary with the reset hypescores of all the stocks
Tickers = {}
for Ticker in Candidate_Tickers:
    Tickers[Ticker] = 0


class StdOutListener(StreamListener):

    def __init__(self, configurationFilePath):
        #Load configuration file in memory once with the constructor.
        with open(configurationFilePath, 'r') as f:
            Data = f.read()
            self.Configuration_Object = json.loads(Data)

        self.Hypescore_Formula = self.Configuration_Object['Hypescore_Formula']

    def on_data(self, data):
        print(data)
 
        #Update the 'TickerScores' File
        with open(TickerScoresFilePath.format(Date = date), 'w') as f:
            json.dump(Tickers, f)


        #Finding user data and tweet text within the json output
        Tweet_Object = json.loads(data)
        user = Tweet_Object['user'] 
        text = (Tweet_Object['text'])
        followers = user['followers_count']
        
        #Determining the influence factor by finding the hypescore formula in the configuration        
        Hypescore = followers/self.Hypescore_Formula 

        
        
        #PROBLEM!!!! This function is defined every time we get a new tweet.
        #Tweet Object, Hypescore and followers variables ^^^ are needed for this function but they cannot leave the on_data function because they rely on the data from the tweet.
        def Update_Ticker_Sentiment(Ticker, text):

            Tweet_Sentiment = TextBlob(text).sentiment.polarity
            if Tweet_Sentiment > 0: #If Sentiment is Positive
                Tickers[Ticker] = Tickers[Ticker] + Hypescore #Add the Hypescore to the total

            if Tweet_Sentiment < 0: #If Sentiment is Negative
                Tickers[Ticker] = Tickers[Ticker] - Hypescore #Subtract the Hypescore to the total
            
            if Tweet_Sentiment == 0: #If Sentiment is neutral
                Tickers[Ticker] = Tickers[Ticker] + Hypescore #Add the Hypescore to the total


        #Print text of the tweet
        print(text)

        #Determine what company the tweet refers to with the first 100 characters
        try:
            print("\nLooking for full tweet text under retweeted status")
            full_text = Tweet_Object['retweeted_status']["extended_tweet"]['full_text']
            Tweet_text = full_text
        except:
            print("\nFull text in the retweeted status not found")
            try:
                print("\nLooking for full tweet under extended tweet")
                full_text = Tweet_Object["extended_tweet"]['full_text']
                Tweet_text = full_text
            except:
                print("\nFull text in the extended tweet not found")
                Tweet_text = text


        for word in Tweet_text.split():

            for Ticker in Candidate_Tickers:

                if word.find(Ticker.upper()) != -1:
                    print("\nThis tweet is talking about", Ticker)
                    Update_Ticker_Sentiment(Ticker, Tweet_text)

                elif word.find(Ticker.lower()) != -1:
                    print("\nThis tweet is talking about", Ticker)
                    Update_Ticker_Sentiment(Ticker, Tweet_text)

        return True

    def on_error(self, status):
        print(status)

#Authentication
if __name__ == "__main__":
    listener = StdOutListener('Configuration.json')
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)


    print(Candidate_Tickers)


    stream.filter(track=Candidate_Tickers)
