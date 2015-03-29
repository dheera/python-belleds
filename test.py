#!/usr/bin/env python3

from belleds import Belleds
from time import sleep

b = Belleds()
b.connect('192.168.1.139')

lights = b.get_lights()

for light in lights:
  # Setting brightness and color independently

  light.color = (255, 0, 0)
  light.brightness = 255

  sleep(1)

  light.color = (0, 255, 0)
  light.brightness = 127

  sleep(1)

  light.color = (0, 0, 255)
  light.brightness = 255

  sleep(1)

  # Setting brightness and color together

  light.color = (255, 255, 255, 0)
  for i in range(1, 100):
    light.color = (255, 255, 255, i)
    sleep(0.01)

  sleep(1)

  # White light mode
  light.color = (0, 0, 0, 255)


