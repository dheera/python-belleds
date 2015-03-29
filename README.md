Python Belleds API
==================

Python API for [Belleds smart LED bulbs](http://belleds.com/)

By [Dheera Venkatraman](http://dheera.net) based on documentation from the [Belleds Github repository](https://github.com/BelledsQ/QStation_API)

Sample usage:

```python
#!/usr/bin/env python3
from belleds import Belleds
from time import sleep

b = Belleds()
b.connect('192.168.1.139')

lights = b.get_lights()

for light in lights:

  # set color with RGB tuple
  light.color = (255, 0, 0)

  sleep(1)

  # use hex strings if you feel like
  light.color = '#0080CC'

  sleep(1)

  # use brightness to switch the light to white mode

  light.brightness = 127

  sleep(1)

  light.brightness = 255
```

# More advanced examples
*sample-sentiment.py* does natural language processing on a piece of text and changes the light bulb to a color matching the feelings in the text.

*sample-stock.py* changes the color of the light bulb based on the price of Google stock

*sample-audio.py* is a crude audio analyzer using pyaudio.

