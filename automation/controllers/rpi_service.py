import atexit
from depot.automation.controllers import service


class GPIOService(service.Service):

  def __init__(self, *args, **kwargs):
    from RPi import GPIO as gpio
    self.gpio = gpio
    super(GPIOService, self).__init__(*args, **kwargs)

  @atexit.register
  def Cleanup():
    try:
      gpio.cleanup()
    except:
      pass
