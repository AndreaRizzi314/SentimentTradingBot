import alpaca_trade_api as Trade_api
import os

KEY = os.environ.get('ALPACA_KEY')
SECRET = os.environ.get('ALPACA_SECRET')

alpaca_endpoint = "https://paper-api.alpaca.markets"

api = Trade_api.REST(KEY, SECRET, alpaca_endpoint)

account = api.get_account()
print(account.status)