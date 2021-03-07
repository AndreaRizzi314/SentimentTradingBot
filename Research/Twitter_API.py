from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
ACCESS_TOKEN = "1266316636417597441-7af7z1PJTOJyedrXW6YssFBTewiguX"
ACCESS_TOKEN_SECRET = "Jftf5rmkEXYewC2MEqfjJTfwVIigW2rLtT4xLx9jcDL0Y"
CONSUMER_KEY = "6Eopq3NQLbDFwsOEXQaEAcr1k"
CONSUMER_SECRET = "oQziCsy97HPoOnbvlLOkYw38ad7VjcB7oCwPzEZjKb46FYsDRW"
h = 0
List = ('Tesla', 'Microsoft', 'Apple', 'Google')








class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        global h
        
        
        # HypeScore Formula (Per/Tweet) = UserFollowers / 100
        Object = json.loads(data)
        user = Object['user'] 
        h = (Object['text'])
        # h = (h + (user['followers_count'])/100)
        print (h)
        


        return True
        


    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    
    # ############################################
    # with open('Bot/S&P500Tickers.txt') as f:
    #     lines = f.readlines(1663)

    # lines = [x.strip() for x in lines]
    # string = '#'
    # my_new_list = [string + x for x in lines]


    # print(my_new_list)
    # ############################################




    stream.filter(track=['Tesla', 'Microsoft', 'Google'])
    
    
