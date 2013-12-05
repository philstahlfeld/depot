import sys
import socket
import marshal

MAX = 5

class _Message(object):

  def __init__(self):
    self._pass = ''

  def SendOverSocket(self, s):
    # Send length of the Message
    serial = marshal.dumps(self)
    s.send(str(len(serial)).zfill(5))

    s.send(serial)

def ReceiveOverSocket(s):
  msgLen = int(s.recv(5))

  buf = ""
  while len(buf) < msgLen:
      buf += s.recv(512)

  return marshal.loads(buf)


class ServiceMessage(_Message):

  def __init__(self, service_name):
    super(ServiceMessage, self).__init__()
    self.service_name = service_name

class BoardMessage(_Message):
  pass
