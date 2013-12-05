from depot.automation.communication import server
from depot.automation.controllers import board
from depot.automation.controllers import services

if __name__ == '__main__':
  birdhouse = board.Board('The Birdhouse')
  birdhouse.AddService(services.OutletService(name='Bedroom', pin=12))
  birdhouse.AddService(services.OutletService(name='Outlet4', pin=16))
  bc = board.BoardController(b)
  s = server.MessageServer(port=14025)
  s.Start()

  while True:
    msg = s.GetMessage()
    bc.HandleMessage(msg)
