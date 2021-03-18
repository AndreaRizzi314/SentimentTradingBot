from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

List = ('Tesla', 'Microsoft', 'Apple', 'Google')

Tickers = {
    'TSLA' : 0,
    'AAPL' : 0
} 


                                                                                                                                                                    
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)



        with open('Research/TickerScores.json', 'w') as f:
            json.dump(Tickers, f)



        Object = json.loads(data)
        user = Object['user'] 
        text = (Object['text'])
        followers = user['followers_count']
        

        #Determining the influence factor
        with open('Configuration.json', 'r') as f:
            Data = f.read()
            Object = json.loads(Data) 
        Hypescore = followers/Object['Hypescore_Formula']



        print(text)
        for word in text.split():
            if word.find('TSLA') == -1:
                pass
            else:
                Tickers['TSLA'] = Tickers['TSLA'] + Hypescore
                print('Tesla')

            if word.find('AAPL') == -1:
                pass
            else:
                Tickers['AAPL'] = Tickers['AAPL'] + Hypescore
                print('Apple')

            if word.find('CRSR') == -1:
                pass
            else:
                Tickers['CRSR'] = Tickers['CRSR'] + Hypescore
                print('Corsair')

            if word.find('BYND') == -1:
                pass
            else:
                Tickers['BYND'] = Tickers['BYND'] + Hypescore
                print('Beyond Meat')

            if word.find('SPCE') == -1:
                pass
            else:
                Tickers['SPCE'] = Tickers['SPCE'] + Hypescore
                print('Virgin Galactic')

        return True



    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)

    ############################################
    with open(r'Research\MoreTickers.txt', 'r') as f:
        lines = f.readlines(1663)

        lines = [x.strip() for x in lines]
        string = '#'
        my_new_list = [string + x for x in lines]


    print(my_new_list)
    ############################################




    stream.filter(track=lines)
