#!/usr/bin/env python3

# Natural Language Processing example performing
# sentiment analysis and setting a Belleds light to
# a color matching sentiment.
#
# Example usage:
# echo "I hate you and I'm having a terrible day" | ./sample-sentiment.py
# => user is angry, light turns red
# echo "I love chocolate. So awesome!" | ./sample-sentiment.py
# => user is happy, light turns green

from belleds import Belleds
import json
import sys
import urllib.request, urllib.parse

# main code

b = Belleds()
b.connect('192.168.1.139')
lights = b.get_lights()

text = "".join(sys.stdin.readlines())

params = urllib.parse.urlencode({'text': text })
request = urllib.request.urlopen("http://text-processing.com/api/sentiment/", params.encode('utf-8'))
data = json.loads(request.read().decode('utf-8'))
print(data)
r = int(data.get('probability',{}).get('neg',1)*255)
g = int(data.get('probability',{}).get('pos',1)*255)
b = int(data.get('probability',{}).get('neutral',1)*255)

for light in lights:
  light.set(color = (r, g, b), brightness = 100)
