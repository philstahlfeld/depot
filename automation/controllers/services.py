from depot.automation.controllers import rpi_service
from depot.automation.controllers import service


SWITCHABLE = service.ServiceFlavor('switchable')

class OutletService(rpi_service.GPIOService):

  def __init__(self, name, pin):
    super(OutletService, self).__init__(name=name, flavor=SWITCHABLE)
    self._pin = pin
    self.gpio.setmode(self.gpio.BOARD)
    self.gpio.setup(self._pin, self.gpio.OUT)
    self.TurnOff()

  def TurnOff(self):
    self.gpio.output(self._pin, self.gpio.LOW)

  def TurnOn(self):
    self.gpio.output(self._pin, self.gpio.HIGH)

  def Toggle(self):
    self.gpio.output(self._pin, not self.Status())

  def Status(self):
    return self.gpio.input(self._pin)


if __name__ == '__main__':
  outlet = OutletService(name='Test Outlet', pin=12)
  raw_input()
  outlet.TurnOn()
  print outlet.Status()
  raw_input()
  outlet.TurnOff()
  print outlet.Status()
  print outlet.name
  print outlet.flavor
