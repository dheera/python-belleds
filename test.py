#!/usr/bin/env python3

from belleds import Belleds
from time import sleep

b = Belleds()
b.connect('192.168.1.139')

lights = b.get_lights()

for light in lights:
  light.set(color = (255, 0, 0), brightness = 100)
  sleep(0.5)
  light.set(color = (0, 255, 0), brightness = 100)
  sleep(0.5)
  light.set(color = (0, 0, 255), brightness = 100)
  sleep(0.5)
  light.set(color = (255, 255, 255), brightness = 100)
  sleep(0.5)
  for i in range(1, 100):
    light.set(brightness = i)
    sleep(0.01)

  sleep(0.5)
  light.set(color = (0, 0, 0), brightness = 100)
