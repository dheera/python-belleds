#!/usr/bin/env python3

# Python implementation of the Belleds API
# Tested on firmware rev. mb8800_v1.0.0_r389
# (http://belleds.com/en/download.html)

# By Dheera Venkatraman (http://dheera.net/)

import socket, sys, json, time
from pprint import pprint
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
      return [ Light(self, params = led) for led in data.get('led',[]) ]

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

  def __init__(self, belleds_device, params = {}):
    self.belleds_device = belleds_device
    self.params = params

  def set(self, color = None, brightness = None):

    if color:
      self.params['r'] = color[0]
      self.params['g'] = color[1]
      self.params['b'] = color[2]

    if brightness:
      self.params['bright'] = brightness

    cmd = {
      "cmd":"light_ctrl",
      "r": int(self.params.get('r', 255)),
      "g": int(self.params.get('g', 255)),
      "b": int(self.params.get('b', 255)),
      "bright": int(self.params.get('bright', 100)),
      "effect": "9",
      "iswitch": "0" if int(self.params.get('bright')) == 0 else "1",
      "matchValue": "0",
      "sn_list": [ { "sn": self.params['sn'] } ],
    }

    if cmd['r'] == 0 and cmd['g'] == 0 and cmd['b'] == 0:
      cmd['effect'] = "8"

    if "ok" not in self.belleds_device.dispatch_cmd(cmd):
      raise ConnectionError("light control unsuccessful")
