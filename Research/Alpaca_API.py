import alpaca_trade_api as Trade_api
import os
import math
import json
import time

KEY = os.environ.get('ALPACA_KEY')
SECRET = os.environ.get('ALPACA_SECRET')
alpaca_endpoint = "https://paper-api.alpaca.markets"


#Open the TickerScores File
with open(r'BotData\TickerScores2021-03-25.json', 'r') as f:
    data = json.load(f)

#Empty list 
sorted_list_keys = []

#Seperate List for the values and the keys within the dictionary
key_list = list(data.keys())
value_list = list(data.values())

#sorted list of values
sorted_values = sorted(value_list, reverse=True)

#sorted list of Keys
for number in sorted_values:
    sorted_list_keys.append(key_list[value_list.index(number)])


def Calculate_Quantity(price, Buying_Power):
    #How many whole shares can you buy with your money (Input: Price of one share)
    quantity = (Buying_Power / price)
    print(quantity)
    return quantity
def Get_Buying_Power():
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Get account information.
    account = api.get_account()

    # Check if our account is restricted from trading.
    if account.trading_blocked:
        print('Account is currently restricted from trading.')

    # Check how much money we have to spend
    # print('${} is available as buying power.'.format(account.buying_power))
    return(account.buying_power)
def Is_Market_Open():

    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Check if the market is open now.
    clock = api.get_clock()
    #print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
    if clock.is_open:
        return 1
    else:
        return 0
def HistoricalPrice():

    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset('DBX', 'day', limit=5)
    aapl_bars = barset['DBX']

    # See how much AAPL moved in that timeframe.
    week_open = aapl_bars[0].o
    week_close = aapl_bars[-1].c
    percent_change = (week_close - week_open) / week_open * 100
    print('DBX moved {}% over the last 5 days'.format(percent_change))
def Buy_Order(SYMBOL, QTY):
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Submit a market order to buy 1 share of Apple at market price
    api.submit_order(
        symbol= SYMBOL,
        qty= QTY,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
def View_Positions():
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Get a list of all of our positions.
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))
def Live_Price(Ticker):
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)
    quote = api.get_last_quote(Ticker)
    return quote.bidprice



while True:
    if Is_Market_Open() == 0:
        print("Market is closed....")
    if Is_Market_Open() == 1:
        print("Market is now open!!!")
        while True:
            
            with open('Configuration.json', 'r') as f:
                Data = f.read()
                Object = json.loads(Data) 

            Buying_power = Get_Buying_Power()

            if Buying_power > 100:

                if Object["Risk_Tolerance"] == 1:
                    Individual_Stock_Money = Buying_power/5
                
                if Object["Risk_Tolerance"] == 2:
                    Individual_Stock_Money = Buying_power/4

                if Object["Risk_Tolerance"] == 3:
                    Individual_Stock_Money = Buying_power/3

                if Object["Risk_Tolerance"] == 4:
                    Individual_Stock_Money = Buying_power/2

                if Object["Risk_Tolerance"] == 5:
                    Individual_Stock_Money = Buying_power
    time.sleep(1)