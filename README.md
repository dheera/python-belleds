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

  # set color and brightness together
  light.color = (255, 0, 0, 0)

  sleep(1)

  # set color only
  light.color = (0, 255, 0)

  sleep(1)

  # set brightness only

  light.brightness = 127

  sleep(1)

  # use (0, 0, 0) for white light setting
  light.color = (0, 0, 0, 255)
```

# More advanced examples
*sample-sentiment.py* does natural language processing on a piece of text and changes the light bulb to a color matching the feelings in the text.

*sample-stock.py* changes the color of the light bulb based on the price of Google stock

*sample-audio.py* is a crude audio analyzer using pyaudio.
