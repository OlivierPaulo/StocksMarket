import os
import requests
import json
import pandas as pd
from Telegram.sendmarkdown import SendMarkdown

stocks = pd.read_csv("data/stocks.csv")

url = 'https://cloud.iexapis.com/stable/stock/market/batch'

parameters = {
  'symbols': ",".join([symbol for symbol in stocks.symbol]),  ## Retrieve the ID of each crypto to pass them as argument in the API call
  'token': os.environ.get('IEX_TOKEN'),
  'types': 'quote'
}

response = requests.get(url=url, params=parameters)
api_result = response.json()

def trade_action(latest_trade_price, current_price):
  if current_price <= latest_trade_price / 1.1:
    return "Buy"
  elif current_price >= latest_trade_price * 1.1:
    return "Sell"
  else:
    return "Hodl" 

chat_id = "509161525"
telegram_token = os.environ.get('TELEGRAM_API_TOKEN')

for ix, symbol in stocks.symbol.iteritems():
  stocks.loc[ix, "current_price"] = round(api_result[str(symbol)]["quote"]["latestPrice"],2)
  stocks.loc[ix, "action"] = trade_action(stocks.loc[ix, "latest_trade_price"], stocks.loc[ix, "current_price"])
  if stocks.loc[ix, "action"] != "Hodl":
    current_price = str(stocks.loc[ix, 'current_price']).replace('.',',')
    text = f"*Alert {stocks.loc[ix, 'action']}* `{stocks.loc[ix, 'name']}` _@ {current_price}$_ per *{stocks.loc[ix, 'symbol']}*"
    SendMarkdown(chat_id=chat_id, text=text, token=telegram_token)
    stocks.loc[ix, "latest_trade_price"] = stocks.loc[ix, "current_price"]
    stocks.loc[ix, "buy_price"] = round(stocks.loc[ix, "latest_trade_price"] / 1.1, 2)
    stocks.loc[ix, "sell_price"] = round(stocks.loc[ix, "latest_trade_price"] * 1.1, 2)
    text2 = f"Next trade for ```{stocks.loc[ix, 'symbol']}```:\n*Buy* price : _{str(stocks.loc[ix, 'buy_price']).replace('.',',')}$_ \n*Sell* price : _{str(stocks.loc[ix, 'sell_price']).replace('.',',')}$_"
    SendMarkdown(chat_id=chat_id, text=text2, token=telegram_token)

stocks.to_csv("data/stocks.csv", index=False)