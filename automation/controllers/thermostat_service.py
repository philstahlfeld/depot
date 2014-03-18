# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import threading
import time

from depot.automation.controllers import service
from depot.automation.controllers.utils import thermometer
from depot.utils import logging


THERMOSTAT = service.ServiceFlavor('thermostat')


class Thermostat(service.Service):
  """Wraps an outlet service to control a heater."""

  def __init__(self, name, outlet, target=70):
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
    return int(thermometer.GetTemperature())

  def Status(self):
    outlet = self._outlet.Status()
    temp = self.GetTemperature()
    return (temp, self._target, outlet)

  def _ControlOutlet(self):
    while True:
      self._DoControl()
      if self._stop:
        return
      output = 'target: %s, temp: %s' % (thermometer.GetTemperature(), self._target)
      logging.Info('thermostat.log', output)
      time.sleep(5)

  def _DoControl(self):
    """Keep temperature in a 5 degree window."""
    temp = self.GetTemperature()
    if temp > self._target + 2.5:
      self._outlet.TurnOff()
    elif temp < self._target - 2.5:
      self._outlet.TurnOn()



