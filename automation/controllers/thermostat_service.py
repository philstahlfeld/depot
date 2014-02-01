import threading
import time

from depot.automation.controllers import service
from depot.automation.controllers.utils import thermometer


THERMOSTAT = service.ServiceFlavor('thermostat')


class Thermostat(service.Service):
  """Wraps an outlet service to control a heater."""

  def __init__(self, name, outlet, target=72):
    super(Thermostat, self).__init__(name=name, flavor=THERMOSTAT)
    self._outlet = outlet
    self._target = target  # Target temperature
    self._stop = True
    self.Start()

  def Start(self):
    self._stop = False
    t = threading.Thread(target=self._ControlOutlet)
    t.start()

  def Stop(self):
    self._stop = True

  def SetTarget(self, target):
    self._target = target

  def GetTarget(self):
    return self._target

  def GetTemperature(self):
    return 73 #thermometer.GetTemperature()

  def Status(self):
    outlet = self._outlet.Status()
    temp = self.GetTemperature()
    return (temp, self._target, outlet)

  def _ControlOutlet(self):
    while True:
      self._DoControl()
      if self._stop:
        return
      time.sleep(30)

  def _DoControl(self):
    """Keep temperature in a 5 degree window."""
    temp = self.GetTemperature()
    if temp > self._target + 2.5:
      self._outlet.TurnOff()
    elif temp < self._target - 2.5:
      self._outlet.TurnOn()



