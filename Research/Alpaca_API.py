import alpaca_trade_api as Trade_api

alpaca_endpoint = "https://paper-api.alpaca.markets"

api = Trade_api.REST("PKHHGP9WE0PA0XVF54F1", "kXrrs6fYqbCouDvNlkWhIjH82QF4tc48pKaYXvvR", alpaca_endpoint)

account = api.get_account()
print(account.status)