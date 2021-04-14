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
    if price == 0:
        return 0
    else:
        quantity = math.floor(Buying_Power / price)
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
    #Making a raw request for access to fractional shares  
    data = {
        "symbol": SYMBOL,
        "notional": QTY,
        "side": "buy",
        "type": "market",
        "time_in_force": "day"
    }

    r = requests.post(Orders_url, json=data, headers=Headers)
def Get_Portfolio():
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Get a list of all of our positions.
    portfolio = api.list_positions()
     
    return portfolio
def Amount_Of_Positions():
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Get a list of all of our positions.
    portfolio = api.list_positions()
    Number_Of_Positions = 0
    # Print the quantity of shares for each position.
    for position in portfolio:
        Number_Of_Positions += 1
    return Number_Of_Positions
def Live_Price(symbol):
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)
    symbol_bars = api.get_barset(symbol, 'minute', 1).df.iloc[0]
    symbol_price = symbol_bars[symbol]['close']
    return symbol_price
def Sell_Order(SYMBOL, QTY):
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)
    #Making a trailing stop order with the target percentage listed in the configuration file
    Percentage = str(Configration_Object['Stop_Loss'])

    api.submit_order  (
        symbol= SYMBOL,
        qty= QTY,
        side= "sell",
        type= "trailing_stop",
        trail_percent= Percentage,
        time_in_force= "gtc"
    )
        

Diversification = Configration_Object["Diversification"]
Number_Of_Current_Positions = Amount_Of_Positions()
Number_Of_Desired_Positions = Diversification
Positions_Left_To_Buy = Number_Of_Desired_Positions - Number_Of_Current_Positions


for i in range(0, Positions_Left_To_Buy):
    Buying_power = Get_Buying_Power() #Buying power in the account including money that can be taken out on margin
    
    #Dividing the total buying power by the amount of stocks that will be bought depending on the diversification.
    Individual_Stock_Money = float(Buying_power)/ float(Positions_Left_To_Buy)* 0.995

    Stock_List_Position = 0  # Position of the items in the sorted list of keys, always starts from the top

    while True:

        Symbol_To_Evaluate_Buying = sorted_list_keys[Stock_List_Position]

        #This is making a list of all open positions we have in the account 
        List_of_current_position_symbols = []
        Portfolio = Get_Portfolio()
        for position in Portfolio:
            List_of_current_position_symbols.append(position.symbol)

        Can_I_Buy_This_Ticker = True
        #Determining if the ticker that was chosen is already an existing position
        for ticker in List_of_current_position_symbols:
            if ticker == Symbol_To_Evaluate_Buying:
                Can_I_Buy_This_Ticker = False
                break
            else:
                Can_I_Buy_This_Ticker = True
        
        #If the ticker was already used then increase the Stock_List_Position by 1 and try again with the next item in the list
        if Can_I_Buy_This_Ticker == False:
            Stock_List_Position += 1

        else:
            Price = Live_Price(Symbol_To_Evaluate_Buying)
            QTY = Calculate_Quantity(Price, Individual_Stock_Money)
            #Making a buy order for each stock
            Buy_Order_In_Shares(Symbol_To_Evaluate_Buying, QTY)
            #Waiting for the order to be filled
            time.sleep(10)
            #Making a sell order for each stock
            Sell_Order(Symbol_To_Evaluate_Buying, QTY)
            Positions_Left_To_Buy -= 1
            break


print(Stock_List_Position)

Diversification = Configration_Object["Diversification"]
Number_of_Stocks = len(sorted_list_keys)




##The purpose of this loop is to keep the number of positions equal to the diversification
##This loop will look at our positions every minute and check if anything sold, If something sold, then it will buy the next stock in the list
while True:
    Number_Of_Current_Positions = Amount_Of_Positions()
    Number_Of_Desired_Positions = Diversification
    Positions_To_Be_Filled = Number_Of_Desired_Positions - Number_Of_Current_Positions
    #If we have the same amount of positions as the preset diversification then wait 1 minute
    if Number_Of_Current_Positions == Diversification:
        time.sleep(60)
    else:

        Buying_Power = Get_Buying_Power()


        for i in range(0, Positions_To_Be_Filled):
            Buying_power = Get_Buying_Power()
            Individual_Stock_Money = float(Buying_power)/ float(Positions_To_Be_Filled)* 0.995
            # Stock_List_Position = 0  # Position of the items in the sorted list of keys, always starts from the top
            Stock_List_Position += 1
            
            while True:
                Symbol_To_Evaluate_Buying = sorted_list_keys[Stock_List_Position]

                #This is making a list of all open positions we have in the account
                List_of_current_position_symbols = []
                Portfolio = Get_Portfolio()
                for position in Portfolio:
                    List_of_current_position_symbols.append(position.symbol)

                Can_I_Buy_This_Ticker = True
                #Determining if the ticker that was chosen is already an existing position
                for ticker in List_of_current_position_symbols:
                    if ticker == Symbol_To_Evaluate_Buying:
                        Can_I_Buy_This_Ticker = False
                        break
                    else:
                        Can_I_Buy_This_Ticker = True
                
                #If the ticker was already used then increase the Stock_List_Position by 1 and try again with the next item in the list
                if Can_I_Buy_This_Ticker == False:
                    Stock_List_Position += 1
                    if Stock_List_Position == Number_of_Stocks:
                        sys.exit()#Close the program if the Stock_List_Position reaches more than the items in the list


                else:
                    
                    Price = Live_Price(Symbol_To_Evaluate_Buying)#Live Price of the Ticker that we are evaluating
                    #Calculate the amount of whole shares we can buy with the price of one share and the amount of money that is allocated for this position
                    QTY = Calculate_Quantity(Price, Individual_Stock_Money)
                    #Making a buy order for each stock
                    Buy_Order_In_Shares(Symbol_To_Evaluate_Buying, QTY)
                    #Waiting for the order to be filled
                    time.sleep(10)
                    #Making a sell order for each stock
                    Sell_Order(Symbol_To_Evaluate_Buying, QTY)
                    #After Buying reduce the amount of positions that are needed to be filled by 1 
                    Positions_To_Be_Filled -= 1
                    break








