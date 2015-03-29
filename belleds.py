#!/usr/bin/env python3

# Python implementation of the Belleds API
# Tested on firmware rev. mb8800_v1.0.0_r389
# (http://belleds.com/en/download.html)

# By Dheera Venkatraman (http://dheera.net/)

import socket, sys, json, time, binascii
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

  color = (0,0,0)
  brightness = 255

  def __repr__(self):
    return '[Light]'

  def __init__(self, belleds_device, params = {}):
    self.belleds_device = belleds_device

    # Uncomment if in the future the Belleds device actually reports the
    # state of its parameters via lights_list. For now it reports
    # r=0 g=0 b=0 bright=0 on startup rather than the actual state
    # of the system, so for now we manually initialize to hardcoded values.
    # self.__color = (int(params.get('r', 255)),
    #              int(params.get('g', 255)),
    #              int(params.get('b', 255)))
    # self.__brightness = int(params.get('bright', 100)*255.0/100)

    self.__color = (255, 255, 255)
    self.__brightness = 255
    self.__params = params

  @property
  def color(self):
    return self.__color

  @color.setter
  def color(self, color):
    if type(color) is str and color[0]=='#' and (len(color)==7 or len(color)==9):
      self.color = binascii.unhexlify(color[1:])

    if len(color) == 4:
      self.__color = (color[0], color[1], color[2])
      self.__brightness = color[3]
      self.update()
    elif len(color) == 3:
      self.__color = color
      self.update()

  @property
  def brightness(self):
    return self.__brightness

  @brightness.setter
  def brightness(self, brightness):
    self.__brightness = brightness
    self.update()

  def update(self):
    cmd = {
      "cmd":"light_ctrl",
      "r": self.__color[0],
      "g": self.__color[1],
      "b": self.__color[2],
      "bright": int(100.0*self.__brightness/255),
      "effect": "9",
      "iswitch": "0" if self.__brightness == 0 else "1",
      "matchValue": "0",
      "sn_list": [ { "sn": self.__params['sn'] } ],
    }

    if cmd['r'] == 0 and cmd['g'] == 0 and cmd['b'] == 0:
      cmd['effect'] = "8"

    if "ok" not in self.belleds_device.dispatch_cmd(cmd):
      raise ConnectionError("light control unsuccessful")
