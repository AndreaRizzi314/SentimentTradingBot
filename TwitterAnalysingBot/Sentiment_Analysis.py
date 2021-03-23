from textblob import TextBlob
# Sentence = input("Say a sentence: ")
Sentence2 = TextBlob("I am short on TSLA")
# textblob = TextBlob(Sentence)
print(Sentence2.sentiment)

Hypescore = 1
text = 'TSLA is an increadibly bad company'











# with open(r'Research\MoreTickers.txt', 'r') as f:
#         lines = f.readlines(1663)

#         lines = [x.strip() for x in lines]



# for word in text.split():

#             for Ticker in lines:

#                 if word.find(Ticker) == -1:
#                     pass
    
#                 else:
#                     if TextBlob(text).sentiment.polarity > 0: #If Sentiment is Positive
#                         print('+1')

#                     if TextBlob(text).sentiment.polarity < 0: #If Sentiment is Negative
#                         print('-1')
                    
#                     if TextBlob(text).sentiment.polarity == 0: #If Sentiment is neutral
#                         print('+-0')







