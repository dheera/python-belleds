#!/usr/bin/env python3

from belleds import Belleds
from time import sleep

b = Belleds()
b.connect('192.168.1.139')

lights = b.get_lights()

for light in lights:
  # Setting brightness and color independently

  light.color = (255, 0, 0)

  sleep(1)

  # You can use hex strings too

  light.color = '#0000FF'

  sleep(1)

  # Color slide

  for i in range(0, 255):
    light.color = (255-i, i, 0)
    sleep(0.01)

  sleep(1)

  # White light mode
  for i in range(0, 255):
    light.brightness = i
    sleep(0.01)

