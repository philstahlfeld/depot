import sys
import socket
import pickle

class _Message(object):

  def __init__(self):
    self._pass = ''

  def SendOverSocket(self, s):
    # Send length of the Message
    serial = pickle.dumps(self)
    s.write(str(len(serial)).zfill(4))

    s.send(serial)

def RecieveOverSocket(s):
  msgLen = int(s.recv(4))

  buf = ""
  while len(buf) < msgLen:
      buf += s.read()

  return pickle.loads(buf)


class ServiceMessage(_Message):

  def __init__(self, service_name):
    super(ServiceMessage, self).__init__()
    self.service_name = service_name

class BoardMessage(_Message):
  pass
