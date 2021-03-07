# SentimentTradingBot
## Overview of the project
This project is about how social media affects the stockmarket and if it can be a profitable source of information to base a trading bot on.

## Architecture 
This project is made up of several components. 

### Twitter Analyzer Bot
This bot reads all the tweets about a certain stock/stocks and weighs its influence factor.\
Text from every tweet will run through sentiment analysis and it will deterine if the tweet's HypeScore(Based on the influence) should be added or subtracted to the overall hypescore of that stock.\
All hypescores are sorted and written into a 'TickerScore' file 

### Seller bot
Tracks the live prices of the stocks. \
This bot checks the existing stocks in our portfolio and determines when to sell them using a stop-loss that is defined in the configuration file.

### Random buyer bot
With the list of all the stockmarket ticker symbols, this bot will randomly choose and buy stocks. It can use stop-losses but it will not have access to the 'TickerScore' File.

### Social based buyer bot
Using the information that was gathered with the Twitter Analyser Bot. This bot will read the 'TickerScore' file and buy the most 'hyped' stocks and diversify depending on the risk tollerence declared in the configuration file.