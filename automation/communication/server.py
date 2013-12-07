import socket

from depot.automation.communication import message

class MessageServer(object):

  def __init__(self, port):
    self.host = '0.0.0.0'
    self.port = port
    self.bindsocket = None

  def Start(self):
    self._bindsocket = socket.socket()
    self._bindsocket.bind((self.host, self.port))
    self._bindsocket.listen(5)

  def GetMessage(self):
    conn, (ip, port) = self._bindsocket.accept()
    print 'New connection from %s' % ip
    msg = message.ReceiveOverSocket(conn)
    return (msg, conn)


if __name__ == '__main__':
  server = MessageServer(14025)
  server.Start()
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('0.0.0.0', 14025))
  msg = message.BoardMessage()
  msg.SendOverSocket(s)
  rcv = server.GetMessage()
  print type(rcv)
