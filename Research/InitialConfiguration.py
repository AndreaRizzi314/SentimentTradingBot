import json

Config_Dict = {
    'Hypescore_Formula': 1000,  #HYPESCORE: followers/?
    'Risk_Tolerance': 1,        #DIVERSIFICATION: Number between 1-5 (1 = buy 5 stocks)(5 = buy 1 stock)
    'Stop_Loss': 2              #WHEN TO SELL(%): Sell when ?% below day highs    
}

with open('Configuration.json', 'w') as f:
    json.dump(Config_Dict, f)


with open('Configuration.json', 'r') as f:
    Data = f.read()
    Object = json.loads(Data)
    print(Object['Hypescore_Formula'])