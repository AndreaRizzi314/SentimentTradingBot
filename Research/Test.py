
with open('Bot/S&P500Tickers.txt') as f:
    lines = f.readlines(1663)

lines = [x.strip() for x in lines]

string = '#'
my_new_list = [string + x for x in lines]


print(my_new_list)








# File = open("Bot/Tickers.txt", "r")
# Contents = File.readlines()
# print (Contents)
# File.close()