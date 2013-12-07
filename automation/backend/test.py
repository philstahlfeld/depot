from depot.automation.communication import action_message
from depot.automation.communication import message
from depot.automation.communication import services_message
from depot.automation.communication import status_message
from depot.automation.controllers import board
from depot.automation.controllers import services
import socket


if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('10.1.10.18', 14025))
  msg = services_message.ServicesMessage()
  msg.SendOverSocket(s)
  msg = message.ReceiveOverSocket(s)
  print msg.services
  s.close()
