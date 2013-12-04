from depot.automation.communication import action_message
from depot.automation.communication import services_message
from depot.automation.communication import status_message
from depot.automation.controllers import board
from depot.automation.controllers import services

b = board.Board('Test Board')
s = services.OutletService(name='Test Outlet', pin=12)
b.AddService(s)

bc = board.BoardController(b)
msg = services_message.ServicesMessage()
bc.HandleMessage(msg)
print msg.services
