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
  # color tests
  light.set(color = (255, 0, 0), brightness = 100)
  sleep(0.25)
  light.set(color = (0, 255, 0))
  sleep(0.25)
  light.set(color = (0, 0, 255), brightness = 50)
  sleep(0.25)

  # use (0, 0, 0) for white light setting
  light.set(color = (0, 0, 0), brightness = 100)
```

# More advanced examples
*sample-sentiment.py* does natural language processing on a piece of text and changes the light bulb to a color matching the feelings in the text.

*sample-stock.py* changes the color of the light bulb based on the price of Google stock

*sample-audio.py* is a crude audio analyzer using pyaudio.
