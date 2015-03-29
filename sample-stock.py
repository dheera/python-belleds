#!/usr/bin/env python3

# Makes your light green if Google stock goes up
# and red if Google stock goes down

from belleds import Belleds
from time import sleep
import json
import urllib.request

WATCH_SYMBOL = "GOOG"

b = Belleds()
b.connect('192.168.1.139')
lights = b.get_lights()

def get_quote(ticker_symbol):
  url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22' + ticker_symbol + '%22)&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
  request = urllib.request.urlopen(url)
  try:
    data = json.loads(request.read().decode('utf-8'))
    return data.get('query').get('results').get('quote')
  except:
    print("Could not retrieve quote")
    return None
  
quote = get_quote("GOOG")
if quote:
  price = float(quote.get('LastTradePriceOnly', 0))
  change = float(quote.get('Change', 0))
  if change > 0:
    for light in lights:
      light.color = (0, 255, 0)
  elif change < 0:
    for light in lights:
      light.color = (255, 0, 0)
  else:
    for light in lights:
      light.color = (255, 255, 255)

