from depot.automation.communication import server
from depot.automation.controllers import board
from depot.automation.controllers import services

if __name__ == '__main__':
  birdhouse = board.Board('The Birdhouse')
  birdhouse.AddService(services.OutletService(name='Lamp', pin=12))
  birdhouse.AddService(services.OutletService(name='Heater', pin=16))
  bc = board.BoardController(birdhouse)
  s = server.MessageServer(port=14025)
  s.Start()

  while True:
    msg, conn = s.GetMessage()
    rtn = bc.HandleMessage(msg)
    if rtn:
      rtn.SendOverSocket(conn)
    conn.close()
