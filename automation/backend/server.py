# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import threading

from depot.automation.communication import server
from depot.automation.controllers import board
from depot.automation.controllers import services
from depot.automation.controllers import thermostat_service

def HandleMessage(bc, msg, conn):
  try:
    rtn = bc.HandleMessage(msg)
    if rtn:
      rtn.SendOverSocket(conn)
  finally:
    conn.close()

if __name__ == '__main__':
  birdhouse = board.Board('The Birdhouse')

  # Define board services
  birdhouse.AddService(services.OutletService(name='Lamp', pin=12))
  heater_outlet = services.OutletService(name='Heater', pin=16)
  birdhouse.AddService(thermostat_service.Thermostat(name='Bedroom', outlet=heater_outlet))

  # Define hooks
  birdhouse.AddHook('returned_home')

  # Define hook handler
  def HookHandler(hook, board):
    if hook == 'returned_home':
      board['Lamp'].TurnOn()

  bc = board.BoardController(birdhouse)
  bc.hook_handler = HookHandler

  s = server.MessageServer(port=14025)
  s.Start()

  while True:
    msg, conn = s.GetMessage()
    t = threading.Thread(target=HandleMessage, args=(bc, msg, conn))
    t.daemon = True
    t.start()
