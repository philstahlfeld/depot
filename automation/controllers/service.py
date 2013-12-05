import atexit
try:
  import RPi.GPIO as gpio
except:
  class Mock(object):
    pass
  def cleanup():
    pass
  gpio = Mock()
  gpio.cleanup = cleanup

class Service(object):

  def __init__(self, name, flavor):
      self.name = name
      self.flavor = flavor

  def Status(self):
    raise NotImplementedError


class GPIOService(Service):

  @atexit.register
  def Cleanup():
    gpio.cleanup()


class ServiceFlavor(object):

  def __init__(self, name):
    self.name = name
