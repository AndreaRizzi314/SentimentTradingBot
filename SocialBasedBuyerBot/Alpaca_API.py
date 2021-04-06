import alpaca_trade_api as Trade_api
import os
import math
import json
import time
import requests
from datetime import date
import sys

date = date.today()

KEY = os.environ.get('ALPACA_KEY')
SECRET = os.environ.get('ALPACA_SECRET')
alpaca_endpoint = "https://paper-api.alpaca.markets"

Orders_url = "{}/v2/orders".format(alpaca_endpoint)
Headers = {"APCA-API-KEY-ID": KEY, "APCA-API-SECRET-KEY": SECRET}

Bot_Data_Ticker_File_Path = "BotData/TickerScores{Date}.json"
Daily_Log_Ticker_File_Path = "DailyLogs/Daily_Log_{Date}.txt"

#Open the Configuration file
with open('Configuration.json', 'r') as f:
    Data = f.read()
    Configration_Object = json.loads(Data)

#Open the TickerScores File
try:
    with open(Bot_Data_Ticker_File_Path.format(Date = date), 'r') as f:
        data = json.load(f)
#If there is an error with opening the new TickerScores file then end the program
except:
    print("\nThe TickerScores file has not been updated\n")
    sys.exit()

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
    #How many shares can you buy with your money (Input: Price of one share)
    price = price * 0.98
    if price == 0:
        return 0
    else:
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
    if clock.is_open:
        return 1
    else:
        return 0
def HistoricalPrice():

    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset('AAPL', 'day', limit=5)
    aapl_bars = barset['AAPL']

    # See how much AAPL moved in that timeframe.
    week_open = aapl_bars[0].o
    week_close = aapl_bars[-1].c
    percent_change = (week_close - week_open) / week_open * 100
    print('AAPL moved {}% over the last 5 days'.format(percent_change))
def Buy_Order_In_Shares(SYMBOL, QTY):
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Submit a market order to buy 1 share of a stock at market price
    api.submit_order(
        symbol= SYMBOL,
        qty= QTY,
        side='buy',
        type='market',
        time_in_force='day'
    )
def Buy_Order_In_Dollars(SYMBOL, QTY):
    #Makeing a raw request for access to fractional shares  
    data = {
        "symbol": SYMBOL,
        "notional": QTY,
        "side": "buy",
        "type": "market",
        "time_in_force": "day"
    }

    r = requests.post(Orders_url, json=data, headers=Headers)
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
    print(quote.bidprice)
    return quote.bidprice
def Sell_Order(SYMBOL, QTY):
    #Makeing a trailing stop order with the target percentage listed in the configuration file
    Percentage = str(Configration_Object['Stop_Loss'])

    api.submit_order  (
        symbol= SYMBOL,
        qty= QTY,
        side= "sell",
        type= "trailing_stop",
        trail_percent= Percentage,
        time_in_force= "day"
    )



Buying_power = Get_Buying_Power() # Buying power in the account including money that can be taken out on margin
Stock_List_Position = 0  # Position of the items in the sorted list of keys starting with the highest stock on the list 


for Stock_List_Position in range(0, Configration_Object["Diversification"]):
    #Dividing the total buying power by the amount of stocks that will be bought depending on the diversification.
    Individual_Stock_Money = float(Buying_power)/ float(Configration_Object['Diversification']) - float(.01)
    #Making a buy order for each stock
    Buy_Order_In_Dollars(sorted_list_keys[Stock_List_Position], Individual_Stock_Money)
    #Listing the buy orders in the Daily logs 
    with open(Daily_Log_Ticker_File_Path.format(Date = date), 'a') as f:
        Read = ("\n{}\nBuy Order:{} dollars of {} stock").format(date, Individual_Stock_Money, sorted_list_keys[Stock_List_Position])
        f.write(Read) 




