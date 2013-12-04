import RPi.GPIO as gpio

from depot.automation.controllers import service


SWITCHABLE = service.ServiceFlavor('switchable')

class OutletService(service.GPIOService):

  def __init__(self, name, pin):
    super(OutletService, self).__init__(name=name, flavor=SWITCHABLE)
    self._pin = pin
    gpio.setmode(gpio.BOARD)
    gpio.setup(self._pin, gpio.OUT)
    self.TurnOff()

  def TurnOff(self):
    gpio.output(self._pin, gpio.LOW)

  def TurnOn(self):
    gpio.output(self._pin, gpio.HIGH)

  def Toggle(self):
    gpio.output(self._pin, not self.Status())

  def Status(self):
    return gpio.input(self._pin)


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
