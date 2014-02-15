# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import sys
import socket
import pickle

MAX = 5

class _Message(object):

  def __init__(self):
    self._pass = ''

  def SendOverSocket(self, s):
    # Send length of the Message
    serial = pickle.dumps(self)
    s.send(str(len(serial)).zfill(5))

    s.send(serial)

def ReceiveOverSocket(s):
  msgLen = int(s.recv(5))

  buf = ""
  while len(buf) < msgLen:
      buf += s.recv(512)

  return pickle.loads(buf)


class ServiceMessage(_Message):

  def __init__(self, service_name):
    super(ServiceMessage, self).__init__()
    self.service_name = service_name

class BoardMessage(_Message):
  pass
