#!/usr/bin/env python3

# Makes your light green if Google stock goes up
# and red if Google stock goes down

from belleds import Belleds
from time import sleep
import json
from pprint import pprint
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
    print("foo")
    return None
  
while True:
  quote = get_quote("GOOG")
  if quote:
    price = float(quote.get('LastTradePriceOnly'))
    change = float(quote.get('Change'))
    if change > 0:
      for light in lights:
        light.set(color = (0, 255, 0), brightness = 100)
    elif change < 0:
      for light in lights:
        light.set(color = (255, 0, 0), brightness = 100)
    else:
      for light in lights:
        light.set(color = (255, 255, 255), brightness = 100)
  sleep(30)


# a MATLAB-like jet color map
def jet(v, vmin, vmax):
   c = [1.0, 1.0, 1.0]
   v = max(v, vmin)
   v = min(v, vmax)
   dv = vmax - vmin
   if (v < (vmin + 0.25 * dv)):
      c[0] = 0;
      c[1] = 4 * (v - vmin) / dv;
   elif (v < (vmin + 0.5 * dv)):
      c[0] = 0;
      c[2] = 1 + 4 * (vmin + 0.25 * dv - v) / dv;
   elif (v < (vmin + 0.75 * dv)):
      c[0] = 4 * (v - vmin - 0.5 * dv) / dv;
      c[2] = 0;
   else:
      c[1] = 1 + 4 * (vmin + 0.75 * dv - v) / dv;
      c[2] = 0;

   c[0] = int(255*c[0])
   c[1] = int(255*c[1])
   c[2] = int(255*c[2])
   return(tuple(c))

# main code

b = Belleds()
b.connect('192.168.1.139')
lights = b.get_lights()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

last_100 = deque()
last_5 = deque()

while True:
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)
    last_100.append(rms)
    last_5.append(rms)
    if len(last_100)>100:
      last_100.popleft()
    if len(last_5)>5:
      last_5.popleft()
    score = 100./5. * sum(last_5) / sum(last_100)
    score = min(4,score)
    score = max(0.25,score)
    if score>2:
      r = max(255, (score/2)*255)
      g = 0
      b = 0
    elif score<0.5:
      r = 0
      g = 0
      b = max(255, (score-0.5)*255)

    color = jet(score, 0.75, 1.33)
    print(str('=' * int(10*score)) + ' ' * 20, end="\r")

    for light in lights:
      light.set(color = color, brightness = 100)

