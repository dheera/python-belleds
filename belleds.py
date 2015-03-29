#!/usr/bin/env python3

# Python implementation of the Belleds API
# Tested on firmware rev. mb8800_v1.0.0_r389
# (http://belleds.com/en/download.html)

import socket, sys, json, time
from requests.exceptions import ConnectionError

class Belleds:

  def __repr__(self):
    return '[Belleds]'

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  host = ''
  port = 11600

  def connect(self, host, port = 11600):
    self.host = host
    self.port = port

  def get_lights(self):
    cmd = { "cmd":"light_list" }
    output = self.dispatch_cmd(cmd)

    try:
      data = json.loads(self.dispatch_cmd(cmd))
      return [ Light(self, led['sn']) for led in data.get('led',[]) ]

    except ValueError:
      raise ConnectionError("invalid response returned")


  def dispatch_cmd(self, cmd):
    try :
      self.s.sendto(json.dumps(cmd).encode('utf-8'), (self.host, self.port))
      d = self.s.recvfrom(1024)
      reply, addr = d[0], d[1]
      return reply.decode('utf-8')

    except socket.error:
      raise ConnectionError('connection error')

class Light:

  def __init__(self, belleds_device, sn):
    self.belleds_device = belleds_device
    self.sn = sn

  def set(self, color = (255,255,255), brightness = 100):
    cmd = {
      "cmd":"light_ctrl",
      "r": int(color[0]),
      "g": int(color[1]),
      "b": int(color[2]),
      "bright": int(brightness),
      "effect": "9",
      "iswitch": "1" if brightness > 0 else "0",
      "matchValue": "0",
      "sn_list": [ { "sn": self.sn } ],
    }

    if "ok" not in self.belleds_device.dispatch_cmd(cmd):
      raise ConnectionError("light control unsuccessful")
