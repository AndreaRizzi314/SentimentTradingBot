from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
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

    ############################################
    with open(r'Research\MoreTickers.txt', 'r') as f:
        lines = f.readlines(1663)

        lines = [x.strip() for x in lines]
        string = '#'
        my_new_list = [string + x for x in lines]


    print(my_new_list)
    ############################################




    stream.filter(track=lines)
