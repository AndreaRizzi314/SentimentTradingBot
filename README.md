# SentimentTradingBot
## Overview of the project
This project is about how social media affects the stockmarket and if it can be a profitable source of information to base a trading bot on.

## Architecture  
This project is made up of several components. 

### Twitter Analyzer Bot
This bot streams all the tweets with a certain keyword or ticker symbol and weighs its influence factor.\
Text from every tweet will run through sentiment analysis and it will determine if the tweet's HypeScore(Based on the influence) should be added or subtracted to the overall hypescore of that stock.\
To avoid the most popular stocks always having the highest hypescore the bot divides the hypescore by the amount of tweets about that stock, this way it can find the average\
All of the data collected by the bot is written into a daily 'TickerScore' file that can be later used by the Buying Bot


### Investing Bot
There are two sections to this bot: \
The first is the social based buying component. The bot will sort the data within the 'TickersScores' file and make buying decisions based on the stocks with the highest scores.\
The second section is the random bot, this is where the data from the 'TickerScores' file is shuffled and randomised and then used to buy stocks.\
Diversification is declared in the Configuration file and is followed by both the bots.The only difference between the two sections is the data used to make the buying decisions.
\
\
The Investing Bot also places a Trailing Stop-Loss after placing a buy order. A trailing stop-loss increases as the price of a stock increases but if the stock goes below a certain threshold it will sell. This is used to maximise our profits

### Launching the Investing bot
To launch the investing bot in Random mode, execute the following command at the command line:
```
<Python Install Folder path>/python.exe <repo clone folder path>/SentimentTradingBot/InvestingBot/InvestingBot.py Random
```
To launch the investing bot in Social mode, execute the following command at the command line:

```
<Python Install Folder path>/python.exe <repo clone folder path>/SentimentTradingBot/InvestingBot/InvestingBot.py Social
```
**Note**: \
Replace the following with your appropriate paths:

```<Python Install Folder path>``` should be the path where you installed Python

```<repo clone folder path>``` should be the path where you cloned the project repo

### Environment Variables 
The access token and access token secret for the twitter api are under the names: ACCESS_TOKEN & ACCESS_TOKEN_SECRET\
The consumer key and consumer secret are also under the names: CONSUMER_KEY & CONSUMER_SECRET\

\
For this project I made two accounts with Alpaca so that I could use both the random and social based bots to compare them. The names of these environment variables are as follows:\
RANDOM_ALPACA_KEY & RANDOM_ALPACA_SECRET\
SOCIAL_BASED_ALPACA_KEY & SOCIAL_BASED_ALPACA_SECRET

To obtain your own credentials for the Twitter Api go to: <https://developer.twitter.com/en>\
To obtain your own credentials for the Alpaca Api go to: <https://alpaca.markets/>

### Known issues:
1. At the moment I cannot deal with tweets that have imbeded references to other tweets. For now, those tweets are ignored
2. Some tweets given by the api are in different languages and cannot be translated at the moment, these tweets will also be ignored
3. On occasion, twitter gives the bot tweets that have nothing to do with the keywords that were provided