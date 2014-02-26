# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

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
