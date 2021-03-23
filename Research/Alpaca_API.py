import alpaca_trade_api as Trade_api
import os

KEY = os.environ.get('ALPACA_KEY')
SECRET = os.environ.get('ALPACA_SECRET')
alpaca_endpoint = "https://paper-api.alpaca.markets"


def Get_Buying_Power():
    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Get account information.
    account = api.get_account()

    # Check if our account is restricted from trading.
    if account.trading_blocked:
        print('Account is currently restricted from trading.')

    # Check how much money we have to spend
    print('${} is available as buying power.'.format(account.buying_power))
def Is_Market_Open():

    api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

    # Check if the market is open now.
    clock = api.get_clock()
    print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
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


View_Positions()