# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

from depot.automation.communication import message

class ServicesMessage(message.BoardMessage):

  def __init__(self):
    self.services = {}

  def AddService(self, name, flavor):
    self.services[name] = flavor
