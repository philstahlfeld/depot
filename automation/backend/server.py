from depot.automation.communication import server
from depot.automation.controllers import board
from depot.automation.controllers import services
from depot.automation.controllers import thermostat_service

if __name__ == '__main__':
  birdhouse = board.Board('The Birdhouse')
  birdhouse.AddService(services.OutletService(name='Lamp', pin=12))
  heater_outlet = services.OutletService(name='Heater', pin=16)
  birdhouse.AddService(thermostat_service.Thermostat(name='Bedroom', outlet=heater_outlet))
  bc = board.BoardController(birdhouse)
  s = server.MessageServer(port=14025)
  s.Start()

  while True:
    msg, conn = s.GetMessage()
    print msg
    rtn = bc.HandleMessage(msg)
    if rtn:
      rtn.SendOverSocket(conn)
    conn.close()
