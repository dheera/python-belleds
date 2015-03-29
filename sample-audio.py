#!/usr/bin/env python3

# Combines the python-belleds API with pyaudio
# (assuming you have it installed) to
# make a Belleds system dance to music
# This is a really silly implementation based
# on moving RMS averages. Someone should probably
# write a better version with beat detection and
# frequency analysis.

from belleds import Belleds
from collections import deque
import pyaudio
import wave
import audioop

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
      light.color = color

