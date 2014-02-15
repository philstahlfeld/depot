# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

class Service(object):

  def __init__(self, name, flavor):
      self.name = name
      self.flavor = flavor

  def Status(self):
    raise NotImplementedError


class ServiceFlavor(object):

  def __init__(self, name):
    self.name = name
